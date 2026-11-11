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


class TutorActionForm(forms.Form):
    course = forms.CharField(max_length=20, widget=forms.HiddenInput)
    revision = forms.IntegerField(min_value=0, widget=forms.HiddenInput)
    action = forms.ChoiceField(
        choices=(("ask", "ask"), ("new", "new"), ("continue_demo", "continue_demo")),
        widget=forms.HiddenInput,
    )


class ExerciseAnswerForm(forms.Form):
    content = forms.CharField(
        label="Su respuesta", max_length=4000, strip=True,
        error_messages={
            "required": "Escriba su respuesta antes de enviarla.",
            "max_length": "Su respuesta no puede superar 4000 caracteres.",
        },
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 6}),
    )
