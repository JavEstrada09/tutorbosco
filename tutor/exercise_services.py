import json
import re
from dataclasses import dataclass

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db import transaction

from academics.models import StudentProfile, TeacherProfile
from academics.services import get_course_summaries, get_weak_topics
from tutor.exercise_providers import DemoExerciseProvider, GeminiExerciseProvider
from tutor.models import PracticeExercise
from tutor.providers import (
    InvalidTutorResponseError, TutorConfigurationError, TutorContext,
    TutorUnavailableError,
)
from tutor.services import get_tutor_mode


@dataclass(frozen=True)
class PracticeState:
    student: StudentProfile
    summary: object
    courses: tuple
    weak_topics: tuple
    message: str


def practice_state(user, course_code):
    if user is None or not user.is_authenticated:
        raise PermissionDenied
    if TeacherProfile.objects.filter(user=user).exists():
        raise PermissionDenied
    student = StudentProfile.objects.filter(user=user).first()
    if student is None:
        raise PermissionDenied
    summaries = get_course_summaries(student)
    summary = next((s for s in summaries if s.course.code == course_code), None)
    if summary is None:
        raise PermissionDenied
    weak_topics = get_weak_topics(summary.topics)
    message = ""
    if summary.average is None:
        message = "Usted aún no tiene calificaciones en este curso para identificar qué temas debe reforzar."
    elif not weak_topics:
        message = "Usted no tiene temas débiles en este curso según el umbral configurado."
    return PracticeState(
        student, summary, tuple(s.course for s in summaries), weak_topics, message,
    )


def _practice_context(state):
    return TutorContext(
        career=state.student.career,
        course_name=state.summary.course.name,
        course_code=state.summary.course.code,
        academic_snapshot=tuple(
            {"topic_id": item.topic.pk, "topic": item.topic.name, "grade": item.value}
            for item in state.summary.topics
        ),
        weak_topics=tuple(
            {"topic_id": topic.pk, "topic": topic.name} for topic in state.weak_topics
        ),
        academic_status="weak_topics",
    )


def _invalid_response():
    return InvalidTutorResponseError(
        "No se pudo generar una práctica válida para sus temas débiles. Inténtelo nuevamente."
    )


def validate_exercises(raw, allowed_topics):
    """Valida el lote completo antes de guardar cualquier ejercicio."""
    if not isinstance(raw, str) or len(raw) > 24000:
        raise _invalid_response()
    try:
        data = json.loads(raw)
    except (ValueError, TypeError) as error:
        raise _invalid_response() from error
    if not isinstance(data, dict) or set(data) != {"exercises"}:
        raise _invalid_response()
    exercises = data["exercises"]
    if not isinstance(exercises, list) or not 1 <= len(exercises) <= 6:
        raise _invalid_response()
    seen = set()
    validated = []
    for item in exercises:
        if not isinstance(item, dict):
            raise _invalid_response()
        topic_id = item.get("topic_id")
        text = item.get("statement")
        if (
            type(topic_id) is not int or topic_id not in allowed_topics
            or topic_id in seen or not isinstance(text, str)
            or not 10 <= len(text.strip()) <= 3000
            or re.search(r"<[^>]*>", text)
        ):
            raise _invalid_response()
        # No exigir palabras literales: «Defina» y «Diseñe» también son formales.
        # Idioma y trato formal se indican al proveedor y se revisan en CA-10.
        words = set(re.findall(r"\b\w+\b", text.casefold()))
        if words.intersection({"tú", "vosotros", "vos", "haz", "escribe", "explica"}):
            raise _invalid_response()
        seen.add(topic_id)
        validated.append((topic_id, text.strip()))
    return validated


def generate_practice(*, user, course_code):
    state = practice_state(user, course_code)
    if state.message:
        return (), state.message
    context = _practice_context(state)
    mode = get_tutor_mode()
    fallback = False
    if mode == "demo":
        raw = DemoExerciseProvider().generate(context)
    elif mode == "real":
        try:
            raw = GeminiExerciseProvider(
                api_key=settings.GEMINI_API_KEY, model=settings.AI_MODEL,
                total_timeout_ms=settings.GEMINI_TOTAL_TIMEOUT_MS,
                max_attempts=settings.GEMINI_MAX_ATTEMPTS,
            ).generate(context)
        except (TutorUnavailableError, TutorConfigurationError):
            raw = DemoExerciseProvider().generate(context)
            mode, fallback = "demo", True
    else:
        raise TutorConfigurationError("El modo de práctica no está configurado correctamente.")

    topics = {topic.pk: topic for topic in state.weak_topics}
    if mode == "demo" and json.loads(raw) == {"exercises": []}:
        raise TutorUnavailableError(
            "No se pudo generar la práctica: no hay ejercicios grabados aplicables a sus temas débiles."
            + (" Se intentó utilizar el modo demo porque el proveedor real no estuvo disponible." if fallback else "")
        )
    validated = validate_exercises(raw, topics)
    demo_keys = {
        item["topic_id"]: item["demo_key"]
        for item in json.loads(raw)["exercises"]
    } if mode == "demo" else {}
    # No mantener una transacción abierta mientras se consulta la API.
    with transaction.atomic():
        current = practice_state(user, course_code)
        current_ids = {topic.pk for topic in current.weak_topics}
        if not set(topics).issubset(current_ids):
            raise TutorUnavailableError(
                "Sus notas cambiaron durante la generación. Solicite una nueva práctica."
            )
        exercises = tuple(
            PracticeExercise.objects.create(
                student=current.student, course=current.summary.course,
                topic=topics[topic_id], statement=text, mode=mode,
                demo_key=demo_keys.get(topic_id, ""),
            )
            for topic_id, text in validated
        )
    message = (
        "El proveedor real no estuvo disponible. Usted está utilizando ejercicios grabados del modo demo."
        if fallback else "Su práctica se generó correctamente."
    )
    return exercises, message
