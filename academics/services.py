from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

from django.db import transaction

from academics.models import (
    Course,
    Enrollment,
    Grade,
    StudentProfile,
    TeachingAssignment,
    Topic,
)

AVERAGE_PRECISION = Decimal("0.01")
GRADE_MIN_VALUE = 0
GRADE_MAX_VALUE = 100
NOT_TEACHING_MESSAGE = "Usted no imparte este curso. La nota no se guardó."


class GradeRegistrationError(Exception):
    """Rechazo de una nota; el mensaje está en español para la persona usuaria."""


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


@dataclass(frozen=True)
class StudentGradeRow:
    student: StudentProfile
    grades: tuple[int | None, ...]


@dataclass(frozen=True)
class GradeSheet:
    course: Course
    topics: tuple[Topic, ...]
    rows: tuple[StudentGradeRow, ...]


def get_course_grade_sheet(course):
    """Arma la planilla de notas de un curso para la pantalla del docente.

    Incluye solo a los estudiantes inscritos en el curso, ordenados por
    carné, y solo los temas del curso, por orden de creación. En cada fila,
    grades sigue el orden de topics y un tema sin nota tiene None (D-003).
    Usa tres consultas sin importar el tamaño del curso. No comprueba
    permisos: la vista debe obtener el curso con get_taught_course.
    """
    enrollments = (
        Enrollment.objects.filter(course=course)
        .select_related("student__user")
        .order_by("student__student_id")
    )
    topics = tuple(Topic.objects.filter(course=course).order_by("pk"))
    grade_by_student_topic = {
        (student_id, topic_id): value
        for student_id, topic_id, value in Grade.objects.filter(
            topic__course=course
        ).values_list("student_id", "topic_id", "value")
    }

    rows = tuple(
        StudentGradeRow(
            student=enrollment.student,
            grades=tuple(
                grade_by_student_topic.get((enrollment.student_id, topic.pk))
                for topic in topics
            ),
        )
        for enrollment in enrollments
    )
    return GradeSheet(course=course, topics=topics, rows=rows)


def get_taught_course(user, course_code):
    """Devuelve el curso con ese código si el usuario lo imparte, o None.

    Devuelve None si la cuenta no tiene TeacherProfile, si no tiene una
    TeachingAssignment del curso o si el curso no existe. Las vistas de
    docente (S-004 y S-005) responden 403 en los tres casos por igual.
    """
    if user is None or not user.is_authenticated:
        return None
    return Course.objects.filter(
        code=course_code,
        teaching_assignments__teacher__user=user,
    ).first()


def record_grade(*, user, course, student_pk, topic_pk, value):
    """Registra o corrige la nota de un estudiante en un tema del curso.

    Comprueba en el servidor que el usuario tiene sesión e imparte el curso,
    que el tema pertenece al curso, que el estudiante está inscrito en él y
    que la nota es un entero de 0 a 100 (D-008). Si algo falla, lanza
    GradeRegistrationError y no escribe nada. Sin sesión, rechaza antes de
    abrir la transacción, sin consultar la base. Corregir reemplaza la nota
    anterior: siempre queda un solo registro por estudiante y tema.

    Devuelve (grade, created), donde created es False si se corrigió.
    """
    if user is None or not user.is_authenticated:
        raise GradeRegistrationError(NOT_TEACHING_MESSAGE)

    with transaction.atomic():
        return _record_grade_for_teacher(
            user=user,
            course=course,
            student_pk=student_pk,
            topic_pk=topic_pk,
            value=value,
        )


def _record_grade_for_teacher(*, user, course, student_pk, topic_pk, value):
    if not TeachingAssignment.objects.filter(
        teacher__user=user,
        course=course,
    ).exists():
        raise GradeRegistrationError(NOT_TEACHING_MESSAGE)

    topic = Topic.objects.filter(pk=topic_pk, course=course).first()
    if topic is None:
        raise GradeRegistrationError(
            "El tema no pertenece a este curso. La nota no se guardó."
        )

    enrollment = (
        Enrollment.objects.select_related("student__user")
        .filter(student_id=student_pk, course=course)
        .first()
    )
    if enrollment is None:
        raise GradeRegistrationError(
            "El estudiante no está asignado a este curso. La nota no se guardó."
        )

    if (
        isinstance(value, bool)
        or not isinstance(value, int)
        or not GRADE_MIN_VALUE <= value <= GRADE_MAX_VALUE
    ):
        raise GradeRegistrationError(
            "La nota debe ser un número entero entre 0 y 100."
        )

    return Grade.objects.update_or_create(
        student=enrollment.student,
        topic=topic,
        defaults={"value": value},
    )
