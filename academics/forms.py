from django import forms

from academics.services import GRADE_MAX_VALUE, GRADE_MIN_VALUE

GRADE_RANGE_ERROR = (
    f"La nota debe estar entre {GRADE_MIN_VALUE} y {GRADE_MAX_VALUE}."
)


class GradeForm(forms.Form):
    """Valida el formato de la nota que envía el docente.

    Las opciones de Estudiante y Tema salen de la planilla del curso y solo
    sirven para mostrarlas. Que el estudiante y el tema pertenezcan al curso
    lo decide record_grade en el servidor (CA-8), no este formulario.
    """

    student = forms.IntegerField(
        label="Estudiante",
        error_messages={
            "required": "Seleccione un estudiante.",
            "invalid": "Seleccione un estudiante.",
        },
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    topic = forms.IntegerField(
        label="Tema",
        error_messages={
            "required": "Seleccione un tema.",
            "invalid": "Seleccione un tema.",
        },
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    value = forms.IntegerField(
        label="Nota",
        min_value=GRADE_MIN_VALUE,
        max_value=GRADE_MAX_VALUE,
        error_messages={
            "required": "Ingrese una nota.",
            "invalid": "La nota debe ser un número entero.",
            "min_value": GRADE_RANGE_ERROR,
            "max_value": GRADE_RANGE_ERROR,
        },
        widget=forms.NumberInput(attrs={"class": "form-control", "step": 1}),
    )

    def __init__(self, *args, grade_sheet, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["student"].widget.choices = [("", "Seleccione un estudiante")] + [
            (
                row.student.pk,
                f"{row.student.student_id} – {display_name(row.student.user)}",
            )
            for row in grade_sheet.rows
        ]
        self.fields["topic"].widget.choices = [("", "Seleccione un tema")] + [
            (topic.pk, topic.name) for topic in grade_sheet.topics
        ]


def display_name(user):
    return user.get_full_name() or user.get_username()
