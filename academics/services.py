from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

from django.conf import settings

from academics.models import (
    Course,
    Enrollment,
    Grade,
    StudentProfile,
    TeachingAssignment,
    Topic,
)

AVERAGE_PRECISION = Decimal("0.01")


@dataclass(frozen=True)
class TopicGrade:
    topic: Topic
    value: int | None


@dataclass(frozen=True)
class CourseSummary:
    course: Course
    topics: tuple[TopicGrade, ...]
    average: Decimal | None


def calculate_average(values):
    """Devuelve el promedio simple de las notas registradas o None.

    Es la única función de promedio del proyecto (D-004, AGENTS.md §9).
    Los valores None representan temas sin nota y no entran al promedio
    (D-003). Si no queda ninguna nota, devuelve None.

    El resultado se redondea a dos decimales con ROUND_HALF_UP. D-004 no
    fija el modo de redondeo; la elección es del plan de S-003.
    """
    grades = [value for value in values if value is not None]
    if not grades:
        return None
    average = Decimal(sum(grades)) / Decimal(len(grades))
    return average.quantize(AVERAGE_PRECISION, rounding=ROUND_HALF_UP)


def get_course_summaries(student_profile):
    """Arma, para cada curso inscrito, sus temas con la nota vigente y el promedio.

    Recibe solo el perfil del estudiante autenticado. Consulta la base en
    cada llamada, sin caché, para reflejar las notas vigentes. Los cursos se
    ordenan por nombre y los temas por orden de creación. Un tema sin nota
    tiene value None.
    """
    courses = [
        enrollment.course
        for enrollment in Enrollment.objects.filter(student=student_profile)
        .select_related("course")
        .order_by("course__name", "course__code")
    ]
    course_ids = [course.pk for course in courses]

    topics_by_course = {course_id: [] for course_id in course_ids}
    for topic in Topic.objects.filter(course_id__in=course_ids).order_by("pk"):
        topics_by_course[topic.course_id].append(topic)

    grade_by_topic = dict(
        Grade.objects.filter(
            student=student_profile,
            topic__course_id__in=course_ids,
        ).values_list("topic_id", "value")
    )

    summaries = []
    for course in courses:
        topic_grades = tuple(
            TopicGrade(topic=topic, value=grade_by_topic.get(topic.pk))
            for topic in topics_by_course[course.pk]
        )
        summaries.append(
            CourseSummary(
                course=course,
                topics=topic_grades,
                average=calculate_average(
                    topic_grade.value for topic_grade in topic_grades
                ),
            )
        )
    return summaries


def is_weak(value):
    """Indica si una nota corresponde a un tema débil.

    Un tema es débil cuando su nota es estrictamente menor que
    WEAK_TOPIC_THRESHOLD (D-002). Un tema sin nota nunca es débil
    (D-003). Es la única función de tema débil del proyecto
    (AGENTS.md §9); S-007 la reutilizará.
    """
    if value is None:
        return False
    return value < settings.WEAK_TOPIC_THRESHOLD


def get_weak_topics(topic_grades):
    """Devuelve los temas débiles de una secuencia de TopicGrade."""
    return tuple(item.topic for item in topic_grades if is_weak(item.value))


@dataclass(frozen=True)
class StudentPanelRow:
    student: StudentProfile
    average: Decimal | None
    weak_topics: tuple[Topic, ...]


@dataclass(frozen=True)
class TopicWeakCount:
    topic: Topic
    weak_count: int


@dataclass(frozen=True)
class CoursePanel:
    course: Course
    rows: tuple[StudentPanelRow, ...]
    topic_weak_counts: tuple[TopicWeakCount, ...]


def get_taught_courses(teacher_profile):
    """Devuelve los cursos que imparte el docente, ordenados por nombre."""
    return [
        assignment.course
        for assignment in TeachingAssignment.objects.filter(teacher=teacher_profile)
        .select_related("course")
        .order_by("course__name", "course__code")
    ]


def get_course_panel(course):
    """Arma el panel de un curso: promedio y temas débiles por estudiante
    y el conteo de estudiantes con cada tema débil.

    Incluye únicamente a los estudiantes inscritos en el curso. Consulta
    la base en cada llamada, sin caché, para reflejar las notas vigentes.
    Los estudiantes quedan ordenados por nombre y los temas por orden de
    creación.
    """
    students = [
        enrollment.student
        for enrollment in Enrollment.objects.filter(course=course)
        .select_related("student__user")
        .order_by(
            "student__user__first_name",
            "student__user__last_name",
            "student__user__username",
        )
    ]
    topics = list(Topic.objects.filter(course=course).order_by("pk"))

    grade_by_student_topic = {
        (student_id, topic_id): value
        for student_id, topic_id, value in Grade.objects.filter(
            student__in=students,
            topic__in=topics,
        ).values_list("student_id", "topic_id", "value")
    }

    rows = []
    weak_count_by_topic = {topic.pk: 0 for topic in topics}
    for student in students:
        topic_grades = tuple(
            TopicGrade(
                topic=topic,
                value=grade_by_student_topic.get((student.pk, topic.pk)),
            )
            for topic in topics
        )
        weak_topics = get_weak_topics(topic_grades)
        for topic in weak_topics:
            weak_count_by_topic[topic.pk] += 1
        rows.append(
            StudentPanelRow(
                student=student,
                average=calculate_average(
                    topic_grade.value for topic_grade in topic_grades
                ),
                weak_topics=weak_topics,
            )
        )

    return CoursePanel(
        course=course,
        rows=tuple(rows),
        topic_weak_counts=tuple(
            TopicWeakCount(topic=topic, weak_count=weak_count_by_topic[topic.pk])
            for topic in topics
        ),
    )


def get_student_panel_row(course, student_profile):
    """Devuelve la fila del panel del curso para un estudiante inscrito.

    Devuelve None si el estudiante no está inscrito en el curso.
    """
    for row in get_course_panel(course).rows:
        if row.student.pk == student_profile.pk:
            return row
    return None
