from django.urls import path

from academics.views import (
    student_home,
    student_profile,
    teacher_courses,
    teacher_course_topics,
    teacher_course_students,
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
]
