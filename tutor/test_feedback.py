import json
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import httpx2
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from google.genai import errors

from academics.models import Course, Enrollment, Grade, StudentProfile, TeacherProfile, Topic
from tutor.demo_exercises import DEMO_EXERCISES
from tutor.demo_feedback import DEMO_FEEDBACK, demo_case
from tutor.feedback import owned_answer, submit_answer
from tutor.feedback_providers import GeminiFeedbackProvider
from tutor.models import ExerciseAnswer, ExerciseFeedback, PracticeExercise
from tutor.providers import TutorUnavailableError


@override_settings(WEAK_TOPIC_THRESHOLD=60, GEMINI_API_KEY="synthetic-test-key")
class FeedbackTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="feedback_student")
        self.other_user = User.objects.create_user(username="feedback_other")
        self.teacher = User.objects.create_user(username="feedback_teacher")
        TeacherProfile.objects.create(user=self.teacher)
        self.student = StudentProfile.objects.create(
            user=self.user, student_id="2026-00001", career="Sistemas", semester=1,
        )
        self.other = StudentProfile.objects.create(
            user=self.other_user, student_id="2026-00002", career="Otra carrera", semester=2,
        )
        self.course = Course.objects.create(code="PROG-COM", name="Programación Comercial")
        self.topic = Topic.objects.create(course=self.course, name="Git y GitHub avanzado")
        for student, value in ((self.student, 25), (self.other, 55)):
            Enrollment.objects.create(student=student, course=self.course)
            Grade.objects.create(student=student, topic=self.topic, value=value)
        key, statement = DEMO_EXERCISES[self.course.code][self.topic.name]
        self.exercise = PracticeExercise.objects.create(
            student=self.student, course=self.course, topic=self.topic,
            statement=statement, mode="demo", demo_key=key,
        )
        self.foreign = PracticeExercise.objects.create(
            student=self.other, course=self.course, topic=self.topic,
            statement=statement, mode="demo", demo_key=key,
        )
        self.case = DEMO_FEEDBACK[key]
        self.url = reverse("exercise_answer", args=[self.exercise.pk])
        self.client.force_login(self.user)

    def submit(self, content=None, **changes):
        return submit_answer(
            user=changes.get("user", self.user),
            exercise_id=changes.get("exercise_id", self.exercise.pk),
            content=self.case.correct if content is None else content,
        )

    def raw(self, **changes):
        data = {
            "assessment": "Identifica la integración de ramas y la conservación del historial.",
            "guidance": "Revise los conflictos antes de confirmar la integración y ejecute las pruebas.",
        }
        data.update(changes)
        return json.dumps(data, ensure_ascii=False)

    @override_settings(AI_MODE="demo")
    def test_answer_is_persisted_with_derived_ownership_ca1(self):
        answer, _ = self.submit("  " + self.case.correct + "  ")
        answer.refresh_from_db()
        self.assertIsInstance(answer.pk, uuid.UUID)
        self.assertEqual(answer.content, self.case.correct)
        self.assertEqual(answer.exercise.student, self.student)
        self.assertEqual(answer.exercise.course, self.course)
        self.assertEqual(answer.exercise.topic, self.topic)
        self.assertEqual(answer.feedback.source, "demo")

    @override_settings(AI_MODE="real")
    def test_empty_and_excessive_answers_never_call_provider_ca2(self):
        with patch.object(GeminiFeedbackProvider, "evaluate") as provider:
            for content in ("", "   \n\t", "x" * 4001):
                with self.subTest(length=len(content)), self.assertRaises(ValidationError):
                    self.submit(content)
                response = self.client.post(self.url, {"content": content})
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.context["answer_form"].errors)
            provider.assert_not_called()
        self.assertFalse(ExerciseAnswer.objects.exists())

    @override_settings(AI_MODE="real")
    def test_maximum_length_answer_is_accepted(self):
        with patch.object(GeminiFeedbackProvider, "evaluate", return_value=self.raw()):
            answer, _ = self.submit("x" * 4000)
        self.assertEqual(len(answer.content), 4000)
        self.assertTrue(ExerciseFeedback.objects.filter(answer=answer).exists())

    @override_settings(AI_MODE="real")
    def test_real_feedback_is_related_to_saved_answer_ca3(self):
        def evaluate(*, exercise, content, context):
            self.assertTrue(ExerciseAnswer.objects.filter(exercise=exercise, content=content).exists())
            self.assertEqual(exercise.pk, self.exercise.pk)
            self.assertEqual(content, self.case.correct)
            return self.raw()
        with patch.object(GeminiFeedbackProvider, "evaluate", side_effect=evaluate):
            answer, _ = self.submit()
        self.assertEqual(answer.feedback.source, "real")
        self.assertIn("conservación del historial", answer.feedback.text)
        self.assertIn("Revise los conflictos", answer.feedback.text)

    @override_settings(AI_MODE="real")
    def test_context_is_private_and_uses_current_grades_ca4(self):
        with patch.object(GeminiFeedbackProvider, "evaluate", return_value=self.raw()) as provider:
            self.submit()
            first = provider.call_args.kwargs["context"]
            Grade.objects.filter(student=self.student, topic=self.topic).update(value=65)
            self.submit()
            second = provider.call_args.kwargs["context"]
            self.submit(user=self.other_user, exercise_id=self.foreign.pk)
            third = provider.call_args.kwargs["context"]
        self.assertEqual(first.academic_snapshot, ({"topic": self.topic.name, "grade": 25},))
        self.assertEqual(second.academic_snapshot[0]["grade"], 65)
        self.assertEqual(second.weak_topics, ())
        self.assertEqual(third.academic_snapshot[0]["grade"], 55)
        self.assertEqual(first.career, "Sistemas")
        self.assertEqual(third.career, "Otra carrera")
        self.assertNotIn(self.other_user.username, str(first))
        self.assertEqual(first.turns, ())

    @override_settings(AI_MODE="demo")
    def test_demo_support_varies_by_current_topic_grade_ca4(self):
        first, _ = self.submit()
        other, _ = self.submit(user=self.other_user, exercise_id=self.foreign.pk)
        self.assertIn(self.case.detailed, first.feedback.text)
        self.assertIn(self.case.brief, other.feedback.text)
        Grade.objects.filter(student=self.student, topic=self.topic).delete()
        no_grade, _ = self.submit()
        self.assertIn(self.case.detailed, no_grade.feedback.text)

    @override_settings(AI_MODE="demo")
    def test_attempts_remain_distinct_across_exercises_and_courses_ca5(self):
        first, _ = self.submit()
        second, _ = self.submit(self.case.incorrect)
        course = Course.objects.create(code="BD-APL", name="Bases de Datos Aplicadas")
        topic = Topic.objects.create(course=course, name="Consultas SQL")
        Enrollment.objects.create(student=self.student, course=course)
        key, statement = DEMO_EXERCISES[course.code][topic.name]
        exercise = PracticeExercise.objects.create(
            student=self.student, course=course, topic=topic,
            statement=statement, demo_key=key, mode="demo",
        )
        third, _ = self.submit(DEMO_FEEDBACK[key].correct, exercise_id=exercise.pk)
        self.assertEqual(len({first.pk, second.pk, third.pk}), 3)
        for answer, expected, excluded in (
            (first, self.case.success, self.case.correction),
            (second, self.case.correction, self.case.success),
            (third, DEMO_FEEDBACK[key].success, self.case.success),
        ):
            page = self.client.get(reverse("exercise_answer_result", args=[answer.pk]))
            self.assertContains(page, expected)
            self.assertNotContains(page, excluded)
        self.assertEqual(ExerciseAnswer.objects.count(), 3)

    @override_settings(AI_MODE="real")
    def test_unauthorized_submissions_never_write_or_call_provider_ca6(self):
        users_and_ids = (
            (None, self.exercise.pk), (self.teacher, self.exercise.pk),
            (self.user, self.foreign.pk), (self.user, uuid.uuid4()),
            (self.user, "invalid"),
        )
        with patch.object(GeminiFeedbackProvider, "evaluate") as provider:
            for user, key in users_and_ids:
                with self.subTest(user=user, exercise=key), self.assertRaises(PermissionDenied):
                    self.submit(user=user, exercise_id=key)
            provider.assert_not_called()
        self.assertFalse(ExerciseAnswer.objects.exists())

    @override_settings(AI_MODE="demo")
    def test_foreign_and_missing_answer_results_are_denied_ca6(self):
        answer, _ = self.submit(user=self.other_user, exercise_id=self.foreign.pk)
        for key in (answer.pk, uuid.uuid4()):
            page = self.client.get(reverse("exercise_answer_result", args=[key]))
            self.assertEqual(page.status_code, 403)
            self.assertNotContains(page, answer.content, status_code=403)
        self.client.force_login(self.teacher)
        self.assertEqual(self.client.get(self.url).status_code, 403)
        self.client.logout()
        self.assertEqual(self.client.get(self.url).status_code, 302)

    @override_settings(AI_MODE="demo")
    def test_unassigned_course_and_revoked_enrollment_are_denied_ca6(self):
        answer, _ = self.submit()
        Enrollment.objects.filter(student=self.student).delete()
        self.assertEqual(self.client.get(self.url).status_code, 403)
        self.assertEqual(self.client.post(self.url, {"content": self.case.correct}).status_code, 403)
        with self.assertRaises(PermissionDenied):
            owned_answer(self.user, answer.pk)
        self.assertEqual(ExerciseAnswer.objects.count(), 1)

    @override_settings(AI_MODE="demo")
    def test_inconsistent_exercise_course_is_rejected(self):
        course = Course.objects.create(code="OTRO", name="Otro curso")
        Enrollment.objects.create(student=self.student, course=course)
        PracticeExercise.objects.filter(pk=self.exercise.pk).update(course=course)
        self.assertEqual(self.client.post(self.url, {"content": self.case.correct}).status_code, 403)
        self.assertFalse(ExerciseAnswer.objects.exists())

    @override_settings(AI_MODE="demo")
    def test_manipulated_relations_and_csrf_are_rejected_ca6(self):
        for field in ("student", "student_id", "course", "topic_id", "exercise_id", "answer_id"):
            self.assertEqual(self.client.post(self.url, {"content": self.case.correct, field: "999"}).status_code, 403)
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.user)
        self.assertEqual(csrf_client.post(self.url, {"content": self.case.correct}).status_code, 403)
        self.assertFalse(ExerciseAnswer.objects.exists())
        csrf_client.get(self.url)
        response = csrf_client.post(self.url, {
            "content": self.case.correct,
            "csrfmiddlewaretoken": csrf_client.cookies["csrftoken"].value,
        })
        self.assertEqual(response.status_code, 302)

    @override_settings(AI_MODE="demo", GEMINI_API_KEY="")
    def test_demo_correct_and_incorrect_answers_are_offline_ca7(self):
        with patch("tutor.providers._create_gemini_client", side_effect=AssertionError("No Gemini")), patch(
            "socket.socket.connect", side_effect=AssertionError("No network"),
        ):
            correct, _ = self.submit("  " + self.case.correct.upper().replace(" ", "  ") + "  ")
            incorrect, _ = self.submit(self.case.incorrect)
        self.assertIn(self.case.success, correct.feedback.text)
        self.assertIn(self.case.correction, incorrect.feedback.text)
        self.assertNotEqual(correct.feedback.text, incorrect.feedback.text)

    @override_settings(AI_MODE="demo", GEMINI_API_KEY="")
    def test_all_24_demo_cases_have_distinct_correct_and_incorrect_feedback(self):
        keys = set()
        for code, topics in DEMO_EXERCISES.items():
            course, _ = Course.objects.get_or_create(code=code, defaults={"name": code})
            Enrollment.objects.get_or_create(student=self.student, course=course)
            for name, (key, statement) in topics.items():
                topic, _ = Topic.objects.get_or_create(course=course, name=name)
                exercise = PracticeExercise.objects.create(
                    student=self.student, course=course, topic=topic,
                    statement=statement, demo_key=key, mode="demo",
                )
                case = demo_case(exercise)
                self.assertIsNotNone(case)
                correct, _ = self.submit(case.correct, exercise_id=exercise.pk)
                incorrect, _ = self.submit(case.incorrect, exercise_id=exercise.pk)
                self.assertIn(case.success, correct.feedback.text)
                self.assertIn(case.correction, incorrect.feedback.text)
                self.assertNotEqual(correct.feedback.text, incorrect.feedback.text)
                keys.add(key)
        self.assertEqual(keys, set(DEMO_FEEDBACK))
        self.assertEqual(len(keys), 24)

    @override_settings(AI_MODE="demo")
    def test_unknown_demo_response_is_preserved_without_invented_feedback(self):
        answer, notice = self.submit(self.case.correct + " Esta frase cambia la respuesta.")
        self.assertTrue(ExerciseAnswer.objects.filter(pk=answer.pk).exists())
        self.assertFalse(ExerciseFeedback.objects.filter(answer=answer).exists())
        self.assertIn("No hay retroalimentación grabada", notice)

    @override_settings(AI_MODE="demo")
    def test_demo_requires_exact_exercise_and_never_evaluates_real_exercises(self):
        for change in ({"statement": "Otro enunciado"}, {"mode": "real"}, {"demo_key": "unknown"}):
            with self.subTest(change=change):
                original = {"statement": self.exercise.statement, "mode": "demo", "demo_key": self.exercise.demo_key}
                PracticeExercise.objects.filter(pk=self.exercise.pk).update(**change)
                answer, _ = self.submit()
                self.assertFalse(ExerciseFeedback.objects.filter(answer=answer).exists())
                PracticeExercise.objects.filter(pk=self.exercise.pk).update(**original)

    @override_settings(AI_MODE="real")
    def test_connection_failure_uses_demo_and_informs_ca8(self):
        with patch.object(GeminiFeedbackProvider, "evaluate", side_effect=TutorUnavailableError("Sin conexión")):
            answer, notice = self.submit()
        self.assertEqual(answer.feedback.source, "demo")
        self.assertIn("modo demo", notice)

    @override_settings(AI_MODE="real")
    def test_connection_failure_without_demo_case_preserves_answer_ca8(self):
        with patch.object(GeminiFeedbackProvider, "evaluate", side_effect=TutorUnavailableError("Sin conexión")):
            answer, notice = self.submit("Respuesta sin caso grabado")
        self.assertFalse(ExerciseFeedback.objects.filter(answer=answer).exists())
        self.assertTrue(ExerciseAnswer.objects.filter(pk=answer.pk).exists())
        self.assertIn("se intentó el modo demo", notice)

    @override_settings(AI_MODE="real", GEMINI_API_KEY="")
    def test_missing_key_falls_back_without_constructing_client(self):
        with patch("tutor.providers._create_gemini_client") as factory:
            answer, notice = self.submit()
            factory.assert_not_called()
        self.assertEqual(answer.feedback.source, "demo")
        self.assertIn("modo demo", notice)

    @override_settings(AI_MODE="real")
    def test_shared_transport_errors_fall_back_ca8(self):
        failures = (
            errors.ClientError(429, {"error": {"message": "quota"}}),
            errors.ServerError(504, {"error": {"message": "timeout"}}),
            TimeoutError(), httpx2.ConnectError("offline"),
        )
        for failure in failures:
            with self.subTest(error=type(failure).__name__), patch("tutor.providers._create_gemini_client") as factory:
                client = factory.return_value.__enter__.return_value
                generate = AsyncMock(side_effect=failure)
                client.aio.__aenter__.return_value.models.generate_content = generate
                answer, notice = self.submit()
                self.assertEqual(answer.feedback.source, "demo")
                self.assertIn("modo demo", notice)
                self.assertEqual(generate.await_count, 1)
                self.assertEqual(factory.call_args.kwargs["max_attempts"], 1)
                self.assertEqual(factory.call_args.kwargs["total_timeout_ms"], 60000)

    @override_settings(AI_MODE="real")
    def test_invalid_outputs_do_not_lose_answers_ca9(self):
        outputs = (
            None, "", "not JSON", "null", "[]", "{}", "x" * 12001,
            self.raw(assessment=" "), self.raw(guidance=7), self.raw(guidance="x" * 4001),
            self.raw(assessment='<script>alert("test")</script>'),
            json.dumps({"assessment": "Texto sin orientación"}),
        )
        for raw in outputs:
            with self.subTest(raw=str(raw)[:60]), patch.object(GeminiFeedbackProvider, "evaluate", return_value=raw), patch(
                "tutor.feedback.recorded_feedback",
            ) as demo:
                answer, notice = self.submit()
                self.assertTrue(ExerciseAnswer.objects.filter(pk=answer.pk).exists())
                self.assertFalse(ExerciseFeedback.objects.filter(answer=answer).exists())
                self.assertIn("Su respuesta se conservó", notice)
                demo.assert_not_called()

    @override_settings(AI_MODE="real")
    def test_formal_feedback_without_literal_usted_and_extra_metadata_is_valid(self):
        raw = self.raw(assessment="Identifica las etapas del ciclo de integración.", metadata={"unused": True})
        with patch.object(GeminiFeedbackProvider, "evaluate", return_value=raw):
            answer, _ = self.submit()
        self.assertIn("Identifica las etapas", answer.feedback.text)

    @override_settings(AI_MODE="real")
    def test_revoked_enrollment_during_provider_call_blocks_feedback(self):
        def revoke(**kwargs):
            Enrollment.objects.filter(student=self.student).delete()
            return self.raw()
        with patch.object(GeminiFeedbackProvider, "evaluate", side_effect=revoke):
            with self.assertRaises(PermissionDenied):
                self.submit()
        self.assertEqual(ExerciseAnswer.objects.count(), 1)
        self.assertFalse(ExerciseFeedback.objects.exists())

    @override_settings(AI_MODE="real")
    def test_real_transport_uses_feedback_instructions_and_no_foreign_context(self):
        with patch("tutor.providers._create_gemini_client") as factory:
            client = factory.return_value.__enter__.return_value
            generate = AsyncMock(return_value=SimpleNamespace(text=self.raw()))
            client.aio.__aenter__.return_value.models.generate_content = generate
            self.submit()
        call = generate.call_args.kwargs
        self.assertIn("en español con trato de usted", call["config"]["system_instruction"])
        instructions = call["config"]["system_instruction"]
        self.assertIn("Evalúe solo los requisitos explícitos del enunciado", instructions)
        self.assertIn("No exija técnicas avanzadas ni precisión profesional", instructions)
        self.assertIn("sugerencias opcionales, no como requisitos incumplidos", instructions)
        self.assertIn("La nota vigente orienta el apoyo, no demuestra errores", instructions)
        payload = json.loads(call["contents"])
        question = json.loads(payload["pregunta"])
        self.assertEqual(question["enunciado"], self.exercise.statement)
        self.assertEqual(question["respuesta_estudiante"], self.case.correct)
        self.assertEqual(payload["datos_academicos"]["temas_y_notas"][0]["grade"], 25)
        self.assertNotIn(self.other_user.username, call["contents"])
        self.assertNotIn(str(self.student.pk), question)

    @override_settings(AI_MODE="demo")
    def test_redirect_and_get_do_not_resubmit_or_call_provider(self):
        response = self.client.post(self.url, {"content": self.case.correct}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Retroalimentación grabada del modo demo")
        self.assertContains(response, self.course.name)
        with patch("tutor.feedback._request_feedback") as provider:
            self.client.get(response.redirect_chain[-1][0])
            self.client.get(self.url)
            provider.assert_not_called()
        self.assertEqual(ExerciseAnswer.objects.count(), 1)

    @override_settings(AI_MODE="demo")
    def test_no_feedback_is_visible_and_answer_is_preserved_in_ui(self):
        response = self.client.post(self.url, {"content": "Sin caso grabado"}, follow=True)
        self.assertContains(response, "Su respuesta se conservó")
        self.assertContains(response, "Sin caso grabado")
        self.assertContains(response, "no se obtuvo retroalimentación válida")

    @override_settings(AI_MODE="real")
    def test_content_is_escaped_and_official_grades_do_not_change_ca10(self):
        before = list(Grade.objects.order_by("pk").values_list("pk", "value"))
        content = '<script>alert("student")</script>'
        with patch.object(GeminiFeedbackProvider, "evaluate", return_value=self.raw()):
            answer, _ = self.submit(content)
        page = self.client.get(reverse("exercise_answer_result", args=[answer.pk]))
        self.assertNotContains(page, content)
        self.assertContains(page, "&lt;script&gt;")
        answer.feedback.text = '<img src=x onerror="alert(1)">'
        answer.feedback.save(update_fields=["text"])
        page = self.client.get(reverse("exercise_answer_result", args=[answer.pk]))
        self.assertNotContains(page, '<img src=x')
        self.assertContains(page, "&lt;img")
        self.assertEqual(list(Grade.objects.order_by("pk").values_list("pk", "value")), before)
