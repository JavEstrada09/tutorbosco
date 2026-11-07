from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField


GENERIC_LOGIN_ERROR = "Las credenciales ingresadas no son válidas."


class SpanishAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label="Usuario",
        widget=forms.TextInput(
            attrs={
                "autocomplete": "username",
                "autofocus": True,
                "class": "form-control",
            }
        ),
    )
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "class": "form-control",
            }
        ),
    )
    error_messages = {
        "invalid_login": GENERIC_LOGIN_ERROR,
        "inactive": GENERIC_LOGIN_ERROR,
    }
