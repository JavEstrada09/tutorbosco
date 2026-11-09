from dataclasses import dataclass
from typing import Protocol

from tutor.demo_responses import DEMO_RESPONSES, normalize_demo_question


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


def _create_gemini_client(api_key):
    # El SDK se importa solo cuando el modo real necesita hacer una llamada.
    from google import genai

    return genai.Client(api_key=api_key)


class GeminiTutorProvider:
    def __init__(self, *, api_key: str, model: str):
        if not api_key:
            raise TutorConfigurationError(
                "El tutor real no está configurado. Active el modo demo."
            )
        if not model:
            raise TutorConfigurationError(
                "El modelo del tutor no está configurado. Active el modo demo."
            )
        self.api_key = api_key
        self.model = model

    def answer(self, *, question: str, context: TutorContext) -> str:
        prompt = (
            "Responda en español como tutor académico. Diríjase al estudiante "
            "con el trato de usted, mencione explícitamente el curso y devuelva "
            "solo texto, sin HTML.\n"
            f"Pregunta: {question}\n"
            f"Carrera: {context.career}\n"
            f"Curso: {context.course_name}"
        )
        try:
            client = _create_gemini_client(self.api_key)
            response = client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            return response.text
        except Exception as error:
            raise TutorUnavailableError(
                "No fue posible consultar el tutor real. Active el modo demo."
            ) from error
