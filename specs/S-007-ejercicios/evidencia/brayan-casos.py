"""Casos independientes de Brayan para S-007 sobre una base SQLite aislada."""

import json
import os
import sys
import uuid
from pathlib import Path
from unittest.mock import patch

ROOT_DIR = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.test import Client, override_settings
from django.urls import reverse
from google.genai import errors

from academics.models import (
    Course,
    Enrollment,
    Grade,
    StudentProfile,
    TeacherProfile,
)
from tutor.exercise_providers import DemoExerciseProvider, GeminiExerciseProvider
from tutor.exercise_services import generate_practice, practice_state
from tutor.models import PracticeExercise
from tutor.providers import InvalidTutorResponseError, TutorUnavailableError


results = []


def record(criterion, passed, detail):
    status = "PASS" if passed else "FAIL"
    results.append((criterion, passed, detail))
    print(f"{criterion} {status}: {detail}")


def expect_error(error_type, callback):
    try:
        callback()
    except error_type:
        return True
    return False


def replace_grades(student, topics, values):
    Grade.objects.filter(student=student).delete()
    for topic, value in zip(topics, values):
        if value is not None:
            Grade.objects.create(student=student, topic=topic, value=value)


def new_student(username, student_id, course, career):
    user = get_user_model().objects.create_user(username=username)
    user.set_unusable_password()
    user.save(update_fields=["password"])
    student = StudentProfile.objects.create(
        user=user,
        student_id=student_id,
        career=career,
        semester=8,
    )
    Enrollment.objects.create(student=student, course=course)
    return user, student


def real_response(topic, statement=None):
    return json.dumps(
        {
            "exercises": [
                {
                    "topic_id": topic.pk,
                    "statement": statement
                    or "Explique usted cómo aplicaría este tema en un caso comercial.",
                }
            ]
        },
        ensure_ascii=False,
    )


User = get_user_model()
User.objects.filter(username__startswith="verify_s007_").delete()
Course.objects.filter(code="VER-AJENO").delete()

course = Course.objects.get(code="PROG-COM")
topics = list(course.topics.order_by("pk"))
user, student = new_student(
    "verify_s007_student",
    "2026-90001",
    course,
    "Verificacion de Sistemas",
)
other_user, other_student = new_student(
    "verify_s007_other",
    "2026-90002",
    course,
    "Verificacion Diferente",
)
no_weak_user, no_weak_student = new_student(
    "verify_s007_no_weak",
    "2026-90003",
    course,
    "Verificacion sin temas debiles",
)
no_grades_user, no_grades_student = new_student(
    "verify_s007_no_grades",
    "2026-90004",
    course,
    "Verificacion sin notas",
)
teacher_user = User.objects.create_user(username="verify_s007_teacher")
teacher_user.set_unusable_password()
teacher_user.save(update_fields=["password"])
TeacherProfile.objects.create(user=teacher_user)
outsider = Course.objects.create(code="VER-AJENO", name="Curso ajeno de verificacion")

demo_student_password = os.environ.get("DEMO_STUDENT_PASSWORD")
demo_teacher_password = os.environ.get("DEMO_TEACHER_PASSWORD")
if not demo_student_password or not demo_teacher_password:
    raise RuntimeError("Las contrasenas demo deben estar configuradas localmente.")
for verification_user in (user, other_user, no_weak_user, no_grades_user):
    verification_user.set_password(demo_student_password)
    verification_user.save(update_fields=["password"])
teacher_user.set_password(demo_teacher_password)
teacher_user.save(update_fields=["password"])
replace_grades(no_weak_student, topics, [60, 85, 90, None, None, None])


# CA-1 y CA-3: comparacion estricta y notas ausentes.
with override_settings(WEAK_TOPIC_THRESHOLD=60, AI_MODE="demo"):
    replace_grades(student, topics, [45, 59, 60, 85, None, None])
    state = practice_state(user, course.code)
    weak_ids = {topic.pk for topic in state.weak_topics}
    record(
        "CA-1",
        weak_ids == {topics[0].pk, topics[1].pk},
        f"debiles={sorted(weak_ids)}; esperados={[topics[0].pk, topics[1].pk]}",
    )
    record(
        "CA-3",
        topics[4].pk not in weak_ids and topics[5].pk not in weak_ids,
        "dos temas sin nota quedaron fuera de la seleccion",
    )


# CA-2: el umbral se cambia en el mismo proceso que ejecuta el servicio.
with override_settings(WEAK_TOPIC_THRESHOLD=70, AI_MODE="demo"):
    replace_grades(student, topics, [60, 69, 70, None, None, None])
    state = practice_state(user, course.code)
    weak_ids = {topic.pk for topic in state.weak_topics}
    record(
        "CA-2",
        weak_ids == {topics[0].pk, topics[1].pk},
        f"umbral efectivo=70; debiles={sorted(weak_ids)}",
    )


# CA-4: lote real simulado, nuevo y limitado al tema permitido.
with override_settings(
    WEAK_TOPIC_THRESHOLD=60,
    AI_MODE="real",
    GEMINI_API_KEY="synthetic-verification-key",
):
    replace_grades(student, topics, [45, 60, 85, None, None, None])
    old_ids = set(PracticeExercise.objects.values_list("pk", flat=True))
    with patch.object(
        GeminiExerciseProvider,
        "generate",
        return_value=real_response(topics[0]),
    ) as provider:
        exercises, _ = generate_practice(user=user, course_code=course.code)
    new_ids = {item.pk for item in exercises} - old_ids
    context = provider.call_args.args[0]
    ca4_ok = (
        len(new_ids) == 1
        and all(item.statement and item.course == course for item in exercises)
        and {item.topic_id for item in exercises} == {topics[0].pk}
        and {item["topic_id"] for item in context.weak_topics} == {topics[0].pk}
    )
    record("CA-4", ca4_ok, f"ejercicios_nuevos={len(new_ids)}; tema={topics[0].name}")


# CA-5: estados distintos y cero llamadas a proveedores.
with override_settings(WEAK_TOPIC_THRESHOLD=60, AI_MODE="demo"):
    with patch.object(DemoExerciseProvider, "generate") as demo, patch.object(
        GeminiExerciseProvider, "generate"
    ) as real:
        replace_grades(student, topics, [60, 85, None, None, None, None])
        no_weak, no_weak_notice = generate_practice(user=user, course_code=course.code)
        replace_grades(student, topics, [None] * 6)
        no_grades, no_grades_notice = generate_practice(user=user, course_code=course.code)
    ca5_ok = (
        not no_weak
        and not no_grades
        and "no tiene temas débiles" in no_weak_notice
        and "aún no tiene calificaciones" in no_grades_notice
        and demo.call_count == 0
        and real.call_count == 0
    )
    record("CA-5", ca5_ok, "avisos distintos; llamadas demo=0 y real=0")


# CA-6: solo cambia la practica nueva; el UUID historico permanece.
with override_settings(WEAK_TOPIC_THRESHOLD=60, AI_MODE="demo"):
    replace_grades(student, topics, [45, 80, 85, None, None, None])
    first, _ = generate_practice(user=user, course_code=course.code)
    historical_id = first[0].pk
    replace_grades(student, topics, [60, 40, 85, None, None, None])
    second, _ = generate_practice(user=user, course_code=course.code)
    ca6_ok = (
        {item.topic_id for item in second} == {topics[1].pk}
        and PracticeExercise.objects.filter(pk=historical_id, topic=topics[0]).exists()
    )
    record(
        "CA-6",
        ca6_ok,
        f"historico_conservado={historical_id}; tema_nuevo={topics[1].name}",
    )


# CA-7: servicio, HTTP, CSRF, UUID ajeno y contexto privado.
with override_settings(WEAK_TOPIC_THRESHOLD=60, AI_MODE="demo"):
    replace_grades(student, topics, [45, 60, 85, None, None, None])
    with patch.object(DemoExerciseProvider, "generate") as provider:
        direct_denials = [
            expect_error(
                PermissionDenied,
                lambda: generate_practice(user=AnonymousUser(), course_code=course.code),
            ),
            expect_error(
                PermissionDenied,
                lambda: generate_practice(user=teacher_user, course_code=course.code),
            ),
            expect_error(
                PermissionDenied,
                lambda: generate_practice(user=user, course_code=outsider.code),
            ),
        ]
        unauthorized_provider_calls = provider.call_count
    anonymous = Client(HTTP_HOST="localhost")
    student_client = Client(HTTP_HOST="localhost")
    student_client.force_login(user)
    teacher_client = Client(HTTP_HOST="localhost")
    teacher_client.force_login(teacher_user)
    practice_url = reverse("student_practice", args=[course.code])
    outsider_url = reverse("student_practice", args=[outsider.code])
    http_codes = [
        anonymous.post(practice_url).status_code,
        teacher_client.post(practice_url).status_code,
        student_client.post(outsider_url).status_code,
        student_client.post(practice_url, {"student_id": other_student.pk}).status_code,
    ]
    csrf_client = Client(enforce_csrf_checks=True, HTTP_HOST="localhost")
    csrf_client.force_login(user)
    csrf_code = csrf_client.post(practice_url).status_code
    replace_grades(other_student, topics, [30, 80, 85, None, None, None])
    foreign, _ = generate_practice(user=other_user, course_code=course.code)
    foreign_page = student_client.get(f"{practice_url}?exercise={foreign[0].pk}")

with override_settings(
    WEAK_TOPIC_THRESHOLD=60,
    AI_MODE="real",
    GEMINI_API_KEY="synthetic-verification-key",
):
    replace_grades(student, topics, [45, 60, 85, None, None, None])
    with patch.object(
        GeminiExerciseProvider,
        "generate",
        return_value=real_response(topics[0]),
    ) as provider:
        generate_practice(user=user, course_code=course.code)
    context_text = str(provider.call_args.args[0])
    context_ok = (
        "verify_s007_student" not in context_text
        and "verify_s007_other" not in context_text
        and outsider.code not in context_text
        and provider.call_args.args[0].course_code == course.code
    )

ca7_ok = (
    all(direct_denials)
    and unauthorized_provider_calls == 0
    and provider.call_count == 1
    and http_codes == [302, 403, 403, 403]
    and csrf_code == 403
    and foreign_page.status_code == 403
    and foreign[0].statement not in foreign_page.content.decode(errors="replace")
    and context_ok
)
record(
    "CA-7",
    ca7_ok,
    f"HTTP={http_codes}; CSRF={csrf_code}; UUID_ajeno={foreign_page.status_code}; contexto_aislado={context_ok}",
)


# CA-8: dos perfiles distintos, sin construir cliente Gemini y sin URLs externas.
with override_settings(WEAK_TOPIC_THRESHOLD=60, AI_MODE="demo", GEMINI_API_KEY=""):
    replace_grades(student, topics, [45, 80, 85, None, None, None])
    replace_grades(other_student, topics, [80, 45, 85, None, None, None])
    with patch("tutor.providers._create_gemini_client") as gemini_client:
        first, _ = generate_practice(user=user, course_code=course.code)
        other, _ = generate_practice(user=other_user, course_code=course.code)
    page = student_client.get(practice_url).content.decode(errors="replace")
    ca8_ok = (
        gemini_client.call_count == 0
        and {item.topic_id for item in first} == {topics[0].pk}
        and {item.topic_id for item in other} == {topics[1].pk}
        and all(item.mode == "demo" and item.demo_key for item in (*first, *other))
        and "https://" not in page
        and "http://" not in page
    )
    record("CA-8", ca8_ok, "cliente Gemini=0; perfiles distintos; HTML sin recursos HTTP externos")


# CA-9: conexion, cuota, salidas invalidas y catalogo ausente simulados.
with override_settings(
    WEAK_TOPIC_THRESHOLD=60,
    AI_MODE="real",
    GEMINI_API_KEY="synthetic-verification-key",
):
    replace_grades(student, topics, [45, 60, 85, None, None, None])
    with patch.object(
        GeminiExerciseProvider,
        "generate",
        side_effect=TutorUnavailableError("Conexion simulada"),
    ):
        fallback, fallback_notice = generate_practice(user=user, course_code=course.code)
    before_invalid = PracticeExercise.objects.count()
    invalid_cases = []
    for raw in ("", real_response(topics[2]), json.dumps({"exercises": [{"topic_id": topics[0].pk}]})):
        with patch.object(GeminiExerciseProvider, "generate", return_value=raw):
            invalid_cases.append(
                expect_error(
                    InvalidTutorResponseError,
                    lambda: generate_practice(user=user, course_code=course.code),
                )
            )
    invalid_atomic = PracticeExercise.objects.count() == before_invalid

with override_settings(
    WEAK_TOPIC_THRESHOLD=60,
    AI_MODE="real",
    GEMINI_API_KEY="synthetic-verification-key",
):
    with patch("tutor.providers._create_gemini_client") as factory:
        client = factory.return_value.__enter__.return_value
        generate = client.aio.__aenter__.return_value.models.generate_content
        generate.side_effect = errors.ClientError(429, {"error": {"message": "quota"}})
        quota, quota_notice = generate_practice(user=user, course_code=course.code)
    quota_ok = (
        bool(quota)
        and "modo demo" in quota_notice
        and factory.call_args.kwargs["max_attempts"] == 1
    )

with override_settings(WEAK_TOPIC_THRESHOLD=60, AI_MODE="demo"):
    with patch("tutor.exercise_providers.DEMO_EXERCISES", {}):
        missing_catalog = expect_error(
            TutorUnavailableError,
            lambda: generate_practice(user=user, course_code=course.code),
        )

ca9_ok = (
    bool(fallback)
    and all(item.mode == "demo" for item in fallback)
    and "modo demo" in fallback_notice
    and all(invalid_cases)
    and invalid_atomic
    and quota_ok
    and missing_catalog
)
record(
    "CA-9",
    ca9_ok,
    "conexion y cuota simuladas; invalidos rechazados atomicamente; catalogo ausente informado",
)


# CA-10: idioma formal, UUID, relaciones, escape y notas oficiales intactas.
with override_settings(WEAK_TOPIC_THRESHOLD=60, AI_MODE="demo"):
    replace_grades(student, topics, [45, 60, 85, None, None, None])
    grades_before = list(
        Grade.objects.filter(student=student).order_by("pk").values_list("pk", "value")
    )
    exercises, _ = generate_practice(user=user, course_code=course.code)
    exercise = exercises[0]
    stable_id = exercise.pk
    exercise.refresh_from_db()
    formal_spanish = "usted" in exercise.statement.casefold()
    relations_ok = (
        isinstance(stable_id, uuid.UUID)
        and exercise.pk == stable_id
        and exercise.student == student
        and exercise.course == course
        and exercise.topic == topics[0]
    )
    exercise.statement = '<script>alert("verificacion")</script>'
    exercise.save(update_fields=["statement"])
    rendered = student_client.get(f"{practice_url}?exercise={stable_id}")
    body = rendered.content.decode(errors="replace")
    escaped = '<script>alert("verificacion")</script>' not in body and "&lt;script&gt;" in body
    grades_after = list(
        Grade.objects.filter(student=student).order_by("pk").values_list("pk", "value")
    )
    record(
        "CA-10",
        formal_spanish and relations_ok and escaped and grades_before == grades_after,
        f"UUID={stable_id}; formal={formal_spanish}; escape={escaped}; notas_sin_cambios={grades_before == grades_after}",
    )


failed = [criterion for criterion, passed, _ in results if not passed]
print(f"SUMMARY total={len(results)} passed={len(results) - len(failed)} failed={len(failed)}")
if failed:
    print("FAILED_CRITERIA=" + ",".join(failed))
    sys.exit(1)
