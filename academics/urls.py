from django.urls import path

from academics.views import (
    role_home,
    student_home,
    student_profile,
    teacher_course_grades,
    teacher_course_panel,
    teacher_course_students,
    teacher_course_topics,
    teacher_courses,
    teacher_panel,
    teacher_student_detail,
)

urlpatterns = [
    # S-001: Inicio del estudiante
    path("", student_home, name="student_home"),

    # S-003: Perfil académico del estudiante
    path("perfil/", student_profile, name="student_profile"),

    # S-004: Listado de cursos del docente
    path(
        "docente/cursos/",
        teacher_courses,
        name="teacher_courses",
    ),

    # S-004: Administración de temas
    path(
        "docente/cursos/<str:course_code>/temas/",
        teacher_course_topics,
        name="teacher_course_topics",
    ),

    # S-004: Asignación de estudiantes
    path(
        "docente/cursos/<str:course_code>/estudiantes/",
        teacher_course_students,
        name="teacher_course_students",
    ),
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
