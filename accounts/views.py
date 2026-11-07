from django.contrib.auth.views import LoginView, LogoutView

from accounts.forms import SpanishAuthenticationForm


class StudentLoginView(LoginView):
    authentication_form = SpanishAuthenticationForm
    template_name = "registration/login.html"
    redirect_authenticated_user = True


class PostOnlyLogoutView(LogoutView):
    http_method_names = ["post", "options"]
