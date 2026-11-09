import re
from dataclasses import dataclass

from django.conf import settings

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
    return settings.AI_MODE.strip().lower()


def _select_provider():
    mode = get_tutor_mode()
    if mode == "demo":
        return DemoTutorProvider(), mode
    if mode == "real":
        return (
            GeminiTutorProvider(
                api_key=settings.GEMINI_API_KEY,
                model=settings.AI_MODEL,
            ),
            mode,
        )
    raise TutorConfigurationError(
        "El modo del tutor no es válido. Configure AI_MODE como demo o real."
    )


def _validate_response(response, context):
    if not isinstance(response, str) or not response.strip():
        raise InvalidTutorResponseError(
            "El tutor no devolvió una respuesta válida. Inténtelo de nuevo."
        )
    text = response.strip()
    if len(text) > 10_000:
        raise InvalidTutorResponseError(
            "La respuesta del tutor es demasiado extensa. Inténtelo de nuevo."
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
            "La respuesta del tutor no cumple el formato esperado. "
            "Inténtelo de nuevo."
        )
    return text


def ask_tutor(*, question: str, career: str, course_name: str) -> TutorReply:
    context = TutorContext(career=career, course_name=course_name)
    provider, mode = _select_provider()
    response = provider.answer(question=question, context=context)
    return TutorReply(text=_validate_response(response, context), mode=mode)
