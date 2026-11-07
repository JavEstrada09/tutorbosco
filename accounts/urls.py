from django.urls import path

from accounts.views import PostOnlyLogoutView, StudentLoginView


urlpatterns = [
    path("acceso/", StudentLoginView.as_view(), name="login"),
    path("salir/", PostOnlyLogoutView.as_view(), name="logout"),
]
