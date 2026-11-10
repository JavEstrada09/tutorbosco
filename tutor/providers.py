import asyncio
import logging
from dataclasses import dataclass
from typing import Protocol

from asgiref.sync import async_to_sync

from tutor.demo_responses import DEMO_RESPONSES, normalize_demo_question


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class TutorContext:
    career: str
    course_name: str


class TutorProvider(Protocol):
    def answer(self, *, question: str, context: TutorContext) -> str: ...


class TutorError(Exception):
    """Error del tutor cuyo mensaje es seguro para mostrar en la interfaz."""


class TutorConfigurationError(TutorError):
    pass


class TutorUnavailableError(TutorError):
    pass


class InvalidTutorResponseError(TutorError):
    pass


class DemoTutorProvider:
    def answer(self, *, question: str, context: TutorContext) -> str:
        response = DEMO_RESPONSES.get(normalize_demo_question(question))
        if response is None:
            raise TutorUnavailableError(
                "Esta pregunta no está disponible en el modo demo. "
                "Use la pregunta de ejemplo."
            )
        return response


def _create_gemini_client(api_key, *, total_timeout_ms, max_attempts):
    # El SDK se importa solo cuando el modo real necesita hacer una llamada.
    from google import genai
    from google.genai import types

    return genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            timeout=total_timeout_ms,
            retry_options=types.HttpRetryOptions(attempts=max_attempts),
        ),
    )


class GeminiTutorProvider:
    def __init__(
        self,
        *,
        api_key: str,
        model: str,
        total_timeout_ms: int,
        max_attempts: int,
    ):
        if not isinstance(api_key, str) or not api_key.strip():
            raise TutorConfigurationError(
                "El tutor real no está configurado. Puede continuar en modo demo."
            )
        if not isinstance(model, str) or not model.strip():
            raise TutorConfigurationError(
                "El modelo del tutor no está configurado. "
                "Puede continuar en modo demo."
            )
        if not isinstance(total_timeout_ms, int) or total_timeout_ms <= 0:
            raise TutorConfigurationError(
                "El límite total de espera del tutor no es válido. "
                "Puede continuar en modo demo."
            )
        if not isinstance(max_attempts, int) or max_attempts != 1:
            raise TutorConfigurationError(
                "La cantidad de intentos del tutor no es válida. "
                "Puede continuar en modo demo."
            )
        self.api_key = api_key.strip()
        self.model = model.strip()
        self.total_timeout_ms = total_timeout_ms
        self.max_attempts = max_attempts

    async def _generate_response(self, client, prompt):
        async with client.aio as async_client:
            async with asyncio.timeout(self.total_timeout_ms / 1000):
                return await async_client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )

    def answer(self, *, question: str, context: TutorContext) -> str:
        import httpx2
        from google.genai import errors

        prompt = (
            "Responda en español como tutor académico. Diríjase al estudiante "
            "con el trato de usted, mencione explícitamente el curso y devuelva "
            "solo texto, sin HTML.\n"
            f"Pregunta: {question}\n"
            f"Carrera: {context.career}\n"
            f"Curso: {context.course_name}"
        )
        try:
            with _create_gemini_client(
                self.api_key,
                total_timeout_ms=self.total_timeout_ms,
                max_attempts=self.max_attempts,
            ) as client:
                response = async_to_sync(self._generate_response)(client, prompt)
                return response.text
        except errors.APIError as error:
            if error.code == 429:
                raise TutorUnavailableError(
                    "El tutor real alcanzó su límite de uso. "
                    "Puede continuar en modo demo."
                ) from error
            if error.code == 504:
                raise TutorUnavailableError(
                    "El tutor real tardó demasiado en responder. "
                    "Puede continuar en modo demo."
                ) from error
            raise TutorUnavailableError(
                "El proveedor del tutor real no pudo responder. "
                "Puede continuar en modo demo."
            ) from error
        except (TimeoutError, httpx2.TimeoutException) as error:
            raise TutorUnavailableError(
                "El tutor real tardó demasiado en responder. "
                "Puede continuar en modo demo."
            ) from error
        except httpx2.RequestError as error:
            raise TutorUnavailableError(
                "No fue posible conectar con el tutor real. "
                "Puede continuar en modo demo."
            ) from error
        except Exception as error:
            logger.error(
                "Fallo inesperado del proveedor Gemini (%s).",
                type(error).__name__,
            )
            raise TutorUnavailableError(
                "No fue posible consultar el tutor real. "
                "Puede continuar en modo demo."
            ) from error
