
from django import forms

from academics.models import Enrollment, StudentProfile, Topic


# =====================================================
# S-004: Formulario para crear y modificar temas
# =====================================================

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["name"]
        labels = {
            "name": "Nombre del tema",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 150,
                    "placeholder": "Ingrese el nombre del tema",
                }
            ),
        }

    def __init__(self, *args, course, **kwargs):
        super().__init__(*args, **kwargs)
        self.course = course

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if not name:
            raise forms.ValidationError(
                "El nombre del tema es obligatorio."
            )

        exists = Topic.objects.filter(
            course=self.course,
            name__iexact=name,
        ).exclude(pk=self.instance.pk).exists()

        if exists:
            raise forms.ValidationError(
                "Este tema ya está registrado en el curso."
            )

        return name


# =====================================================
# S-004: Formulario para asignar estudiantes
# =====================================================

class StudentEnrollmentForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=StudentProfile.objects.none(),
        label="Estudiante",
        empty_label="Seleccione un estudiante",
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
    )

    def __init__(self, *args, course, **kwargs):
        super().__init__(*args, **kwargs)
        self.course = course

        self.fields["student"].queryset = (
            StudentProfile.objects
            .select_related("user")
            .order_by("student_id")
        )

    def clean_student(self):
        student = self.cleaned_data["student"]

        already_enrolled = Enrollment.objects.filter(
            student=student,
            course=self.course,
        ).exists()

        if already_enrolled:
            raise forms.ValidationError(
                "Este estudiante ya está asignado a este curso."
            )

        return student
