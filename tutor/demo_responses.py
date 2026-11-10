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
