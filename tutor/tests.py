import asyncio
import secrets
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import httpx2
from django.contrib.auth import get_user_model
from django.test import Client, SimpleTestCase, TestCase, override_settings
from django.urls import reverse
from google.genai import errors as genai_errors

from academics.models import Course, Enrollment, StudentProfile
from tutor.demo_responses import DEMO_QUESTION, DEMO_RESPONSE
from tutor.forms import TutorQuestionForm
from tutor.providers import (
    InvalidTutorResponseError,
    TutorConfigurationError,
    TutorUnavailableError,
    _create_gemini_client,
)
from tutor.services import TutorReply, ask_tutor


def mock_gemini_generation(create_client):
    client = create_client.return_value.__enter__.return_value
    async_client = client.aio.__aenter__.return_value
    async_client.models.generate_content = AsyncMock()
    return async_client.models.generate_content


class TutorQuestionFormTests(SimpleTestCase):
    def test_question_is_required_and_rejects_only_whitespace(self):
        for value in ("", "   "):
            with self.subTest(value=value):
                form = TutorQuestionForm({"question": value})
                self.assertFalse(form.is_valid())
                self.assertIn(
                    "Escriba una pregunta para el tutor.",
                    form.errors["question"],
                )

    def test_question_is_trimmed_and_limited_to_500_characters(self):
        form = TutorQuestionForm({"question": "  ¿Qué es una variable?  "})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["question"], "¿Qué es una variable?")

        long_form = TutorQuestionForm({"question": "a" * 501})
        self.assertFalse(long_form.is_valid())
        self.assertIn(
            "La pregunta no puede superar 500 caracteres.",
            long_form.errors["question"],
        )


class TutorServiceTests(SimpleTestCase):
    @patch("google.genai.Client")
    def test_real_client_sets_network_timeout_and_no_retries(self, client_class):
        client = _create_gemini_client(
            "clave-sintetica",
            total_timeout_ms=60_000,
            max_attempts=1,
        )

        self.assertEqual(client, client_class.return_value)
        call = client_class.call_args.kwargs
        self.assertEqual(call["api_key"], "clave-sintetica")
        self.assertEqual(call["http_options"].timeout, 60_000)
        retry_options = call["http_options"].retry_options
        self.assertEqual(retry_options.attempts, 1)

    @override_settings(AI_MODE="demo", GEMINI_API_KEY="")
    @patch("socket.create_connection")
    @patch("tutor.providers._create_gemini_client")
    def test_demo_returns_recorded_response_without_network_or_gemini(
        self,
        client,
        create_connection,
    ):
        reply = ask_tutor(
            question=DEMO_QUESTION,
            career="Ingeniería en Sistemas",
            course_name="Programación Comercial",
        )

        self.assertEqual(reply, TutorReply(text=DEMO_RESPONSE, mode="demo"))
        client.assert_not_called()
        create_connection.assert_not_called()

    @override_settings(AI_MODE="demo", GEMINI_API_KEY="")
    def test_demo_rejects_questions_outside_its_recorded_case(self):
        with self.assertRaisesMessage(
            TutorUnavailableError,
            "Esta pregunta no está disponible en el modo demo.",
        ):
            ask_tutor(
                question="¿Qué es una clase?",
                career="Ingeniería en Sistemas",
                course_name="Programación Comercial",
            )

    @override_settings(
        AI_MODE="real",
        AI_MODEL="modelo-simulado",
        GEMINI_API_KEY="clave-sintetica",
    )
    @patch("tutor.providers._create_gemini_client")
    def test_real_provider_sends_only_allowed_context(self, create_client):
        generate_content = mock_gemini_generation(create_client)
        generate_content.return_value = SimpleNamespace(
            text=(
                "En Programación Comercial, usted puede usar una variable "
                "para guardar un valor."
            )
        )

        reply = ask_tutor(
            question="¿Qué es una variable?",
            career="Ingeniería en Sistemas",
            course_name="Programación Comercial",
        )

        self.assertEqual(reply.mode, "real")
        create_client.assert_called_once_with(
            "clave-sintetica",
            total_timeout_ms=60_000,
            max_attempts=1,
        )
        call = generate_content.call_args.kwargs
        self.assertEqual(call["model"], "modelo-simulado")
        self.assertIn("Pregunta: ¿Qué es una variable?", call["contents"])
        self.assertIn("Carrera: Ingeniería en Sistemas", call["contents"])
        self.assertIn("Curso: Programación Comercial", call["contents"])
        self.assertNotIn("carné", call["contents"].casefold())
        self.assertNotIn("contraseña", call["contents"].casefold())

    @override_settings(AI_MODE="real", AI_MODEL="modelo", GEMINI_API_KEY="")
    @patch("tutor.providers._create_gemini_client")
    def test_real_mode_requires_key_before_initializing_client(self, client):
        with self.assertRaisesMessage(
            TutorConfigurationError,
            "El tutor real no está configurado.",
        ):
            ask_tutor(
                question=DEMO_QUESTION,
                career="Ingeniería en Sistemas",
                course_name="Programación Comercial",
            )
        client.assert_not_called()

    @override_settings(AI_MODE="otro")
    def test_invalid_mode_is_rejected(self):
        with self.assertRaisesMessage(
            TutorConfigurationError,
            "El modo del tutor no es válido.",
        ):
            ask_tutor(
                question=DEMO_QUESTION,
                career="Ingeniería en Sistemas",
                course_name="Programación Comercial",
            )

    @override_settings(
        AI_MODE="real",
        AI_MODEL="modelo-simulado",
        GEMINI_API_KEY="clave-sintetica",
    )
    @patch("tutor.providers._create_gemini_client")
    def test_expected_provider_failures_have_safe_specific_messages(
        self,
        create_client,
    ):
        generate_content = mock_gemini_generation(create_client)
        request = httpx2.Request("POST", "https://example.invalid")
        cases = (
            (
                httpx2.ConnectError("detalle-interno", request=request),
                "No fue posible conectar con el tutor real.",
            ),
            (
                genai_errors.ServerError(
                    504,
                    {"error": {"message": "detalle-interno", "status": "TIEMPO"}},
                ),
                "El tutor real tardó demasiado en responder.",
            ),
        )

        for error, expected_message in cases:
            with self.subTest(error=type(error).__name__):
                generate_content.side_effect = error
                with self.assertRaises(TutorUnavailableError) as raised:
                    ask_tutor(
                        question=DEMO_QUESTION,
                        career="Ingeniería en Sistemas",
                        course_name="Programación Comercial",
                    )
                message = str(raised.exception)
                self.assertIn(expected_message, message)
                self.assertIn("Puede continuar en modo demo.", message)
                self.assertNotIn("clave-secreta", message)
                self.assertNotIn("detalle-interno", message)

    @override_settings(
        AI_MODE="real",
        AI_MODEL="modelo-simulado",
        GEMINI_API_KEY="clave-sintetica",
    )
    @patch("tutor.providers.logger.error")
    @patch("google.genai.Client")
    def test_429_is_not_retried_or_logged(self, client_class, log_error):
        generate_content = mock_gemini_generation(client_class)
        generate_content.side_effect = genai_errors.ClientError(
            429,
            {
                "error": {
                    "message": "detalle-interno-del-proveedor",
                    "status": "RESOURCE_EXHAUSTED",
                }
            },
        )

        with self.assertRaisesMessage(
            TutorUnavailableError,
            "El tutor real alcanzó su límite de uso.",
        ):
            ask_tutor(
                question=DEMO_QUESTION,
                career="Ingeniería en Sistemas",
                course_name="Programación Comercial",
            )

        generate_content.assert_awaited_once()
        http_options = client_class.call_args.kwargs["http_options"]
        self.assertEqual(http_options.timeout, 60_000)
        self.assertEqual(http_options.retry_options.attempts, 1)
        log_error.assert_not_called()

    @override_settings(
        AI_MODE="real",
        AI_MODEL="modelo-simulado",
        GEMINI_API_KEY="clave-sintetica",
        GEMINI_TOTAL_TIMEOUT_MS=20,
    )
    @patch("tutor.providers._create_gemini_client")
    def test_total_timeout_cancels_generation(self, create_client):
        cancelled = False

        async def generate_slowly(**kwargs):
            nonlocal cancelled
            try:
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                cancelled = True
                raise

        generate_content = mock_gemini_generation(create_client)
        generate_content.side_effect = generate_slowly

        with self.assertRaisesMessage(
            TutorUnavailableError,
            "El tutor real tardó demasiado en responder.",
        ):
            ask_tutor(
                question=DEMO_QUESTION,
                career="Ingeniería en Sistemas",
                course_name="Programación Comercial",
            )

        self.assertTrue(cancelled)
        generate_content.assert_awaited_once()

    @override_settings(
        AI_MODE="real",
        AI_MODEL="modelo-simulado",
        GEMINI_API_KEY="clave-sintetica",
        GEMINI_TOTAL_TIMEOUT_MS=0,
    )
    @patch("tutor.providers._create_gemini_client")
    def test_invalid_timeout_is_rejected_before_initializing_client(self, client):
        with self.assertRaisesMessage(
            TutorConfigurationError,
            "El límite total de espera del tutor no es válido.",
        ):
            ask_tutor(
                question=DEMO_QUESTION,
                career="Ingeniería en Sistemas",
                course_name="Programación Comercial",
            )
        client.assert_not_called()

    @override_settings(
        AI_MODE="real",
        AI_MODEL="modelo-simulado",
        GEMINI_API_KEY="clave-sintetica",
    )
    @patch("tutor.providers._create_gemini_client")
    def test_empty_or_nonconforming_real_outputs_are_rejected(self, create_client):
        generate_content = mock_gemini_generation(create_client)

        for response in (
            "",
            "Una respuesta sin el curso ni el trato requerido.",
            (
                "In Programación Comercial, usted should declare a variable "
                "before using it."
            ),
        ):
            with self.subTest(response=response):
                generate_content.return_value = SimpleNamespace(text=response)
                with self.assertRaises(InvalidTutorResponseError):
                    ask_tutor(
                        question=DEMO_QUESTION,
                        career="Ingeniería en Sistemas",
                        course_name="Programación Comercial",
                    )


@override_settings(AI_MODE="demo", GEMINI_API_KEY="")
class TutorViewTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.user = get_user_model().objects.create_user(
            username="estudiante_tutor",
            password=secrets.token_urlsafe(24),
        )
        self.profile = StudentProfile.objects.create(
            user=self.user,
            student_id="2026-00500",
            career="Ingeniería en Sistemas",
            semester=2,
        )
        self.course = Course.objects.create(
            code="PROG-COM",
            name="Programación Comercial",
        )
        self.enrollment = Enrollment.objects.create(
            student=self.profile,
            course=self.course,
        )
        self.client.force_login(self.user)

    def get_csrf_token(self):
        response = self.client.get(reverse("student_home"))
        return response.cookies["csrftoken"].value

    def test_page_shows_demo_label_example_and_question_form(self):
        response = self.client.get(reverse("student_home"))

        self.assertContains(response, "Modo demo")
        self.assertContains(response, DEMO_QUESTION)
        self.assertContains(response, "Su pregunta")
        self.assertContains(response, "Programación Comercial")

    @patch("academics.views.ask_tutor")
    def test_post_without_csrf_is_rejected_before_tutor(self, ask_tutor_mock):
        response = self.client.post(
            reverse("student_home"),
            {"question": DEMO_QUESTION},
        )

        self.assertEqual(response.status_code, 403)
        ask_tutor_mock.assert_not_called()

    @patch("academics.views.ask_tutor")
    def test_authorization_is_rechecked_before_tutor(self, ask_tutor_mock):
        csrf_token = self.get_csrf_token()
        self.enrollment.delete()

        response = self.client.post(
            reverse("student_home"),
            {
                "question": DEMO_QUESTION,
                "csrfmiddlewaretoken": csrf_token,
            },
        )

        self.assertEqual(response.status_code, 403)
        ask_tutor_mock.assert_not_called()

    @override_settings(AI_MODE="real")
    @patch("academics.views.ask_tutor")
    def test_course_selection_checks_enrollment_before_calling_tutor(self, ask_tutor_mock):
        selected = Course.objects.create(code="DES-WEB", name="Desarrollo Web")
        foreign = Course.objects.create(code="BD-APL", name="Bases de Datos Aplicadas")
        Enrollment.objects.create(student=self.profile, course=selected)
        url = reverse("student_home")
        csrf_token = self.get_csrf_token()

        default_page = self.client.get(url)
        self.assertEqual(default_page.context["selected_course"], self.course)
        self.assertContains(default_page, "Desarrollo Web")
        self.assertNotContains(default_page, foreign.name)
        self.assertContains(
            self.client.get(url, {"course": selected.code}),
            "Consulte sobre Desarrollo Web",
        )

        for method in (self.client.get, self.client.post):
            with self.subTest(method=method.__name__):
                response = method(
                    url,
                    {"course": foreign.code, "question": DEMO_QUESTION},
                    HTTP_X_CSRFTOKEN=csrf_token,
                )
                self.assertNotContains(response, foreign.name, status_code=403)
        ask_tutor_mock.assert_not_called()

        response = self.client.post(
            url,
            {"course": selected.code, "question": DEMO_QUESTION},
            HTTP_X_CSRFTOKEN=csrf_token,
        )
        self.assertEqual(response.context["selected_course"], selected)
        ask_tutor_mock.assert_called_once_with(
            question=DEMO_QUESTION,
            career=self.profile.career,
            course_name=selected.name,
            mode=None,
        )

    @patch("tutor.providers._create_gemini_client")
    def test_demo_question_completes_flow_without_gemini(self, client):
        csrf_token = self.get_csrf_token()

        response = self.client.post(
            reverse("student_home"),
            {
                "question": DEMO_QUESTION,
                "csrfmiddlewaretoken": csrf_token,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, DEMO_RESPONSE)
        self.assertContains(response, "Modo demo")
        self.assertContains(response, "Respuesta grabada del modo demo")
        self.assertContains(response, self.profile.career)
        client.assert_not_called()

    @override_settings(
        AI_MODE="real",
        AI_MODEL="modelo-simulado",
        GEMINI_API_KEY="clave-sintetica",
    )
    @patch("tutor.providers._create_gemini_client")
    def test_real_failure_offers_demo_without_exposing_details(self, create_client):
        generate_content = mock_gemini_generation(create_client)
        generate_content.side_effect = genai_errors.ClientError(
            429,
            {"error": {"message": "clave-secreta", "status": "RESOURCE_EXHAUSTED"}},
        )
        csrf_token = self.get_csrf_token()

        response = self.client.post(
            reverse("student_home"),
            {
                "question": "¿Qué es una clase?",
                "csrfmiddlewaretoken": csrf_token,
            },
        )

        self.assertContains(response, "alcanzó su límite de uso")
        self.assertContains(response, "Continuar en modo demo")
        self.assertContains(response, DEMO_QUESTION)
        self.assertNotContains(response, "clave-secreta")
        self.assertNotContains(response, "RESOURCE_EXHAUSTED")

    @override_settings(
        AI_MODE="real",
        AI_MODEL="modelo-simulado",
        GEMINI_API_KEY="clave-sintetica",
    )
    @patch("tutor.providers._create_gemini_client")
    def test_demo_continuation_uses_recorded_question_without_gemini(self, client):
        csrf_token = self.get_csrf_token()

        response = self.client.post(
            reverse("student_home"),
            {
                "continue_in_demo": "1",
                "question": "pregunta manipulada",
                "csrfmiddlewaretoken": csrf_token,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, DEMO_RESPONSE)
        self.assertContains(response, "Respuesta grabada del modo demo")
        client.assert_not_called()

    @patch("academics.views.ask_tutor")
    def test_invalid_question_is_not_sent_to_provider(self, ask_tutor_mock):
        csrf_token = self.get_csrf_token()

        response = self.client.post(
            reverse("student_home"),
            {"question": " ", "csrfmiddlewaretoken": csrf_token},
        )

        self.assertContains(response, "Escriba una pregunta para el tutor.")
        ask_tutor_mock.assert_not_called()

    @patch("academics.views.ask_tutor")
    def test_provider_output_is_rendered_as_plain_text(self, ask_tutor_mock):
        ask_tutor_mock.return_value = TutorReply(
            text=(
                "En Programación Comercial, usted verá texto. "
                "<script>alert('x')</script>"
            ),
            mode="demo",
        )
        csrf_token = self.get_csrf_token()

        response = self.client.post(
            reverse("student_home"),
            {
                "question": DEMO_QUESTION,
                "csrfmiddlewaretoken": csrf_token,
            },
        )

        self.assertNotContains(response, "<script>alert('x')</script>")
        self.assertContains(
            response,
            "&lt;script&gt;alert(&#x27;x&#x27;)&lt;/script&gt;",
        )
