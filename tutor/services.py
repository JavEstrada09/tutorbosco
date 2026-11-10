import re
from dataclasses import dataclass

from django.conf import settings
from django.contrib.auth import SESSION_KEY
from django.contrib.sessions.models import Session
from django.core.exceptions import PermissionDenied
from django.db.models import Exists, F
from django.utils import timezone

from academics.models import Enrollment
from academics.services import get_course_summaries, is_weak
from tutor.models import TutorConversation

from tutor.providers import (
    DemoTutorProvider,
    GeminiTutorProvider,
    InvalidTutorResponseError,
    TutorConfigurationError,
    TutorContext,
)


@dataclass(frozen=True)
class TutorReply:
    text: str
    mode: str


def get_tutor_mode():
    mode = getattr(settings, "AI_MODE", "")
    if not isinstance(mode, str):
        return ""
    return mode.strip().lower()


def _select_provider(mode=None):
    mode = mode or get_tutor_mode()
    if mode == "demo":
        return DemoTutorProvider(), mode
    if mode == "real":
        return (
            GeminiTutorProvider(
                api_key=settings.GEMINI_API_KEY,
                model=settings.AI_MODEL,
                total_timeout_ms=settings.GEMINI_TOTAL_TIMEOUT_MS,
                max_attempts=settings.GEMINI_MAX_ATTEMPTS,
            ),
            mode,
        )
    raise TutorConfigurationError(
        "El modo del tutor no es válido. Puede continuar en modo demo."
    )


def _validate_response(response, context):
    if not isinstance(response, str) or not response.strip():
        raise InvalidTutorResponseError(
            "El tutor real no devolvió una respuesta válida. "
            "Puede continuar en modo demo."
        )
    text = response.strip()
    if len(text) > 10_000:
        raise InvalidTutorResponseError(
            "La respuesta del tutor real es demasiado extensa. "
            "Puede continuar en modo demo."
        )
    normalized_text = text.casefold()
    words = set(re.findall(r"\b[\wáéíóúüñ]+\b", normalized_text))
    spanish_markers = {
        "como",
        "con",
        "de",
        "el",
        "en",
        "es",
        "la",
        "para",
        "por",
        "puede",
        "que",
        "su",
        "una",
        "usted",
    }
    if (
        context.course_name.casefold() not in normalized_text
        or "usted" not in normalized_text
        or len(words & spanish_markers) < 4
    ):
        raise InvalidTutorResponseError(
            "La respuesta del tutor real no cumple el formato esperado. "
            "Puede continuar en modo demo."
        )
    return text


def ask_tutor(
    *, question: str, career: str, course_name: str, mode=None, context=None
) -> TutorReply:
    context = context or TutorContext(career=career, course_name=course_name)
    provider, mode = _select_provider(mode)
    response = provider.answer(question=question, context=context)
    return TutorReply(text=_validate_response(response, context), mode=mode)


class StaleConversationError(Exception):
    """La revisión solicitada ya no corresponde al hilo activo."""


def _academic_snapshot(student, course):
    for summary in get_course_summaries(student):
        if summary.course == course:
            return [
                {"topic": item.topic.name, "grade": item.value}
                for item in summary.topics
            ]
    raise PermissionDenied


def open_conversation(*, session_key, student, course):
    """Devuelve el hilo activo y si se creó, para la sesión del estudiante."""
    session = Session.objects.filter(
        pk=session_key, expire_date__gt=timezone.now()
    ).first()
    if session is None or session.get_decoded().get(SESSION_KEY) != str(student.user_id):
        raise PermissionDenied

    if not Enrollment.objects.filter(student=student, course=course).exists():
        raise PermissionDenied

    return TutorConversation.objects.get_or_create(
        session=session,
        student=student,
        course=course,
        defaults={"academic_snapshot": lambda: _academic_snapshot(student, course)},
    )


def _current_conversation(conversation, revision):
    enrollment = Enrollment.objects.filter(
        student_id=conversation.student_id, course_id=conversation.course_id
    )
    return TutorConversation.objects.filter(
        Exists(enrollment),
        pk=conversation.pk,
        session_id=conversation.session_id,
        session__expire_date__gt=timezone.now(),
        student_id=conversation.student_id,
        course_id=conversation.course_id,
        revision=revision,
    )


def _reject_unavailable(conversation):
    if not Enrollment.objects.filter(
        student_id=conversation.student_id, course_id=conversation.course_id
    ).exists():
        raise PermissionDenied
    raise StaleConversationError


def check_conversation_revision(conversation, revision):
    """Comprueba la revisión antes de iniciar una consulta al proveedor."""
    if revision != conversation.revision or not _current_conversation(
        conversation, revision
    ).exists():
        _reject_unavailable(conversation)


def _update_conversation(conversation, revision, **changes):
    if revision != conversation.revision:
        _reject_unavailable(conversation)
    updated = _current_conversation(conversation, revision).update(
        revision=F("revision") + 1, **changes
    )
    if not updated:
        _reject_unavailable(conversation)


def reset_conversation(conversation, revision):
    _update_conversation(
        conversation,
        revision,
        academic_snapshot=_academic_snapshot(conversation.student, conversation.course),
        turns=[],
        pending_question="",
    )


def store_pending_question(conversation, revision, question):
    _update_conversation(conversation, revision, pending_question=question)


def append_conversation_turn(conversation, revision, *, question, answer):
    """Guarda el turno ya validado y consume la pregunta pendiente."""
    _update_conversation(
        conversation,
        revision,
        turns=[*conversation.turns, {"question": question, "answer": answer}],
        pending_question="",
    )


# Cuatro turnos recientes; cada pregunta ya está limitada a 500 caracteres.
# Se limita la respuesta enviada, conservando completos los turnos en la base.
CONTEXT_TURN_LIMIT = 4
CONTEXT_ANSWER_LIMIT = 2000


def conversation_context(conversation):
    """Proyecta solo los datos permitidos del hilo, sin identificadores."""
    snapshot = tuple(
        {"topic": item["topic"], "grade": item["grade"]}
        for item in conversation.academic_snapshot
    )
    weak_topics = tuple(item["topic"] for item in snapshot if is_weak(item["grade"]))
    has_grades = any(item["grade"] is not None for item in snapshot)
    return TutorContext(
        career=conversation.student.career,
        course_name=conversation.course.name,
        course_code=conversation.course.code,
        academic_snapshot=snapshot,
        weak_topics=weak_topics,
        academic_status=(
            "weak_topics" if weak_topics else "no_weak_topics" if has_grades else "no_grades"
        ),
        turns=tuple(
            {"question": turn["question"][:500],
             "answer": turn["answer"][:CONTEXT_ANSWER_LIMIT]}
            for turn in conversation.turns[-CONTEXT_TURN_LIMIT:]
        ),
    )
