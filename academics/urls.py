from django.urls import path

from academics.views import student_home, student_profile


urlpatterns = [
    path("", student_home, name="student_home"),
    path("perfil/", student_profile, name="student_profile"),
]
