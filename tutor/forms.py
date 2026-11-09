from django import forms


class TutorQuestionForm(forms.Form):
    question = forms.CharField(
        label="Su pregunta",
        min_length=3,
        max_length=500,
        strip=True,
        error_messages={
            "required": "Escriba una pregunta para el tutor.",
            "min_length": "La pregunta debe tener al menos 3 caracteres.",
            "max_length": "La pregunta no puede superar 500 caracteres.",
        },
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Escriba su pregunta sobre el curso.",
            }
        ),
    )
