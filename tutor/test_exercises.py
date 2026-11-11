import json
import uuid
from unittest.mock import AsyncMock, patch

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from google.genai import errors

from academics.management.commands.rebuild_synthetic_data import COURSE_BLUEPRINTS
from academics.models import Course, Enrollment, Grade, StudentProfile, TeacherProfile, Topic
from tutor.demo_exercises import DEMO_EXERCISES
from tutor.exercise_providers import DemoExerciseProvider, GeminiExerciseProvider
from tutor.exercise_services import generate_practice, practice_state
from tutor.models import PracticeExercise
from tutor.providers import InvalidTutorResponseError, TutorUnavailableError


# La configuración común no selecciona proveedor: cada prueba declara su modo.
# La clave sintética permite construir Gemini sin depender del .env del equipo.
@override_settings(WEAK_TOPIC_THRESHOLD=60, GEMINI_API_KEY="synthetic-test-key")
class PracticeTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="practice_student")
        self.student = StudentProfile.objects.create(
            user=self.user, student_id="2026-00001", career="Sistemas", semester=1,
        )
        self.other_user = User.objects.create_user(username="other_student")
        self.other = StudentProfile.objects.create(
            user=self.other_user, student_id="2026-00002", career="Otra carrera", semester=2,
        )
        blueprint = COURSE_BLUEPRINTS["PROG-COM"]
        self.course = Course.objects.create(code="PROG-COM", name=blueprint["name"])
        self.topics = [Topic.objects.create(course=self.course, name=name) for name in blueprint["topics"]]
        for student in (self.student, self.other):
            Enrollment.objects.create(student=student, course=self.course)
        self.set_grades([45, 59, 60, 85, None, None])
        Grade.objects.create(student=self.other, topic=self.topics[2], value=30)
        self.url = reverse("student_practice", args=[self.course.code])
        self.client.force_login(self.user)

    def set_grades(self, values):
        Grade.objects.filter(student=self.student).delete()
        for topic, value in zip(self.topics, values):
            if value is not None:
                Grade.objects.create(student=self.student, topic=topic, value=value)

    def generate(self):
        return generate_practice(user=self.user, course_code=self.course.code)

    def response(self, **changes):
        item = {"topic_id": self.topics[0].pk, "statement": "Explique usted cómo integraría los cambios de una rama conservando su historial."}
        item.update(changes)
        return json.dumps({"exercises": [item]}, ensure_ascii=False)

    @override_settings(AI_MODE="demo")
    def test_strict_threshold_and_missing_grades_ca1_ca3(self):
        exercises, _ = self.generate()
        self.assertEqual({e.topic_id for e in exercises}, {t.pk for t in self.topics[:2]})
        self.assertTrue(all(e.course == self.course and e.student == self.student for e in exercises))

    @override_settings(AI_MODE="demo", WEAK_TOPIC_THRESHOLD=70)
    def test_configurable_threshold_ca2(self):
        self.set_grades([60, 69, 70])
        exercises, _ = self.generate()
        self.assertEqual({e.topic_id for e in exercises}, {t.pk for t in self.topics[:2]})

    @override_settings(AI_MODE="demo")
    def test_no_grades_and_no_weak_topics_skip_providers_ca5(self):
        with patch.object(DemoExerciseProvider, "generate") as demo, patch.object(GeminiExerciseProvider, "generate") as real:
            self.set_grades([60, 85])
            exercises, notice = self.generate()
            self.assertFalse(exercises)
            self.assertIn("no tiene temas débiles", notice)
            self.set_grades([])
            exercises, notice = self.generate()
            self.assertFalse(exercises)
            self.assertIn("aún no tiene calificaciones", notice)
            demo.assert_not_called()
            real.assert_not_called()
        self.assertEqual(PracticeExercise.objects.count(), 0)

    @override_settings(AI_MODE="demo")
    def test_next_practice_uses_corrected_grades_ca6(self):
        first, _ = self.generate()
        self.set_grades([60, 80, 40])
        second, _ = self.generate()
        self.assertEqual({e.topic_id for e in second}, {self.topics[2].pk})
        first[0].refresh_from_db()
        self.assertEqual(first[0].topic_id, self.topics[0].pk)

    @override_settings(AI_MODE="demo")
    def test_demo_is_offline_and_profile_specific_ca8(self):
        with patch("tutor.providers._create_gemini_client") as client:
            first, _ = self.generate()
            other, _ = generate_practice(user=self.other_user, course_code=self.course.code)
        client.assert_not_called()
        self.assertEqual({e.topic_id for e in first}, {t.pk for t in self.topics[:2]})
        self.assertEqual({e.topic_id for e in other}, {self.topics[2].pk})
        self.assertTrue(all(e.mode == "demo" and e.demo_key for e in (*first, *other)))

    @override_settings(AI_MODE="demo")
    def test_catalog_covers_all_synthetic_courses_and_topics(self):
        for code, blueprint in COURSE_BLUEPRINTS.items():
            self.assertEqual(set(DEMO_EXERCISES[code]), set(blueprint["topics"]))
            if code == self.course.code:
                course, topics = self.course, self.topics
            else:
                course = Course.objects.create(code=code, name=blueprint["name"])
                Enrollment.objects.create(student=self.student, course=course)
                topics = [Topic.objects.create(course=course, name=name) for name in blueprint["topics"]]
            for topic in topics:
                Grade.objects.update_or_create(student=self.student, topic=topic, defaults={"value": 45})
            exercises, _ = generate_practice(user=self.user, course_code=code)
            self.assertEqual({e.topic_id for e in exercises}, {t.pk for t in topics})

    @override_settings(AI_MODE="real")
    def test_valid_real_response_and_private_context_ca4_ca7(self):
        with patch.object(GeminiExerciseProvider, "generate", return_value=self.response()) as provider:
            exercises, _ = self.generate()
        context = provider.call_args.args[0]
        self.assertEqual(context.career, "Sistemas")
        self.assertEqual(context.course_code, "PROG-COM")
        self.assertEqual({t["topic_id"] for t in context.weak_topics}, {t.pk for t in self.topics[:2]})
        self.assertEqual(context.academic_snapshot[2]["grade"], 60)
        self.assertEqual(context.turns, ())
        self.assertNotIn("practice_student", str(context))
        self.assertNotIn("other_student", str(context))
        self.assertEqual(exercises[0].mode, "real")
        self.assertEqual(exercises[0].demo_key, "")

    @override_settings(AI_MODE="real")
    def test_formal_statements_without_literal_markers_are_accepted(self):
        self.set_grades([45, 59, None, 40])
        cases = [
            (self.topics[0], "Defina las etapas del ciclo de integración de una rama."),
            (
                self.topics[3],
                "Diseñe un prompt estructurado utilizando la técnica de pocos ejemplos "
                "(few-shot prompting) para que un modelo de lenguaje extraiga correctamente "
                "los datos fiscales de una factura en formato de texto libre y los devuelva "
                "en un formato JSON estandarizado para posterior registro contable.",
            ),
        ]
        for topic, statement in cases:
            with self.subTest(statement=statement), patch.object(
                GeminiExerciseProvider, "generate",
                return_value=self.response(topic_id=topic.pk, statement=statement),
            ) as provider:
                exercises, _ = self.generate()
                provider.assert_called_once()
                self.assertEqual(len(exercises), 1)
                saved = PracticeExercise.objects.get(pk=exercises[0].pk)
                self.assertEqual(saved.statement, statement)
                self.assertEqual(saved.topic, topic)
                self.assertEqual(saved.student, self.student)
                self.assertEqual(saved.course, self.course)
                self.assertEqual(saved.mode, "real")

    @override_settings(AI_MODE="real")
    def test_valid_formal_batch_is_persisted_in_full(self):
        self.set_grades([45] * 6)
        statements = [
            "Detalle el proceso de integración de ramas y resolución de conflictos.",
            "Separe las responsabilidades de una función que calcula totales y guarda archivos.",
            "Identifique las entidades y relaciones necesarias para registrar ventas.",
            "Diseñe un prompt estructurado para extraer datos fiscales de una factura.",
            "Enumere las medidas necesarias para proteger la clave de una API de IA.",
            "Defina criterios de aceptación verificables antes de solicitar código a un agente.",
        ]
        raw = json.dumps({"exercises": [
            {"topic_id": topic.pk, "statement": statement}
            for topic, statement in zip(self.topics, statements)
        ]}, ensure_ascii=False)
        with patch.object(GeminiExerciseProvider, "generate", return_value=raw):
            exercises, _ = self.generate()
        self.assertEqual(len(exercises), 6)
        self.assertEqual(PracticeExercise.objects.filter(student=self.student).count(), 6)
        self.assertEqual([e.statement for e in exercises], statements)
        self.assertEqual({e.topic_id for e in exercises}, {t.pk for t in self.topics})

    @override_settings(AI_MODE="real")
    def test_invalid_provider_output_is_never_persisted_ca9(self):
        bad_outputs = [
            "", "null", "[]", "invalid JSON", "x" * 24001,
            self.response(statement=" "), self.response(statement="x" * 3001),
            self.response(topic_id=self.topics[2].pk), self.response(topic_id=True),
            self.response(statement="<script>alert(1)</script> Explique usted su respuesta."),
            self.response(statement="Explica tú cómo se integra una rama."),
            self.response(statement="Haz una integración de las ramas del repositorio."),
            self.response(statement="Escribe los pasos para integrar una rama."),
            json.dumps({"exercises": [{"topic_id": self.topics[0].pk}]}),
        ]
        for raw in bad_outputs:
            with self.subTest(raw=raw[:70]), patch.object(GeminiExerciseProvider, "generate", return_value=raw), patch.object(DemoExerciseProvider, "generate") as demo:
                with self.assertRaises(InvalidTutorResponseError):
                    self.generate()
                demo.assert_not_called()
                self.assertFalse(PracticeExercise.objects.exists())

    @override_settings(AI_MODE="real")
    def test_mixed_valid_invalid_batch_is_atomic(self):
        raw = json.loads(self.response())
        raw["exercises"].append({"topic_id": self.topics[2].pk, "statement": "Explique usted su razonamiento para este ejercicio."})
        with patch.object(GeminiExerciseProvider, "generate", return_value=json.dumps(raw)):
            with self.assertRaises(InvalidTutorResponseError):
                self.generate()
        self.assertFalse(PracticeExercise.objects.exists())

    @override_settings(AI_MODE="real")
    def test_connection_failure_falls_back_and_informs_ca9(self):
        with patch.object(GeminiExerciseProvider, "generate", side_effect=TutorUnavailableError("Sin conexión")):
            exercises, notice = self.generate()
        self.assertTrue(exercises)
        self.assertTrue(all(e.mode == "demo" for e in exercises))
        self.assertIn("modo demo", notice)

    @override_settings(AI_MODE="real")
    def test_quota_uses_shared_transport_and_falls_back_ca9(self):
        with patch("tutor.providers._create_gemini_client") as factory:
            client = factory.return_value.__enter__.return_value
            generate = client.aio.__aenter__.return_value.models.generate_content
            generate.side_effect = errors.ClientError(429, {"error": {"message": "quota"}})
            exercises, notice = self.generate()
        self.assertTrue(exercises)
        self.assertIn("modo demo", notice)
        self.assertEqual(factory.call_args.kwargs["max_attempts"], 1)
        self.assertEqual(factory.call_args.kwargs["total_timeout_ms"], 60000)

    @override_settings(AI_MODE="real")
    def test_real_transport_receives_exercise_instructions(self):
        with patch("tutor.providers._create_gemini_client") as factory:
            client = factory.return_value.__enter__.return_value
            generate = AsyncMock(return_value=type("Response", (), {"text": self.response()})())
            client.aio.__aenter__.return_value.models.generate_content = generate
            exercises, _ = self.generate()
        self.assertEqual(exercises[0].mode, "real")
        instructions = generate.call_args.kwargs["config"]["system_instruction"]
        self.assertIn("JSON", instructions)
        self.assertIn("en español con trato de usted", instructions)
        payload = json.loads(generate.call_args.kwargs["contents"])
        self.assertEqual(payload["datos_academicos"]["temas_debiles"][0]["topic_id"], self.topics[0].pk)

    @override_settings(AI_MODE="demo")
    def test_missing_demo_catalog_never_substitutes_other_topics_ca9(self):
        with patch("tutor.exercise_providers.DEMO_EXERCISES", {}):
            with self.assertRaisesMessage(TutorUnavailableError, "no hay ejercicios grabados"):
                self.generate()
        self.assertFalse(PracticeExercise.objects.exists())

    @override_settings(AI_MODE="real")
    def test_grade_change_during_generation_rejects_stale_exercises(self):
        def changed(context):
            self.set_grades([80, 80])
            return self.response()
        with patch.object(GeminiExerciseProvider, "generate", side_effect=changed):
            with self.assertRaisesMessage(TutorUnavailableError, "notas cambiaron"):
                self.generate()
        self.assertFalse(PracticeExercise.objects.exists())

    @override_settings(AI_MODE="demo")
    def test_unauthorized_generation_is_rejected_before_provider_ca7(self):
        teacher = get_user_model().objects.create_user(username="practice_teacher")
        TeacherProfile.objects.create(user=teacher)
        outsider = Course.objects.create(code="AJENO", name="Curso ajeno")
        with patch.object(DemoExerciseProvider, "generate") as provider:
            for user, code in ((None, self.course.code), (teacher, self.course.code), (self.user, outsider.code)):
                with self.subTest(user=user, code=code), self.assertRaises(PermissionDenied):
                    generate_practice(user=user, course_code=code)
            provider.assert_not_called()
        self.client.force_login(teacher)
        self.assertEqual(self.client.post(self.url).status_code, 403)
        self.client.logout()
        self.assertEqual(self.client.post(self.url).status_code, 302)

    @override_settings(AI_MODE="demo")
    def test_manipulated_post_and_csrf_are_rejected_ca7(self):
        with patch.object(DemoExerciseProvider, "generate") as provider:
            for field in ("student", "student_id", "course", "topic_id", "statement"):
                self.assertEqual(self.client.post(self.url, {field: "999"}).status_code, 403)
            provider.assert_not_called()
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.user)
        self.assertEqual(csrf_client.post(self.url).status_code, 403)
        response = csrf_client.get(self.url)
        self.assertEqual(response.status_code, 200)
        token = csrf_client.cookies["csrftoken"].value
        self.assertEqual(csrf_client.post(self.url, {"csrfmiddlewaretoken": token}).status_code, 302)

    @override_settings(AI_MODE="demo")
    def test_owned_uuid_is_stable_and_foreign_exercise_is_denied_ca10(self):
        exercises, _ = self.generate()
        exercise = exercises[0]
        self.assertIsInstance(exercise.pk, uuid.UUID)
        self.assertContains(self.client.get(self.url + f"?exercise={exercise.pk}"), str(exercise.pk))
        other, _ = generate_practice(user=self.other_user, course_code=self.course.code)
        for key in (other[0].pk, uuid.uuid4(), "invalid"):
            response = self.client.get(self.url + f"?exercise={key}")
            self.assertEqual(response.status_code, 403)
            self.assertNotContains(response, other[0].statement, status_code=403)
        exercise.refresh_from_db()
        self.assertEqual(exercise.student, self.student)

    @override_settings(AI_MODE="demo")
    def test_render_escapes_content_and_does_not_modify_official_grades_ca10(self):
        grades = list(Grade.objects.order_by("pk").values_list("pk", "value"))
        response = self.client.post(self.url, follow=True)
        self.assertContains(response, "Ejercicio grabado del modo demo")
        self.assertContains(response, self.course.name)
        exercise = PracticeExercise.objects.filter(student=self.student).first()
        exercise.statement = '<script>alert("test")</script>'
        exercise.save(update_fields=["statement"])
        page = self.client.get(self.url + f"?exercise={exercise.pk}")
        self.assertNotContains(page, '<script>alert("test")</script>')
        self.assertContains(page, "&lt;script&gt;")
        self.assertEqual(list(Grade.objects.order_by("pk").values_list("pk", "value")), grades)

    @override_settings(AI_MODE="demo")
    def test_get_does_not_generate_and_post_redirect_prevents_refresh_generation(self):
        with patch.object(DemoExerciseProvider, "generate", wraps=DemoExerciseProvider().generate) as provider:
            self.assertEqual(self.client.get(self.url).status_code, 200)
            provider.assert_not_called()
            response = self.client.post(self.url, follow=True)
            self.assertEqual(response.status_code, 200)
            self.client.get(self.url)
            provider.assert_called_once()
