from django.urls import path

from academics.views import (
    role_home,
    student_home,
    student_profile,
    teacher_course_grades,
    teacher_course_panel,
    teacher_panel,
    teacher_student_detail,
)


urlpatterns = [
    path("", student_home, name="student_home"),
    path("perfil/", student_profile, name="student_profile"),
    path("inicio/", role_home, name="role_home"),
    path("docente/panel/", teacher_panel, name="teacher_panel"),
    path(
        "docente/panel/<str:course_code>/",
        teacher_course_panel,
        name="teacher_course_panel",
    ),
    path(
        "docente/panel/<str:course_code>/estudiantes/<int:student_id>/",
        teacher_student_detail,
        name="teacher_student_detail",
    ),
    path(
        "docente/cursos/<str:course_code>/notas/",
        teacher_course_grades,
        name="teacher_course_grades",
    ),
]
