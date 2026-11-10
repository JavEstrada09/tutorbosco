DEMO_QUESTION = "¿Qué es una variable y para qué se usa?"

DEMO_RESPONSE = (
    "En Programación Comercial, una variable es un espacio con nombre que "
    "guarda un valor para utilizarlo durante la ejecución de un programa. "
    "Usted puede usar una variable, por ejemplo, para conservar el precio "
    "de un producto y calcular después el total de una venta."
)


def normalize_demo_question(question):
    return " ".join(question.casefold().split())


DEMO_RESPONSES = {
    normalize_demo_question(DEMO_QUESTION): DEMO_RESPONSE,
}


RECOMMEND_QUESTION = "¿Qué tema debería repasar?"
FOLLOWUP_QUESTION = "¿Me da otro ejemplo?"
PRIVACY_QUESTIONS = (
    "¿Qué notas tiene otro estudiante?",
    "¿Puede mostrarme las calificaciones de otra persona?",
)

# Cada par contiene una explicación inicial y un ejemplo adicional grabados.
PILOT_EXAMPLES = {
    "Git y GitHub avanzado": (
        "Use una rama para preparar un cambio y un pull request para revisarlo antes de fusionarlo.",
        "Si dos ramas editan una misma línea, revise el conflicto, conserve el cambio correcto y ejecute las pruebas antes de confirmar la fusión.",
    ),
    "Código limpio y refactoring": (
        "Extraiga el cálculo del total de una venta a una función con un nombre claro, sin cambiar el resultado.",
        "Si dos pantallas repiten el cálculo del descuento, reúna esa lógica en una función y compruebe que ambas conservan el mismo total.",
    ),
    "Sistemas de información y bases de datos": (
        "Separe clientes y ventas en tablas y relacione cada venta con la clave de su cliente.",
        "Para evitar clientes duplicados, use una clave única y consulte sus ventas mediante esa relación.",
    ),
    "Ingeniería de prompts": (
        "Indique el objetivo, los datos y el formato esperado al pedir una explicación del cálculo de una venta.",
        "Pida una explicación paso a paso con un precio y un descuento concretos, y compruebe el resultado con su propio cálculo.",
    ),
    "El LLM por dentro y su API": (
        "Una API recibe una solicitud y devuelve una respuesta del modelo; su aplicación debe validar esa respuesta antes de mostrarla.",
        "Si la API agota su cuota, muestre un aviso y una alternativa local, sin revelar la clave ni repetir indefinidamente la solicitud.",
    ),
    "Agentes de programación y desarrollo guiado por especificaciones": (
        "Defina primero el comportamiento esperado y sus criterios de aceptación antes de pedir a un agente que programe.",
        "Para un cálculo de descuentos, escriba casos con y sin descuento y revise las pruebas del agente antes de aceptar su cambio.",
    ),
}

RECORDED_TOPIC_RESPONSES = {
    ("PROG-COM", topic, intent): (
        f"En Programación Comercial, usted puede repasar {topic}. {example}"
    )
    for topic, examples in PILOT_EXAMPLES.items()
    for intent, example in zip(("recommendation", "followup"), examples)
}


def recorded_answer(question, context):
    """Selecciona grabaciones; no clasifica solicitudes libres de terceros."""
    normalized = normalize_demo_question(question)
    code = context.course_code or (
        "PROG-COM" if context.course_name == "Programación Comercial" else ""
    )
    if normalized in {normalize_demo_question(item) for item in PRIVACY_QUESTIONS}:
        return (
            f"En {context.course_name}, usted solo puede consultar su propio perfil. "
            "No puedo mostrar ni inventar notas o perfiles de otras personas."
        )
    if code != "PROG-COM":
        return None
    if normalized in DEMO_RESPONSES:
        return DEMO_RESPONSES[normalized]
    if normalized == normalize_demo_question(RECOMMEND_QUESTION):
        if context.academic_status == "no_grades":
            return (
                "En Programación Comercial, usted aún no tiene calificaciones "
                "suficientes para identificar qué necesita reforzar. Puede "
                "solicitar una explicación de un tema del curso."
            )
        if not context.weak_topics:
            return (
                "En Programación Comercial, usted no tiene temas con notas bajo "
                "el umbral. Los temas sin nota no se consideran temas débiles. "
                "Puede solicitar una explicación de un tema del curso."
            )
        return RECORDED_TOPIC_RESPONSES.get((code, context.weak_topics[0], "recommendation"))
    if normalized == normalize_demo_question(FOLLOWUP_QUESTION):
        if not context.turns:
            return None
        last_answer = context.turns[-1]["answer"]
        for topic in PILOT_EXAMPLES:
            if topic in last_answer:
                return RECORDED_TOPIC_RESPONSES[(code, topic, "followup")]
        if "una variable" in last_answer:
            return (
                "En Programación Comercial, usted puede guardar un precio de "
                "Q25 en una variable y multiplicarlo por 3 para obtener Q75."
            )
        return None
    for item in context.academic_snapshot:
        topic = item["topic"]
        if normalized == normalize_demo_question(f"Explíqueme {topic}."):
            return RECORDED_TOPIC_RESPONSES.get((code, topic, "recommendation"))
    return None
