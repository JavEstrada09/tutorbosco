import json
import re

from django.conf import settings
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.db.models import F

from academics.models import TeacherProfile
from tutor.demo_feedback import recorded_feedback
from tutor.exercise_services import practice_state
from tutor.feedback_providers import GeminiFeedbackProvider
from tutor.forms import ExerciseAnswerForm
from tutor.models import ExerciseAnswer, ExerciseFeedback, PracticeExercise
from tutor.providers import (
    InvalidTutorResponseError, TutorConfigurationError, TutorContext,
    TutorUnavailableError,
)
from tutor.services import get_tutor_mode


def _owned_exercises(user):
    if user is None or not user.is_authenticated:
        raise PermissionDenied
    if TeacherProfile.objects.filter(user=user).exists():
        raise PermissionDenied
    return PracticeExercise.objects.filter(
        student__user=user,
        course__enrollments__student_id=F("student_id"),
        topic__course_id=F("course_id"),
    )


def owned_exercise(user, exercise_id):
    try:
        exercise = _owned_exercises(user).select_related(
            "student", "course", "topic",
        ).filter(pk=exercise_id).first()
    except (ValidationError, ValueError) as error:
        raise PermissionDenied from error
    if exercise is None:
        raise PermissionDenied
    return exercise


def owned_answer(user, answer_id):
    try:
        answer = ExerciseAnswer.objects.filter(
            exercise__in=_owned_exercises(user), pk=answer_id,
        ).select_related("exercise__course", "exercise__topic", "feedback").first()
    except (ValidationError, ValueError) as error:
        raise PermissionDenied from error
    if answer is None:
        raise PermissionDenied
    return answer


def _context(user, exercise):
    state = practice_state(user, exercise.course.code)
    snapshot = tuple(
        {"topic": item.topic.name, "grade": item.value}
        for item in state.summary.topics
    )
    grade = next(
        (item.value for item in state.summary.topics if item.topic.pk == exercise.topic_id),
        None,
    )
    return TutorContext(
        career=state.student.career, course_name=exercise.course.name,
        course_code=exercise.course.code, academic_snapshot=snapshot,
        weak_topics=tuple(topic.name for topic in state.weak_topics),
        academic_status=(
            "no_grades" if state.summary.average is None else
            "weak_topics" if state.weak_topics else "no_weak_topics"
        ),
    ), grade


def validate_feedback(raw):
    error = InvalidTutorResponseError(
        "No se pudo obtener retroalimentación válida. Su respuesta se conservó."
    )
    if not isinstance(raw, str) or len(raw) > 12000:
        raise error
    try:
        data = json.loads(raw)
    except (ValueError, TypeError) as cause:
        raise error from cause
    if not isinstance(data, dict):
        raise error
    parts = []
    for field in ("assessment", "guidance"):
        text = data.get(field)
        if not isinstance(text, str) or not 1 <= len(text.strip()) <= 4000:
            raise error
        if re.search(r"<[^>]*>", text):
            raise error
        parts.append(text.strip())
    return f"Aciertos y aspectos por mejorar:\n{parts[0]}\n\nPara continuar:\n{parts[1]}"


def _demo_response(exercise, content, grade):
    data = recorded_feedback(exercise, content, grade)
    if data is None:
        raise TutorUnavailableError(
            "No hay retroalimentación grabada aplicable a este ejercicio y respuesta. "
            "Su respuesta se conservó."
        )
    return json.dumps(data, ensure_ascii=False)


def _request_feedback(exercise, content, context, grade):
    mode = get_tutor_mode()
    if mode == "demo":
        return _demo_response(exercise, content, grade), mode, False
    if mode != "real":
        raise TutorConfigurationError(
            "El modo de retroalimentación no está configurado. Su respuesta se conservó."
        )
    try:
        provider = GeminiFeedbackProvider(
            api_key=settings.GEMINI_API_KEY, model=settings.AI_MODEL,
            total_timeout_ms=settings.GEMINI_TOTAL_TIMEOUT_MS,
            max_attempts=settings.GEMINI_MAX_ATTEMPTS,
        )
        raw = provider.evaluate(exercise=exercise, content=content, context=context)
        return raw, "real", False
    except (TutorUnavailableError, TutorConfigurationError):
        try:
            return _demo_response(exercise, content, grade), "demo", True
        except TutorUnavailableError as error:
            raise TutorUnavailableError(
                "El proveedor real no estuvo disponible y se intentó el modo demo. "
                + str(error)
            ) from error


def submit_answer(*, user, exercise_id, content):
    # Autorización antes de validar o registrar cualquier contenido del envío.
    with transaction.atomic():
        exercise = owned_exercise(user, exercise_id)
        form = ExerciseAnswerForm({"content": content})
        if not form.is_valid():
            raise ValidationError(form.errors["content"])
        answer = ExerciseAnswer.objects.create(
            exercise=exercise, content=form.cleaned_data["content"],
        )
    # La transacción anterior termina antes de consultar el proveedor:
    # ningún error externo puede revertir la respuesta ya guardada.
    context, grade = _context(user, exercise)
    try:
        raw, source, fallback = _request_feedback(exercise, answer.content, context, grade)
        text = validate_feedback(raw)
    except (InvalidTutorResponseError, TutorUnavailableError, TutorConfigurationError) as error:
        owned_answer(user, answer.pk)
        return answer, str(error)

    with transaction.atomic():
        owned_answer(user, answer.pk)
        ExerciseFeedback.objects.create(answer=answer, text=text, source=source)
    notice = (
        "El proveedor real no estuvo disponible. Usted está utilizando retroalimentación grabada del modo demo."
        if fallback else "Su respuesta y retroalimentación se guardaron correctamente."
    )
    return answer, notice
