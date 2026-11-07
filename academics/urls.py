from django.urls import path

from academics.views import student_home


urlpatterns = [
    path("", student_home, name="student_home"),
]
