from django.urls import path

from academics.views import student_home, student_profile, teacher_course_grades


urlpatterns = [
    path("", student_home, name="student_home"),
    path("perfil/", student_profile, name="student_profile"),
    path(
        "docente/cursos/<str:course_code>/notas/",
        teacher_course_grades,
        name="teacher_course_grades",
    ),
]
