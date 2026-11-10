from decimal import ROUND_HALF_UP, Decimal

AVERAGE_PRECISION = Decimal("0.01")


def calculate_average(values):
    """Devuelve el promedio simple de las notas registradas o None.

    Es la única función de promedio del proyecto (D-004, AGENTS.md §9).
    Los valores None representan temas sin nota y no entran al promedio
    (D-003). Si no queda ninguna nota, devuelve None.

    El resultado se redondea a dos decimales con ROUND_HALF_UP. D-004 no
    fija el modo de redondeo; la elección es del plan de S-003.
    """
    grades = [value for value in values if value is not None]
    if not grades:
        return None
    average = Decimal(sum(grades)) / Decimal(len(grades))
    return average.quantize(AVERAGE_PRECISION, rounding=ROUND_HALF_UP)
