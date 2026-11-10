from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

from academics.models import Course, Enrollment, Grade, Topic

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
