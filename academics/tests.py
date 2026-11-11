import os
import secrets
from decimal import Decimal
from io import StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import IntegrityError, transaction
from django.test import Client, SimpleTestCase, TestCase, override_settings
from django.urls import reverse

from academics.management.commands.rebuild_synthetic_data import (
    COURSE_BLUEPRINTS,
    DEMO_CAREER,
    DEMO_SEMESTER,
    DEMO_STUDENT_ID,
    DEMO_TEACHER_USERNAMES,
    DEMO_USERNAME,
    PILOT_COURSE_CODE,
    PILOT_COURSE_NAME,
    TEACHER_ASSIGNMENTS,
    TOTAL_STUDENTS,
)
from academics.models import (
    Course,
    Enrollment,
    Grade,
    StudentProfile,
    TeacherProfile,
    TeachingAssignment,
    Topic,
)
from academics.services import (
    GradeRegistrationError,
    TopicGrade,
    calculate_average,
    get_course_grade_sheet,
    get_course_panel,
    get_course_summaries,
    get_student_panel_row,
    get_taught_course,
    get_taught_courses,
    get_weak_topics,
    is_weak,
    record_grade,
)


class AcademicModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="modelo_estudiante",
            password=secrets.token_urlsafe(24),
        )
        self.profile = StudentProfile.objects.create(
            user=self.user,
            student_id="2025-00001",
            career="Carrera Sintética",
            semester=2,
        )
        self.course = Course.objects.create(
            code="CURSO-PRUEBA",
            name="Curso de prueba",
        )

    def test_student_id_format_and_semester_are_validated(self):
        invalid_profile = StudentProfile(
            user=get_user_model().objects.create_user(username="invalido"),
            student_id="sin-formato",
            career="Carrera Sintética",
            semester=11,
        )

        with self.assertRaises(ValidationError):
            invalid_profile.full_clean()

        with self.assertRaises(IntegrityError), transaction.atomic():
            StudentProfile.objects.create(
                user=get_user_model().objects.create_user(username="semestre"),
                student_id="2025-00002",
                career="Carrera Sintética",
                semester=11,
            )

    def test_student_id_is_unique(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            StudentProfile.objects.create(
                user=get_user_model().objects.create_user(username="duplicado"),
                student_id=self.profile.student_id,
                career="Otra carrera",
                semester=3,
            )

    def test_course_code_is_required_and_unique(self):
        with self.assertRaises(ValidationError):
            Course(code="", name="Sin código").full_clean()

        with self.assertRaises(IntegrityError), transaction.atomic():
            Course.objects.create(code=self.course.code, name="Duplicado")

    def test_enrollment_is_unique_per_student_and_course(self):
        Enrollment.objects.create(student=self.profile, course=self.course)

        with self.assertRaises(IntegrityError), transaction.atomic():
            Enrollment.objects.create(student=self.profile, course=self.course)


class S002AcademicModelTests(TestCase):
    def setUp(self):
        self.teacher_user = get_user_model().objects.create_user(
            username="docente_modelo",
            password=secrets.token_urlsafe(24),
        )
        self.teacher = TeacherProfile.objects.create(user=self.teacher_user)
        self.course = Course.objects.create(
            code="S002-CURSO",
            name="Curso S-002",
        )
        self.student_user = get_user_model().objects.create_user(
            username="estudiante_s002",
            password=secrets.token_urlsafe(24),
        )
        self.student = StudentProfile.objects.create(
            user=self.student_user,
            student_id="2026-00999",
            career="Carrera Sintética",
            semester=1,
        )
        self.topic = Topic.objects.create(
            course=self.course,
            name="Tema de prueba",
        )

    def test_teacher_profile_is_unique_per_user(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            TeacherProfile.objects.create(user=self.teacher_user)

    def test_teaching_assignment_is_unique_per_teacher_and_course(self):
        TeachingAssignment.objects.create(
            teacher=self.teacher,
            course=self.course,
        )

        with self.assertRaises(IntegrityError), transaction.atomic():
            TeachingAssignment.objects.create(
                teacher=self.teacher,
                course=self.course,
            )

    def test_topic_name_is_unique_only_within_the_same_course(self):
        other_course = Course.objects.create(
            code="S002-OTRO",
            name="Otro curso",
        )
        Topic.objects.create(course=other_course, name=self.topic.name)

        with self.assertRaises(IntegrityError), transaction.atomic():
            Topic.objects.create(course=self.course, name=self.topic.name)

    def test_grade_value_is_limited_to_0_and_100(self):
        for invalid_value in (-1, 101):
            grade = Grade(
                student=self.student,
                topic=self.topic,
                value=invalid_value,
            )
            with self.assertRaises(ValidationError):
                grade.full_clean()

        with self.assertRaises(IntegrityError), transaction.atomic():
            Grade.objects.create(
                student=self.student,
                topic=self.topic,
                value=101,
            )

    def test_grade_is_unique_per_student_and_topic(self):
        Grade.objects.create(
            student=self.student,
            topic=self.topic,
            value=60,
        )

        with self.assertRaises(IntegrityError), transaction.atomic():
            Grade.objects.create(
                student=self.student,
                topic=self.topic,
                value=80,
            )

    def test_grade_accepts_the_valid_boundaries(self):
        topic_zero = Topic.objects.create(course=self.course, name="Tema cero")
        topic_hundred = Topic.objects.create(
            course=self.course,
            name="Tema cien",
        )

        Grade.objects.create(student=self.student, topic=topic_zero, value=0)
        Grade.objects.create(
            student=self.student,
            topic=topic_hundred,
            value=100,
        )


class CalculateAverageTests(SimpleTestCase):
    def test_simple_average_is_rounded_to_two_decimals(self):
        self.assertEqual(calculate_average([80, 65, 70]), Decimal("71.67"))

    def test_topics_without_grade_are_excluded(self):
        average = calculate_average([80, 60, None])

        self.assertEqual(average, Decimal("70.00"))
        self.assertEqual(str(average), "70.00")

    def test_returns_none_when_there_are_no_grades(self):
        self.assertIsNone(calculate_average([None, None]))
        self.assertIsNone(calculate_average([]))

    def test_ties_are_rounded_half_up(self):
        self.assertEqual(
            calculate_average([70, 70, 70, 70, 70, 70, 70, 71]),
            Decimal("70.13"),
        )

    def test_accepts_scale_boundaries_and_any_iterable(self):
        self.assertEqual(calculate_average([0, 100]), Decimal("50.00"))
        self.assertEqual(
            calculate_average(value for value in (100,)),
            Decimal("100.00"),
        )


class GetCourseSummariesTests(TestCase):
    def setUp(self):
        self.student = self.create_student("2026-10001")
        self.networks = Course.objects.create(code="S003-RED", name="Redes de prueba")
        self.algorithms = Course.objects.create(
            code="S003-ALG",
            name="Algoritmos de prueba",
        )
        self.unenrolled = Course.objects.create(
            code="S003-AJENO",
            name="Curso sin inscripción",
        )
        self.topics = {
            course.code: [
                Topic.objects.create(course=course, name=name)
                for name in ("Variables", "Condicionales", "Ciclos")
            ]
            for course in (self.networks, self.algorithms, self.unenrolled)
        }
        Enrollment.objects.create(student=self.student, course=self.networks)
        Enrollment.objects.create(student=self.student, course=self.algorithms)

    def create_student(self, student_id):
        user = get_user_model().objects.create_user(
            username=f"resumen_{student_id}",
            password=secrets.token_urlsafe(24),
        )
        return StudentProfile.objects.create(
            user=user,
            student_id=student_id,
            career="Carrera Sintética",
            semester=3,
        )

    def grade(self, student, course, topic_index, value):
        return Grade.objects.create(
            student=student,
            topic=self.topics[course.code][topic_index],
            value=value,
        )

    def test_returns_only_enrolled_courses_ordered_by_name(self):
        self.grade(self.student, self.unenrolled, 0, 90)

        summaries = get_course_summaries(self.student)

        self.assertEqual(
            [summary.course for summary in summaries],
            [self.algorithms, self.networks],
        )

    def test_topics_keep_creation_order_with_grade_or_none(self):
        self.grade(self.student, self.algorithms, 0, 80)
        self.grade(self.student, self.algorithms, 1, 60)

        summary = get_course_summaries(self.student)[0]

        self.assertEqual(
            [(item.topic.name, item.value) for item in summary.topics],
            [("Variables", 80), ("Condicionales", 60), ("Ciclos", None)],
        )
        self.assertEqual(summary.average, Decimal("70.00"))

    def test_course_without_grades_has_no_average(self):
        self.grade(self.student, self.algorithms, 0, 80)

        summaries = get_course_summaries(self.student)

        networks_summary = summaries[1]
        self.assertEqual(networks_summary.course, self.networks)
        self.assertTrue(all(item.value is None for item in networks_summary.topics))
        self.assertIsNone(networks_summary.average)

    def test_ignores_grades_of_other_students(self):
        other_student = self.create_student("2026-10002")
        Enrollment.objects.create(student=other_student, course=self.algorithms)
        self.grade(other_student, self.algorithms, 0, 100)
        self.grade(self.student, self.algorithms, 0, 50)

        summary = get_course_summaries(self.student)[0]

        self.assertEqual(summary.topics[0].value, 50)
        self.assertEqual(summary.average, Decimal("50.00"))

    def test_student_without_enrollments_has_no_summaries(self):
        student = self.create_student("2026-10003")

        self.assertEqual(get_course_summaries(student), [])

    def test_reads_current_grade_on_each_call(self):
        grade = self.grade(self.student, self.algorithms, 0, 40)
        self.assertEqual(
            get_course_summaries(self.student)[0].average,
            Decimal("40.00"),
        )

        grade.value = 90
        grade.save()

        summary = get_course_summaries(self.student)[0]
        self.assertEqual(summary.topics[0].value, 90)
        self.assertEqual(summary.average, Decimal("90.00"))

    def test_uses_three_queries_regardless_of_course_count(self):
        for topic_index, value in enumerate((80, 65, 70)):
            self.grade(self.student, self.algorithms, topic_index, value)
            self.grade(self.student, self.networks, topic_index, value)

        with self.assertNumQueries(3):
            summaries = get_course_summaries(self.student)
            self.assertEqual(
                [summary.average for summary in summaries],
                [Decimal("71.67"), Decimal("71.67")],
            )


def create_s005_user(username):
    return get_user_model().objects.create_user(
        username=username,
        password=secrets.token_urlsafe(24),
    )


def create_s005_teacher(username, *courses):
    teacher = TeacherProfile.objects.create(user=create_s005_user(username))
    for course in courses:
        TeachingAssignment.objects.create(teacher=teacher, course=course)
    return teacher


def create_s005_student(student_id, *courses):
    student = StudentProfile.objects.create(
        user=create_s005_user(f"notas_{student_id}"),
        student_id=student_id,
        career="Carrera Sintética",
        semester=2,
    )
    for course in courses:
        Enrollment.objects.create(student=student, course=course)
    return student


class GetTaughtCourseTests(TestCase):
    def setUp(self):
        self.own_course = Course.objects.create(code="S005-PROPIO", name="Curso propio")
        self.other_course = Course.objects.create(code="S005-AJENO", name="Curso ajeno")
        self.teacher = create_s005_teacher("docente_s005", self.own_course)
        create_s005_teacher("otro_docente_s005", self.other_course)

    def test_returns_course_taught_by_user(self):
        self.assertEqual(
            get_taught_course(self.teacher.user, "S005-PROPIO"),
            self.own_course,
        )

    def test_returns_none_for_course_taught_by_another_teacher(self):
        self.assertIsNone(get_taught_course(self.teacher.user, "S005-AJENO"))

    def test_returns_none_for_unknown_course_code(self):
        self.assertIsNone(get_taught_course(self.teacher.user, "NO-EXISTE"))

    def test_returns_none_for_accounts_without_teacher_profile(self):
        student = create_s005_student("2026-20001", self.own_course)
        staff = get_user_model().objects.create_user(
            username="personal_s005",
            password=secrets.token_urlsafe(24),
            is_staff=True,
        )

        for user in (create_s005_user("sin_perfil_s005"), student.user, staff):
            with self.subTest(username=user.username):
                self.assertIsNone(get_taught_course(user, "S005-PROPIO"))

    def test_returns_none_for_anonymous_user_without_queries(self):
        with self.assertNumQueries(0):
            self.assertIsNone(get_taught_course(AnonymousUser(), "S005-PROPIO"))
            self.assertIsNone(get_taught_course(None, "S005-PROPIO"))


class RecordGradeTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(code="S005-PROG", name="Programación de prueba")
        self.other_course = Course.objects.create(code="S005-BD", name="Bases de prueba")
        self.topic, self.second_topic = (
            Topic.objects.create(course=self.course, name=name)
            for name in ("Variables", "Ciclos")
        )
        self.other_topic = Topic.objects.create(course=self.other_course, name="SQL")
        self.teacher = create_s005_teacher("docente_notas", self.course)
        self.other_teacher = create_s005_teacher("otro_docente_notas", self.other_course)
        self.student = create_s005_student("2026-20010", self.course, self.other_course)
        self.outsider = create_s005_student("2026-20011", self.other_course)

    def record(self, **overrides):
        arguments = {
            "user": self.teacher.user,
            "course": self.course,
            "student_pk": self.student.pk,
            "topic_pk": self.topic.pk,
            "value": 85,
        }
        arguments.update(overrides)
        return record_grade(**arguments)

    def grade_snapshot(self):
        return list(
            Grade.objects.order_by("pk").values_list("student_id", "topic_id", "value")
        )

    def assert_rejected(self, message, **overrides):
        before = self.grade_snapshot()
        with self.assertRaisesMessage(GradeRegistrationError, message):
            self.record(**overrides)
        self.assertEqual(self.grade_snapshot(), before)

    def test_registers_grade_when_student_has_none(self):
        grade, created = self.record(value=85)

        self.assertTrue(created)
        self.assertEqual(
            self.grade_snapshot(),
            [(self.student.pk, self.topic.pk, 85)],
        )
        self.assertEqual(grade.student, self.student)
        self.assertEqual(grade.topic, self.topic)

    def test_correction_replaces_previous_grade(self):
        Grade.objects.create(student=self.student, topic=self.topic, value=60)

        grade, created = self.record(value=75)

        self.assertFalse(created)
        self.assertEqual(grade.value, 75)
        self.assertEqual(
            self.grade_snapshot(),
            [(self.student.pk, self.topic.pk, 75)],
        )

    def test_correction_does_not_touch_other_topics(self):
        Grade.objects.create(student=self.student, topic=self.second_topic, value=50)

        self.record(value=90)

        self.assertEqual(
            Grade.objects.get(student=self.student, topic=self.second_topic).value,
            50,
        )

    def test_accepts_scale_boundaries(self):
        for value in (0, 100):
            with self.subTest(value=value):
                grade, _ = self.record(value=value)
                grade.refresh_from_db()
                self.assertEqual(grade.value, value)

    def test_rejects_values_outside_scale_or_not_integer(self):
        Grade.objects.create(student=self.student, topic=self.topic, value=60)

        for value in (-1, 101, True, 85.5, "85", None):
            with self.subTest(value=value):
                self.assert_rejected(
                    "La nota debe ser un número entero entre 0 y 100.",
                    value=value,
                )

    def test_rejects_course_taught_by_another_teacher(self):
        self.assert_rejected(
            "Usted no imparte este curso. La nota no se guardó.",
            course=self.other_course,
            topic_pk=self.other_topic.pk,
        )

    def test_rejects_account_without_teacher_profile(self):
        for user in (create_s005_user("sin_perfil_notas"), self.student.user):
            with self.subTest(username=user.username):
                self.assert_rejected(
                    "Usted no imparte este curso. La nota no se guardó.",
                    user=user,
                )

    def test_rejects_unauthenticated_user_without_queries(self):
        before = self.grade_snapshot()

        for user in (AnonymousUser(), None):
            with self.subTest(user=user):
                with self.assertNumQueries(0):
                    with self.assertRaisesMessage(
                        GradeRegistrationError,
                        "Usted no imparte este curso. La nota no se guardó.",
                    ):
                        self.record(user=user)

        self.assertEqual(self.grade_snapshot(), before)

    def test_rejects_topic_from_another_course(self):
        Grade.objects.create(student=self.student, topic=self.other_topic, value=40)

        self.assert_rejected(
            "El tema no pertenece a este curso. La nota no se guardó.",
            topic_pk=self.other_topic.pk,
        )

    def test_rejects_unknown_topic(self):
        self.assert_rejected(
            "El tema no pertenece a este curso. La nota no se guardó.",
            topic_pk=self.other_topic.pk + 1000,
        )

    def test_rejects_student_not_enrolled_in_course(self):
        self.assert_rejected(
            "El estudiante no está asignado a este curso. La nota no se guardó.",
            student_pk=self.outsider.pk,
        )

    def test_rejects_unknown_student(self):
        self.assert_rejected(
            "El estudiante no está asignado a este curso. La nota no se guardó.",
            student_pk=self.outsider.pk + 1000,
        )


class GetCourseGradeSheetTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(code="S005-WEB", name="Web de prueba")
        self.other_course = Course.objects.create(code="S005-RED", name="Redes de prueba")
        self.topics = [
            Topic.objects.create(course=self.course, name=name)
            for name in ("HTML", "CSS", "JavaScript")
        ]
        self.other_topic = Topic.objects.create(course=self.other_course, name="Subredes")
        self.late_student = create_s005_student("2026-20032", self.course)
        self.early_student = create_s005_student("2026-20031", self.course)
        self.outsider = create_s005_student("2026-20033", self.other_course)

    def grade(self, student, topic, value):
        return Grade.objects.create(student=student, topic=topic, value=value)

    def test_rows_include_only_enrolled_students_ordered_by_student_id(self):
        sheet = get_course_grade_sheet(self.course)

        self.assertEqual(sheet.course, self.course)
        self.assertEqual(
            [row.student for row in sheet.rows],
            [self.early_student, self.late_student],
        )

    def test_topics_include_only_course_topics_in_creation_order(self):
        sheet = get_course_grade_sheet(self.course)

        self.assertEqual(list(sheet.topics), self.topics)
        self.assertNotIn(self.other_topic, sheet.topics)

    def test_grades_follow_topic_order_with_none_for_missing(self):
        self.grade(self.early_student, self.topics[0], 85)
        self.grade(self.early_student, self.topics[2], 40)

        sheet = get_course_grade_sheet(self.course)

        self.assertEqual(sheet.rows[0].grades, (85, None, 40))
        self.assertEqual(sheet.rows[1].grades, (None, None, None))

    def test_ignores_grades_of_other_courses_and_unenrolled_students(self):
        Enrollment.objects.create(student=self.early_student, course=self.other_course)
        self.grade(self.early_student, self.other_topic, 99)
        self.grade(self.outsider, self.topics[0], 70)

        sheet = get_course_grade_sheet(self.course)

        self.assertNotIn(self.outsider, [row.student for row in sheet.rows])
        self.assertEqual(sheet.rows[0].grades, (None, None, None))

    def test_reflects_correction_made_with_record_grade(self):
        teacher = create_s005_teacher("docente_planilla", self.course)
        self.grade(self.early_student, self.topics[1], 60)

        record_grade(
            user=teacher.user,
            course=self.course,
            student_pk=self.early_student.pk,
            topic_pk=self.topics[1].pk,
            value=75,
        )

        sheet = get_course_grade_sheet(self.course)
        self.assertEqual(sheet.rows[0].grades, (None, 75, None))

    def test_course_without_students_or_topics_is_empty(self):
        empty_course = Course.objects.create(code="S005-VACIO", name="Curso vacío")

        sheet = get_course_grade_sheet(empty_course)

        self.assertEqual(sheet.topics, ())
        self.assertEqual(sheet.rows, ())

    def test_uses_three_queries_regardless_of_course_size(self):
        for index in range(5):
            create_s005_student(f"2026-2004{index}", self.course)
        for topic in self.topics:
            self.grade(self.early_student, topic, 80)

        with self.assertNumQueries(3):
            sheet = get_course_grade_sheet(self.course)
            names = [row.student.user.get_username() for row in sheet.rows]

        self.assertEqual(len(names), 7)
        self.assertEqual(sheet.rows[0].grades, (80, 80, 80))


class TeacherCourseGradesViewTests(TestCase):
    def setUp(self):
        self.programming = Course.objects.create(code="S005-PC", name="Programación")
        self.web = Course.objects.create(code="S005-DW", name="Desarrollo web")
        self.databases = Course.objects.create(code="S005-BDA", name="Bases de datos")
        self.topics = {
            course.code: [
                Topic.objects.create(course=course, name=f"{name} {course.code}")
                for name in ("Variables", "Ciclos")
            ]
            for course in (self.programming, self.web, self.databases)
        }
        self.teacher = create_s005_teacher("docente_vista", self.programming, self.web)
        create_s005_teacher("docente_bd_vista", self.databases)
        self.without_grades = create_s005_student(
            "2026-20051", self.programming, self.web
        )
        self.with_grade = create_s005_student("2026-20052", self.programming)
        self.outsider = create_s005_student("2026-20053", self.databases)
        Grade.objects.create(
            student=self.with_grade,
            topic=self.topics["S005-PC"][0],
            value=60,
        )
        self.client.force_login(self.teacher.user)

    def url(self, course):
        code = course if isinstance(course, str) else course.code
        return reverse("teacher_course_grades", args=[code])

    def post_grade(self, course, student, topic, value, **kwargs):
        return self.client.post(
            self.url(course),
            {"student": student.pk, "topic": topic.pk, "value": value},
            **kwargs,
        )

    def grade_snapshot(self):
        return list(
            Grade.objects.order_by("pk").values_list("student_id", "topic_id", "value")
        )

    def choice_values(self, response, field_name):
        widget = response.context["form"].fields[field_name].widget
        return [value for value, _ in widget.choices if value != ""]

    def test_ca1_registers_new_grade_and_shows_confirmation(self):
        topic = self.topics["S005-PC"][0]

        response = self.post_grade(self.programming, self.without_grades, topic, "85")

        self.assertRedirects(
            response,
            self.url(self.programming),
            fetch_redirect_response=False,
        )
        self.assertEqual(
            Grade.objects.get(student=self.without_grades, topic=topic).value,
            85,
        )
        page = self.client.get(self.url(self.programming))
        self.assertContains(page, "Se guardó la nota 85 de notas_2026-20051")
        self.assertContains(page, "<td>85</td>", html=True)

    def test_ca2_correction_replaces_previous_grade(self):
        topic = self.topics["S005-PC"][0]

        response = self.post_grade(
            self.programming, self.with_grade, topic, "75", follow=True
        )

        self.assertContains(response, "Se actualizó la nota 75")
        self.assertContains(response, "<td>75</td>", html=True)
        self.assertNotContains(response, "<td>60</td>", html=True)
        self.assertEqual(
            list(
                Grade.objects.filter(student=self.with_grade, topic=topic).values_list(
                    "value", flat=True
                )
            ),
            [75],
        )

    def test_ca3_invalid_values_show_spanish_error_and_keep_grade(self):
        topic = self.topics["S005-PC"][0]
        cases = {
            "-5": "La nota debe estar entre 0 y 100.",
            "101": "La nota debe estar entre 0 y 100.",
            "": "Ingrese una nota.",
            "abc": "La nota debe ser un número entero.",
            "85.5": "La nota debe ser un número entero.",
        }

        for value, message in cases.items():
            with self.subTest(value=value):
                response = self.post_grade(self.programming, self.with_grade, topic, value)

                self.assertContains(response, message, status_code=400)
                self.assertEqual(
                    Grade.objects.get(student=self.with_grade, topic=topic).value,
                    60,
                )

    def test_ca4_student_profile_shows_new_grade_and_average(self):
        topic = self.topics["S005-PC"][1]
        self.post_grade(self.programming, self.without_grades, topic, "85")

        self.client.force_login(self.without_grades.user)
        response = self.client.get(reverse("student_profile"))

        self.assertContains(response, "<td>85</td>", html=True)
        self.assertContains(response, "85.00")

    def test_ca5_grade_persists_after_logging_in_again(self):
        password = secrets.token_urlsafe(24)
        self.teacher.user.set_password(password)
        self.teacher.user.save()
        credentials = {"username": self.teacher.user.username, "password": password}
        self.assertTrue(self.client.login(**credentials))
        topic = self.topics["S005-PC"][1]
        saved = self.post_grade(self.programming, self.without_grades, topic, "85")
        self.assertEqual(saved.status_code, 302)

        self.client.post(reverse("logout"))
        self.assertTrue(self.client.login(**credentials))
        response = self.client.get(self.url(self.programming))

        self.assertContains(response, "<td>85</td>", html=True)

    def test_ca6_only_enrolled_students_appear(self):
        response = self.client.get(self.url(self.web))

        self.assertContains(response, self.without_grades.student_id)
        self.assertNotContains(response, self.with_grade.student_id)
        self.assertNotContains(response, self.outsider.student_id)
        self.assertEqual(
            self.choice_values(response, "student"),
            [self.without_grades.pk],
        )

    def test_ca7_only_course_topics_appear(self):
        response = self.client.get(self.url(self.programming))

        for topic in self.topics["S005-PC"]:
            self.assertContains(response, topic.name)
        for code in ("S005-DW", "S005-BDA"):
            for topic in self.topics[code]:
                self.assertNotContains(response, topic.name)
        self.assertEqual(
            self.choice_values(response, "topic"),
            [topic.pk for topic in self.topics["S005-PC"]],
        )

    def test_ca8_rejects_student_not_enrolled_in_course(self):
        before = self.grade_snapshot()

        response = self.post_grade(
            self.web, self.with_grade, self.topics["S005-DW"][0], "90"
        )

        self.assertContains(
            response,
            "El estudiante no está asignado a este curso. La nota no se guardó.",
            status_code=400,
        )
        self.assertEqual(self.grade_snapshot(), before)

    def test_ca8_rejects_topic_from_another_course(self):
        before = self.grade_snapshot()

        response = self.post_grade(
            self.programming, self.with_grade, self.topics["S005-BDA"][0], "90"
        )

        self.assertContains(
            response,
            "El tema no pertenece a este curso. La nota no se guardó.",
            status_code=400,
        )
        self.assertEqual(self.grade_snapshot(), before)

    def test_ca8_rejects_course_taught_by_another_teacher(self):
        before = self.grade_snapshot()

        response = self.post_grade(
            self.databases, self.outsider, self.topics["S005-BDA"][0], "90"
        )

        self.assertContains(response, "Acceso denegado", status_code=403)
        self.assertEqual(self.grade_snapshot(), before)

    def test_anonymous_user_is_redirected_to_login(self):
        self.client.logout()
        url = self.url(self.programming)

        response = self.client.get(url)

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={url}",
            fetch_redirect_response=False,
        )

    def test_accounts_without_teacher_role_are_denied(self):
        staff = get_user_model().objects.create_user(
            username="personal_vista",
            password=secrets.token_urlsafe(24),
            is_staff=True,
        )
        for user in (self.without_grades.user, create_s005_user("sin_perfil_vista"), staff):
            with self.subTest(username=user.username):
                self.client.force_login(user)
                response = self.client.get(self.url(self.programming))
                self.assertContains(response, "Acceso denegado", status_code=403)

    def test_unknown_course_code_is_denied_like_foreign_course(self):
        response = self.client.get(self.url("NO-EXISTE"))

        self.assertContains(response, "Acceso denegado", status_code=403)

    def test_post_without_csrf_token_is_rejected(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.teacher.user)
        before = self.grade_snapshot()

        response = client.post(
            self.url(self.programming),
            {
                "student": self.without_grades.pk,
                "topic": self.topics["S005-PC"][0].pk,
                "value": "85",
            },
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.grade_snapshot(), before)

    def test_empty_course_shows_empty_states_without_form(self):
        empty_course = Course.objects.create(code="S005-VACIO-V", name="Vacío")
        TeachingAssignment.objects.create(teacher=self.teacher, course=empty_course)

        response = self.client.get(self.url(empty_course))

        self.assertContains(response, "Este curso aún no tiene estudiantes asignados.")
        self.assertContains(response, "Este curso aún no tiene temas registrados.")
        self.assertNotContains(response, "Guardar nota")

    def test_missing_grade_is_shown_as_sin_nota(self):
        response = self.client.get(self.url(self.programming))

        self.assertContains(response, "<td>Sin nota</td>", html=True)


class StudentProfileViewTests(TestCase):
    def setUp(self):
        self.programming = Course.objects.create(
            code="S003-PROG",
            name="Programación de prueba",
        )
        self.databases = Course.objects.create(
            code="S003-BD",
            name="Bases de datos de prueba",
        )
        self.networks = Course.objects.create(
            code="S003-RED",
            name="Redes sin inscripción",
        )
        self.topics = {
            course.code: [
                Topic.objects.create(course=course, name=f"{name} {course.code}")
                for name in ("Variables", "Condicionales", "Ciclos")
            ]
            for course in (self.programming, self.databases, self.networks)
        }
        self.student_number = 0

    def create_student(self, *, courses=(), first_name="", last_name="", **fields):
        self.student_number += 1
        user = get_user_model().objects.create_user(
            username=f"perfil_{self.student_number}",
            password=secrets.token_urlsafe(24),
            first_name=first_name,
            last_name=last_name,
        )
        profile = StudentProfile.objects.create(
            user=user,
            student_id=fields.get("student_id", f"2026-2{self.student_number:04d}"),
            career=fields.get("career", "Carrera Sintética"),
            semester=fields.get("semester", 2),
        )
        for course in courses:
            Enrollment.objects.create(student=profile, course=course)
        return user, profile

    def set_grades(self, profile, course, values):
        for topic, value in zip(self.topics[course.code], values):
            if value is not None:
                Grade.objects.create(student=profile, topic=topic, value=value)

    def get_profile(self, user, **params):
        self.client.force_login(user)
        return self.client.get(reverse("student_profile"), params)

    def test_anonymous_access_redirects_to_login(self):
        response = self.client.get(reverse("student_profile"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('student_profile')}",
        )

    def test_accounts_without_student_profile_are_denied(self):
        teacher_user = get_user_model().objects.create_user(username="docente_s003")
        TeacherProfile.objects.create(user=teacher_user)
        accounts = {
            "sin perfil": get_user_model().objects.create_user(username="sin_s003"),
            "docente": teacher_user,
            "personal técnico": get_user_model().objects.create_user(
                username="staff_s003",
                is_staff=True,
            ),
        }
        for label, user in accounts.items():
            with self.subTest(cuenta=label):
                response = self.get_profile(user)

                self.assertContains(
                    response,
                    "Su cuenta no tiene autorización académica",
                    status_code=403,
                )

    def test_profile_only_accepts_get(self):
        user, _ = self.create_student(courses=[self.programming])
        self.client.force_login(user)

        self.assertEqual(self.client.post(reverse("student_profile")).status_code, 405)

    def test_ca1_shows_personal_data_of_authenticated_student(self):
        user, _ = self.create_student(
            courses=[self.programming],
            first_name="Lucía",
            last_name="Sintética",
            student_id="2025-01234",
            career="Ingeniería Ficticia",
            semester=7,
        )

        response = self.get_profile(user)

        self.assertEqual(response.status_code, 200)
        for value in ("Lucía Sintética", "2025-01234", "Ingeniería Ficticia", "7"):
            self.assertContains(response, f"<dd>{value}</dd>", html=True)

    def test_ca1_uses_username_when_account_has_no_name(self):
        user, _ = self.create_student(courses=[self.programming])

        response = self.get_profile(user)

        self.assertContains(response, f"<dd>{user.username}</dd>", html=True)

    def test_ca2_shows_only_enrolled_courses(self):
        user, _ = self.create_student(courses=[self.programming, self.databases])

        response = self.get_profile(user)

        self.assertContains(response, "S003-PROG – Programación de prueba")
        self.assertContains(response, "S003-BD – Bases de datos de prueba")
        self.assertNotContains(response, self.networks.code)
        self.assertNotContains(response, self.networks.name)

    def test_ca3_shows_each_grade_and_course_average(self):
        user, profile = self.create_student(courses=[self.programming])
        self.set_grades(profile, self.programming, (80, 65, 70))

        response = self.get_profile(user)

        for value in (80, 65, 70):
            self.assertContains(response, f"<td>{value}</td>", html=True)
        self.assertContains(response, "<td>71.67</td>", html=True)
        self.assertNotContains(response, "71,67")

    def test_ca4_topic_without_grade_is_shown_and_excluded(self):
        user, profile = self.create_student(courses=[self.programming])
        self.set_grades(profile, self.programming, (80, 60, None))

        response = self.get_profile(user)

        self.assertContains(response, "<td>Sin nota</td>", count=1, html=True)
        self.assertContains(response, "<td>70.00</td>", html=True)

    def test_ca5_course_without_grades_shows_sin_notas(self):
        user, _ = self.create_student(courses=[self.programming])

        response = self.get_profile(user)

        self.assertContains(response, "<td>Sin nota</td>", count=3, html=True)
        self.assertContains(response, "<td>Sin notas</td>", count=1, html=True)

    def test_ca6_student_without_courses_sees_data_and_notice(self):
        user, profile = self.create_student(career="Carrera sin cursos")

        response = self.get_profile(user)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"<dd>{profile.student_id}</dd>", html=True)
        self.assertContains(response, "<dd>Carrera sin cursos</dd>", html=True)
        self.assertContains(response, "Aún no tiene cursos asignados.")

    def test_ca7_each_student_sees_only_own_profile(self):
        first_user, first = self.create_student(
            courses=[self.programming],
            career="Carrera Primera",
        )
        second_user, second = self.create_student(
            courses=[self.databases],
            career="Carrera Segunda",
        )
        self.set_grades(first, self.programming, (90, 80, 70))
        self.set_grades(second, self.databases, (50, 55, 45))

        first_response = self.get_profile(first_user, student_id=second.student_id)
        second_response = self.get_profile(second_user, student_id=first.student_id)

        self.assertContains(first_response, first.student_id)
        self.assertContains(first_response, "Carrera Primera")
        self.assertContains(first_response, "<td>80.00</td>", html=True)
        self.assertNotContains(first_response, second.student_id)
        self.assertNotContains(first_response, "Carrera Segunda")
        self.assertNotContains(first_response, self.databases.name)

        self.assertContains(second_response, second.student_id)
        self.assertContains(second_response, "Carrera Segunda")
        self.assertContains(second_response, "<td>50.00</td>", html=True)
        self.assertNotContains(second_response, first.student_id)
        self.assertNotContains(second_response, "Carrera Primera")
        self.assertNotContains(second_response, self.programming.name)

    def test_ca8_reload_shows_updated_grade_and_average(self):
        user, profile = self.create_student(courses=[self.programming])
        self.set_grades(profile, self.programming, (80, 65, 70))
        self.assertContains(self.get_profile(user), "<td>71.67</td>", html=True)

        Grade.objects.filter(
            student=profile,
            topic=self.topics[self.programming.code][1],
        ).update(value=95)
        response = self.client.get(reverse("student_profile"))

        self.assertContains(response, "<td>95</td>", html=True)
        self.assertNotContains(response, "<td>65</td>", html=True)
        self.assertContains(response, "<td>81.67</td>", html=True)


class StudentAccessTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.course = Course.objects.create(
            code=PILOT_COURSE_CODE,
            name=PILOT_COURSE_NAME,
        )
        self.student_number = 0

    def create_student(self, career, *, enrolled=True, **user_fields):
        self.student_number += 1
        user = get_user_model().objects.create_user(
            username=f"estudiante_{self.student_number}",
            password=secrets.token_urlsafe(24),
            **user_fields,
        )
        profile = StudentProfile.objects.create(
            user=user,
            student_id=f"2026-{self.student_number:05d}",
            career=career,
            semester=2,
        )
        if enrolled:
            Enrollment.objects.create(student=profile, course=self.course)
        return user, profile

    def test_anonymous_access_redirects_to_login_with_safe_next(self):
        response = self.client.get(reverse("student_home"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('student_home')}",
        )

    def test_account_without_profile_is_denied_in_spanish(self):
        user = get_user_model().objects.create_user(username="sin_perfil")
        self.client.force_login(user)

        response = self.client.get(reverse("student_home"))

        self.assertEqual(response.status_code, 403)
        self.assertContains(
            response,
            "Su cuenta no tiene autorización académica",
            status_code=403,
        )

    def test_student_without_enrollments_is_denied(self):
        user, _ = self.create_student("Carrera sin inscripción", enrolled=False)
        self.client.force_login(user)

        response = self.client.get(reverse("student_home"))

        self.assertEqual(response.status_code, 403)
        self.assertNotContains(response, "Carrera sin inscripción", status_code=403)

    @override_settings(AI_MODE="demo")
    def test_student_enrolled_only_in_another_course_can_access_tutor(self):
        user, profile = self.create_student("Carrera inscrita", enrolled=False)
        course = Course.objects.create(code="DES-WEB", name="Desarrollo Web")
        Enrollment.objects.create(student=profile, course=course)
        self.client.force_login(user)

        response = self.client.get(reverse("student_home"))

        self.assertContains(response, "Consulte sobre Desarrollo Web")
        self.assertNotContains(response, PILOT_COURSE_NAME)
        self.assertContains(response, "El modo demo aún no tiene respuestas grabadas")

    def test_staff_status_alone_does_not_grant_academic_access(self):
        user = get_user_model().objects.create_user(
            username="personal_tecnico",
            is_staff=True,
        )
        self.client.force_login(user)

        response = self.client.get(reverse("student_home"))

        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "Acceso denegado", status_code=403)

    def test_each_student_only_sees_career_from_authenticated_account(self):
        first_user, first_profile = self.create_student("Carrera Primera")
        second_user, second_profile = self.create_student("Carrera Segunda")

        self.client.force_login(first_user)
        first_response = self.client.get(
            reverse("student_home"),
            {"student_id": second_profile.student_id},
        )
        self.assertContains(first_response, first_profile.career)
        self.assertNotContains(first_response, second_profile.career)
        self.assertNotContains(first_response, first_profile.student_id)
        self.assertNotContains(first_response, "Semestre")

        self.client.force_login(second_user)
        second_response = self.client.get(
            reverse("student_home"),
            {"student_id": first_profile.student_id},
        )
        self.assertContains(second_response, second_profile.career)
        self.assertNotContains(second_response, first_profile.career)
        self.assertNotContains(second_response, second_profile.student_id)
        self.assertNotContains(second_response, "Semestre")

    def test_student_home_links_to_profile(self):
        user, _ = self.create_student("Carrera con enlace al perfil")
        self.client.force_login(user)

        response = self.client.get(reverse("student_home"))

        self.assertContains(
            response,
            f'<a class="profile-link" href="{reverse("student_profile")}">'
            "Ver su perfil académico</a>",
            html=True,
        )

    def test_logout_is_post_only_and_requires_valid_csrf(self):
        user, _ = self.create_student("Carrera para cerrar sesión")
        self.client.force_login(user)

        self.assertEqual(self.client.get(reverse("logout")).status_code, 405)
        self.assertEqual(self.client.post(reverse("logout")).status_code, 403)
        self.assertIn("_auth_user_id", self.client.session)

        home_response = self.client.get(reverse("student_home"))
        csrf_token = home_response.cookies["csrftoken"].value
        response = self.client.post(
            reverse("logout"),
            {
                "csrfmiddlewaretoken": csrf_token,
                "next": "https://sitio-no-permitido.example/",
            },
        )

        self.assertRedirects(response, reverse("login"))
        self.assertNotIn("_auth_user_id", self.client.session)


@override_settings(
    PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"]
)
class RebuildSyntheticDataTests(TestCase):
    password = secrets.token_urlsafe(24)
    teacher_password = secrets.token_urlsafe(24)

    def run_command(self):
        stdout = StringIO()
        with patch.dict(
            os.environ,
            {
                "DEMO_STUDENT_PASSWORD": self.password,
                "DEMO_TEACHER_PASSWORD": self.teacher_password,
            },
        ):
            call_command("rebuild_synthetic_data", stdout=stdout)
        return stdout.getvalue()

    def test_command_requires_password_without_creating_data(self):
        with patch.dict(os.environ, {"DEMO_STUDENT_PASSWORD": ""}):
            with self.assertRaisesMessage(
                CommandError,
                "DEMO_STUDENT_PASSWORD es obligatoria.",
            ):
                call_command("rebuild_synthetic_data")

        self.assertFalse(get_user_model().objects.filter(username=DEMO_USERNAME))
        self.assertFalse(Course.objects.filter(code=PILOT_COURSE_CODE))

    def test_command_requires_teacher_password_without_creating_data(self):
        with patch.dict(
            os.environ,
            {
                "DEMO_STUDENT_PASSWORD": self.password,
                "DEMO_TEACHER_PASSWORD": "",
            },
        ):
            with self.assertRaisesMessage(
                CommandError,
                "DEMO_TEACHER_PASSWORD es obligatoria.",
            ):
                call_command("rebuild_synthetic_data")

        self.assertFalse(get_user_model().objects.filter(username=DEMO_USERNAME))
        self.assertFalse(Course.objects.filter(code=PILOT_COURSE_CODE))

    def test_command_creates_full_synthetic_dataset(self):
        output = self.run_command()

        user = get_user_model().objects.get(username=DEMO_USERNAME)
        profile = StudentProfile.objects.get(user=user)
        course = Course.objects.get(code=PILOT_COURSE_CODE)

        self.assertEqual(profile.student_id, DEMO_STUDENT_ID)
        self.assertEqual(profile.career, DEMO_CAREER)
        self.assertEqual(profile.semester, DEMO_SEMESTER)
        self.assertEqual(course.name, PILOT_COURSE_NAME)
        self.assertTrue(
            Enrollment.objects.filter(student=profile, course=course).exists()
        )
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertNotEqual(user.password, self.password)
        self.assertTrue(user.check_password(self.password))
        self.assertNotIn(self.password, output)

        self.assertEqual(StudentProfile.objects.count(), TOTAL_STUDENTS)
        self.assertEqual(
            TeacherProfile.objects.count(),
            len(DEMO_TEACHER_USERNAMES),
        )
        self.assertEqual(Course.objects.count(), len(COURSE_BLUEPRINTS))
        self.assertEqual(
            Topic.objects.count(),
            sum(
                len(blueprint["topics"])
                for blueprint in COURSE_BLUEPRINTS.values()
            ),
        )
        for code, blueprint in COURSE_BLUEPRINTS.items():
            self.assertEqual(
                Topic.objects.filter(course__code=code).count(),
                len(blueprint["topics"]),
            )
        self.assertEqual(
            set(
                Topic.objects.filter(course=course).values_list(
                    "name",
                    flat=True,
                )
            ),
            set(COURSE_BLUEPRINTS[PILOT_COURSE_CODE]["topics"]),
        )

        for username in DEMO_TEACHER_USERNAMES:
            teacher_user = get_user_model().objects.get(username=username)
            self.assertTrue(teacher_user.check_password(self.teacher_password))
            self.assertFalse(teacher_user.is_staff)
            self.assertFalse(teacher_user.is_superuser)
            self.assertEqual(
                set(
                    TeachingAssignment.objects.filter(
                        teacher__user=teacher_user
                    ).values_list("course__code", flat=True)
                ),
                set(TEACHER_ASSIGNMENTS[username]),
            )
            self.assertNotIn(self.teacher_password, output)

    def test_command_generates_distinct_grade_profiles(self):
        self.run_command()

        demo = StudentProfile.objects.get(student_id=DEMO_STUDENT_ID)
        no_weak = StudentProfile.objects.get(user__username="estudiante_01")
        no_grades = StudentProfile.objects.get(user__username="estudiante_02")

        self.assertEqual(
            Grade.objects.filter(student=demo, value__lt=60).count(),
            2,
        )
        self.assertEqual(
            Grade.objects.filter(student=no_weak, value__lt=60).count(),
            0,
        )
        self.assertFalse(Grade.objects.filter(student=no_grades).exists())

    def test_command_is_idempotent_and_preserves_unrelated_records(self):
        unrelated_user = get_user_model().objects.create_user(
            username="estudiante_ajeno",
            password=secrets.token_urlsafe(24),
            first_name="Sin cambios",
        )
        unrelated_profile = StudentProfile.objects.create(
            user=unrelated_user,
            student_id="2024-99999",
            career="Carrera ajena",
            semester=4,
        )
        unrelated_course = Course.objects.create(
            code="CURSO-AJENO",
            name="Curso ajeno",
        )
        unrelated_enrollment = Enrollment.objects.create(
            student=unrelated_profile,
            course=unrelated_course,
        )
        unrelated_password_hash = unrelated_user.password

        self.run_command()
        demo_ids = (
            get_user_model().objects.get(username=DEMO_USERNAME).pk,
            StudentProfile.objects.get(student_id=DEMO_STUDENT_ID).pk,
            Course.objects.get(code=PILOT_COURSE_CODE).pk,
        )
        output = self.run_command()

        self.assertEqual(
            demo_ids,
            (
                get_user_model().objects.get(username=DEMO_USERNAME).pk,
                StudentProfile.objects.get(student_id=DEMO_STUDENT_ID).pk,
                Course.objects.get(code=PILOT_COURSE_CODE).pk,
            ),
        )
        self.assertEqual(get_user_model().objects.count(), TOTAL_STUDENTS + 3 + 1)
        self.assertEqual(StudentProfile.objects.count(), TOTAL_STUDENTS + 1)
        self.assertEqual(
            TeacherProfile.objects.count(),
            len(DEMO_TEACHER_USERNAMES),
        )
        self.assertEqual(Course.objects.count(), len(COURSE_BLUEPRINTS) + 1)
        self.assertEqual(
            Topic.objects.count(),
            sum(
                len(blueprint["topics"])
                for blueprint in COURSE_BLUEPRINTS.values()
            ),
        )
        self.assertEqual(
            Enrollment.objects.count(),
            1 + (TOTAL_STUDENTS - 1) * 2 + 1,
        )

        unrelated_user.refresh_from_db()
        unrelated_profile.refresh_from_db()
        unrelated_course.refresh_from_db()
        unrelated_enrollment.refresh_from_db()
        self.assertEqual(unrelated_user.first_name, "Sin cambios")
        self.assertEqual(unrelated_user.password, unrelated_password_hash)
        self.assertEqual(unrelated_profile.career, "Carrera ajena")
        self.assertEqual(unrelated_course.name, "Curso ajeno")
        self.assertEqual(unrelated_enrollment.student, unrelated_profile)
        self.assertNotIn(self.password, output)

    def test_command_preserves_unrelated_grade_on_managed_course(self):
        self.run_command()

        unrelated_user = get_user_model().objects.create_user(
            username="estudiante_con_nota_ajena",
            password=secrets.token_urlsafe(24),
            first_name="Nota ajena",
        )
        unrelated_profile = StudentProfile.objects.create(
            user=unrelated_user,
            student_id="2024-77777",
            career="Carrera ajena",
            semester=3,
        )
        course = Course.objects.get(code=PILOT_COURSE_CODE)
        topic = Topic.objects.filter(course=course).first()
        Enrollment.objects.create(
            student=unrelated_profile,
            course=course,
        )
        unrelated_grade = Grade.objects.create(
            student=unrelated_profile,
            topic=topic,
            value=77,
        )

        output = self.run_command()

        unrelated_user.refresh_from_db()
        unrelated_profile.refresh_from_db()
        unrelated_grade.refresh_from_db()
        self.assertEqual(unrelated_user.first_name, "Nota ajena")
        self.assertEqual(unrelated_profile.career, "Carrera ajena")
        self.assertTrue(
            Enrollment.objects.filter(
                student=unrelated_profile,
                course=course,
            ).exists()
        )
        self.assertTrue(Topic.objects.filter(pk=topic.pk).exists())
        self.assertEqual(unrelated_grade.value, 77)
        self.assertNotIn(self.password, output)

    def test_command_preserves_demo_records_outside_manifest(self):
        self.run_command()

        extra_course = Course.objects.create(
            code="CURSO-EXTRA",
            name="Curso fuera del manifiesto",
        )
        extra_topic = Topic.objects.create(
            course=extra_course,
            name="Tema fuera del manifiesto",
        )
        demo_profile = StudentProfile.objects.get(student_id=DEMO_STUDENT_ID)
        extra_enrollment = Enrollment.objects.create(
            student=demo_profile,
            course=extra_course,
        )
        extra_grade = Grade.objects.create(
            student=demo_profile,
            topic=extra_topic,
            value=88,
        )
        demo_teacher = TeacherProfile.objects.get(
            user__username=DEMO_TEACHER_USERNAMES[0]
        )
        extra_assignment = TeachingAssignment.objects.create(
            teacher=demo_teacher,
            course=extra_course,
        )

        output = self.run_command()

        self.assertTrue(
            Enrollment.objects.filter(pk=extra_enrollment.pk).exists()
        )
        self.assertEqual(Grade.objects.get(pk=extra_grade.pk).value, 88)
        self.assertTrue(
            TeachingAssignment.objects.filter(pk=extra_assignment.pk).exists()
        )
        self.assertNotIn(self.password, output)

    def test_command_preserves_records_outside_each_account_manifest(self):
        self.run_command()

        demo_profile = StudentProfile.objects.get(student_id=DEMO_STUDENT_ID)
        course = Course.objects.get(code="BD-APL")
        topic = Topic.objects.filter(course=course).first()
        extra_enrollment = Enrollment.objects.create(
            student=demo_profile,
            course=course,
        )
        extra_grade = Grade.objects.create(
            student=demo_profile,
            topic=topic,
            value=88,
        )
        demo_teacher = TeacherProfile.objects.get(
            user__username=DEMO_TEACHER_USERNAMES[0]
        )
        extra_assignment = TeachingAssignment.objects.create(
            teacher=demo_teacher,
            course=course,
        )

        self.run_command()

        self.assertTrue(
            Enrollment.objects.filter(pk=extra_enrollment.pk).exists()
        )
        self.assertEqual(Grade.objects.get(pk=extra_grade.pk).value, 88)
        self.assertTrue(
            TeachingAssignment.objects.filter(pk=extra_assignment.pk).exists()
        )

    def test_command_rejects_profile_outside_manifest_for_demo_user(self):
        user = get_user_model().objects.create_user(
            username=DEMO_USERNAME,
            password=secrets.token_urlsafe(24),
            first_name="Nombre original",
        )
        profile = StudentProfile.objects.create(
            user=user,
            student_id="2023-88888",
            career="Carrera original",
            semester=5,
        )
        original_password_hash = user.password

        with self.assertRaisesMessage(
            CommandError,
            "La cuenta sintética existente no coincide con el manifiesto.",
        ):
            self.run_command()

        user.refresh_from_db()
        profile.refresh_from_db()
        self.assertEqual(user.first_name, "Nombre original")
        self.assertEqual(user.password, original_password_hash)
        self.assertEqual(profile.student_id, "2023-88888")
        self.assertEqual(profile.career, "Carrera original")
        self.assertFalse(Course.objects.filter(code=PILOT_COURSE_CODE).exists())

    def test_command_rejects_student_id_owned_by_unrelated_profile(self):
        unrelated_user = get_user_model().objects.create_user(
            username="propietario_ajeno",
            password=secrets.token_urlsafe(24),
        )
        StudentProfile.objects.create(
            user=unrelated_user,
            student_id=DEMO_STUDENT_ID,
            career="Carrera ajena",
            semester=6,
        )

        with self.assertRaisesMessage(
            CommandError,
            "El carné sintético ya pertenece a un perfil fuera del manifiesto.",
        ):
            self.run_command()

        self.assertFalse(get_user_model().objects.filter(username=DEMO_USERNAME))
        self.assertFalse(Course.objects.filter(code=PILOT_COURSE_CODE).exists())

    def test_command_rejects_demo_username_without_profile_unchanged(self):
        user = get_user_model().objects.create_user(
            username=DEMO_USERNAME,
            password=secrets.token_urlsafe(24),
            first_name="Nombre original",
            last_name="Apellido original",
            is_active=False,
        )
        original_state = (
            user.password,
            user.first_name,
            user.last_name,
            user.is_active,
            user.is_staff,
            user.is_superuser,
        )

        with self.assertRaisesMessage(
            CommandError,
            "La cuenta sintética existente no coincide con el manifiesto.",
        ):
            self.run_command()

        user.refresh_from_db()
        self.assertEqual(
            (
                user.password,
                user.first_name,
                user.last_name,
                user.is_active,
                user.is_staff,
                user.is_superuser,
            ),
            original_state,
        )
        self.assertFalse(StudentProfile.objects.filter(user=user).exists())
        self.assertFalse(Course.objects.filter(code=PILOT_COURSE_CODE).exists())

    def test_command_rejects_privileged_demo_username_unchanged(self):
        for privilege in ("is_staff", "is_superuser"):
            with self.subTest(privilege=privilege):
                user = get_user_model().objects.create_user(
                    username=DEMO_USERNAME,
                    password=secrets.token_urlsafe(24),
                    first_name="Nombre privilegiado",
                    last_name="Apellido privilegiado",
                    **{privilege: True},
                )
                StudentProfile.objects.create(
                    user=user,
                    student_id=DEMO_STUDENT_ID,
                    career="Carrera privilegiada",
                    semester=7,
                )
                original_state = (
                    user.password,
                    user.first_name,
                    user.last_name,
                    user.is_staff,
                    user.is_superuser,
                )

                with self.assertRaisesMessage(
                    CommandError,
                    "La cuenta sintética existente tiene privilegios.",
                ):
                    self.run_command()

                user.refresh_from_db()
                self.assertEqual(
                    (
                        user.password,
                        user.first_name,
                        user.last_name,
                        user.is_staff,
                        user.is_superuser,
                    ),
                    original_state,
                )
                self.assertFalse(
                    Course.objects.filter(code=PILOT_COURSE_CODE).exists()
                )

                StudentProfile.objects.filter(user=user).delete()
                user.delete()


class PanelFixtureMixin:
    def setUp(self):
        self.course = Course.objects.create(code="S008-CURSO", name="Curso del panel")
        self.other_course = Course.objects.create(
            code="S008-OTRO", name="Curso ajeno"
        )
        self.topics = [
            Topic.objects.create(course=self.course, name=name)
            for name in ("Variables", "Condicionales", "Ciclos")
        ]
        self.teacher_user = get_user_model().objects.create_user(
            username="docente_panel_s008",
            password=secrets.token_urlsafe(24),
        )
        self.teacher = TeacherProfile.objects.create(user=self.teacher_user)
        TeachingAssignment.objects.create(teacher=self.teacher, course=self.course)
        self.student_number = 0

    def create_student(self, *, courses=(), first_name="", last_name=""):
        self.student_number += 1
        user = get_user_model().objects.create_user(
            username=f"panel_{self.student_number}",
            password=secrets.token_urlsafe(24),
            first_name=first_name,
            last_name=last_name,
        )
        profile = StudentProfile.objects.create(
            user=user,
            student_id=f"2026-3{self.student_number:04d}",
            career="Carrera Sintética",
            semester=2,
        )
        for course in courses:
            Enrollment.objects.create(student=profile, course=course)
        return user, profile

    def set_grades(self, profile, values):
        for topic, value in zip(self.topics, values):
            if value is not None:
                Grade.objects.create(student=profile, topic=topic, value=value)


class IsWeakTests(SimpleTestCase):
    def test_grade_below_threshold_is_weak(self):
        self.assertTrue(is_weak(59))

    def test_grade_at_threshold_is_not_weak(self):
        self.assertFalse(is_weak(60))

    def test_grade_above_threshold_is_not_weak(self):
        self.assertFalse(is_weak(100))

    def test_missing_grade_is_never_weak(self):
        self.assertFalse(is_weak(None))

    @override_settings(WEAK_TOPIC_THRESHOLD=70)
    def test_threshold_is_configurable(self):
        self.assertTrue(is_weak(69))
        self.assertFalse(is_weak(70))


class GetCoursePanelTests(PanelFixtureMixin, TestCase):
    def test_rows_include_average_and_weak_topics(self):
        _, ana = self.create_student(first_name="Ana", courses=[self.course])
        self.set_grades(ana, [80, 55, 60])
        panel = get_course_panel(self.course)
        self.assertEqual(len(panel.rows), 1)
        row = panel.rows[0]
        self.assertEqual(row.average, Decimal("65.00"))
        self.assertEqual(
            [topic.name for topic in row.weak_topics], ["Condicionales"]
        )

    def test_topic_weak_counts_count_only_weak_students(self):
        _, ana = self.create_student(courses=[self.course])
        self.set_grades(ana, [80, 55, 55])
        _, luis = self.create_student(courses=[self.course])
        self.set_grades(luis, [50, 70, 59])
        panel = get_course_panel(self.course)
        counts = {
            item.topic.name: item.weak_count for item in panel.topic_weak_counts
        }
        self.assertEqual(counts, {"Variables": 1, "Condicionales": 1, "Ciclos": 2})

    def test_student_without_grades_has_no_average_and_no_weak_topics(self):
        self.create_student(courses=[self.course])
        panel = get_course_panel(self.course)
        row = panel.rows[0]
        self.assertIsNone(row.average)
        self.assertEqual(row.weak_topics, ())
        self.assertEqual({item.weak_count for item in panel.topic_weak_counts}, {0})

    def test_unenrolled_students_are_excluded(self):
        _, inscrito = self.create_student(courses=[self.course])
        self.set_grades(inscrito, [80, 80, 80])
        _, externo = self.create_student(courses=[self.other_course])
        self.set_grades(externo, [10, 10, 10])
        panel = get_course_panel(self.course)
        self.assertEqual([row.student.pk for row in panel.rows], [inscrito.pk])
        self.assertEqual({item.weak_count for item in panel.topic_weak_counts}, {0})

    def test_student_panel_row_returns_row_or_none(self):
        _, ana = self.create_student(courses=[self.course])
        self.set_grades(ana, [80, 55, 60])
        _, externo = self.create_student(courses=[self.other_course])
        row = get_student_panel_row(self.course, ana)
        self.assertEqual(row.average, Decimal("65.00"))
        self.assertIsNone(get_student_panel_row(self.course, externo))

    def test_taught_courses_only_include_assigned_courses(self):
        self.assertEqual(get_taught_courses(self.teacher), [self.course])

    def test_get_weak_topics_keeps_order_and_ignores_missing_grades(self):
        items = (
            TopicGrade(topic=self.topics[0], value=59),
            TopicGrade(topic=self.topics[1], value=None),
            TopicGrade(topic=self.topics[2], value=60),
        )
        self.assertEqual(get_weak_topics(items), (self.topics[0],))


class TeacherPanelViewTests(PanelFixtureMixin, TestCase):
    def get_panel(self, *, code=None, user=None, **params):
        self.client.force_login(user or self.teacher_user)
        code = self.course.code if code is None else code
        return self.client.get(reverse("teacher_course_panel", args=[code]), params)

    def get_student_detail(self, student_profile, *, code=None, user=None):
        self.client.force_login(user or self.teacher_user)
        code = self.course.code if code is None else code
        return self.client.get(
            reverse("teacher_student_detail", args=[code, student_profile.pk])
        )

    def test_anonymous_access_redirects_to_login(self):
        for url_name, args in (
            ("teacher_panel", None),
            ("teacher_course_panel", (self.course.code,)),
            ("teacher_student_detail", (self.course.code, 1)),
        ):
            with self.subTest(pantalla=url_name):
                url = reverse(url_name, args=args)
                response = self.client.get(url)
                self.assertRedirects(
                    response,
                    f"{reverse('login')}?next={url}",
                )

    def test_accounts_without_teacher_profile_are_denied(self):
        user, student = self.create_student(courses=[self.course])
        accounts = {
            "estudiante": user,
            "sin perfil": get_user_model().objects.create_user(username="sin_s008"),
            "personal técnico": get_user_model().objects.create_user(
                username="staff_s008",
                is_staff=True,
            ),
        }
        for label, account in accounts.items():
            with self.subTest(cuenta=label):
                self.client.force_login(account)
                for url in (
                    reverse("teacher_panel"),
                    reverse("teacher_course_panel", args=[self.course.code]),
                    reverse(
                        "teacher_student_detail",
                        args=[self.course.code, student.pk],
                    ),
                ):
                    response = self.client.get(url)
                    self.assertContains(
                        response,
                        "Su cuenta no tiene autorización académica",
                        status_code=403,
                    )
            self.client.logout()

    def test_ca1_lists_enrolled_students_with_average_and_weak_topics(self):
        _, ana = self.create_student(
            first_name="Ana", last_name="Ruiz", courses=[self.course]
        )
        self.set_grades(ana, [80, 55, 60])
        _, luis = self.create_student(
            first_name="Luis", last_name="Paz", courses=[self.course]
        )
        self.set_grades(luis, [70, 65, 58])
        response = self.get_panel()
        self.assertContains(response, "Ana Ruiz")
        self.assertContains(response, "65.00")
        self.assertContains(response, "Luis Paz")
        self.assertContains(response, "64.33")
        self.assertContains(response, "Condicionales")
        self.assertContains(response, "Ciclos")

    def test_ca2_order_by_average_changes_order(self):
        _, alta = self.create_student(first_name="Alta", courses=[self.course])
        self.set_grades(alta, [90, 90, 90])
        _, baja = self.create_student(first_name="Baja", courses=[self.course])
        self.set_grades(baja, [60, 60, 60])
        desc = self.get_panel(orden="promedio-desc")
        asc = self.get_panel(orden="promedio-asc")
        self.assertLess(desc.content.index(b"Alta"), desc.content.index(b"Baja"))
        self.assertLess(asc.content.index(b"Baja"), asc.content.index(b"Alta"))

    def test_default_order_sorts_by_name(self):
        _, zoe = self.create_student(first_name="Zoe", courses=[self.course])
        self.set_grades(zoe, [80, 80, 80])
        self.create_student(first_name="Ana", courses=[self.course])
        response = self.get_panel()
        self.assertLess(response.content.index(b"Ana"), response.content.index(b"Zoe"))

    def test_ca2_students_without_average_stay_last(self):
        _, con_notas = self.create_student(first_name="Zoe", courses=[self.course])
        self.set_grades(con_notas, [80, 80, 80])
        self.create_student(first_name="Ana", courses=[self.course])
        for order in ("promedio-asc", "promedio-desc"):
            with self.subTest(orden=order):
                response = self.get_panel(orden=order)
                self.assertLess(
                    response.content.index(b"Zoe"),
                    response.content.index(b"Ana"),
                )

    def test_ca3_student_detail_shows_average_and_weak_topics(self):
        _, ana = self.create_student(first_name="Ana", courses=[self.course])
        self.set_grades(ana, [80, 55, 60])
        response = self.get_student_detail(ana)
        self.assertContains(response, "Ana")
        self.assertContains(response, ana.student_id)
        self.assertContains(response, "65.00")
        self.assertContains(response, "Condicionales")

    def test_ca4_topic_breakdown_shows_weak_counts(self):
        _, ana = self.create_student(courses=[self.course])
        self.set_grades(ana, [80, 55, 55])
        _, luis = self.create_student(courses=[self.course])
        self.set_grades(luis, [50, 70, 59])
        response = self.get_panel()
        counts = {
            item.topic.name: item.weak_count
            for item in response.context["topic_weak_counts"]
        }
        self.assertEqual(counts, {"Variables": 1, "Condicionales": 1, "Ciclos": 2})
        self.assertContains(response, "Temas débiles por tema")

    def test_ca5_unassigned_course_is_denied(self):
        response = self.get_panel(code=self.other_course.code)
        self.assertContains(
            response,
            "Su cuenta no tiene autorización académica",
            status_code=403,
        )

    def test_ca5_course_of_another_teacher_is_denied(self):
        other_user = get_user_model().objects.create_user(
            username="docente_ajeno_s008",
            password=secrets.token_urlsafe(24),
        )
        other_teacher = TeacherProfile.objects.create(user=other_user)
        TeachingAssignment.objects.create(
            teacher=other_teacher, course=self.other_course
        )
        response = self.get_panel(code=self.other_course.code)
        self.assertContains(
            response,
            "Su cuenta no tiene autorización académica",
            status_code=403,
        )

    def test_ca5_student_of_another_course_is_denied(self):
        _, externo = self.create_student(courses=[self.other_course])
        response = self.get_student_detail(externo)
        self.assertContains(
            response,
            "Su cuenta no tiene autorización académica",
            status_code=403,
        )

    def test_teacher_panel_lists_only_taught_courses(self):
        self.client.force_login(self.teacher_user)
        response = self.client.get(reverse("teacher_panel"))
        self.assertContains(response, "Curso del panel")
        self.assertNotContains(response, "Curso ajeno")

    def test_teacher_without_courses_sees_notice(self):
        other_user = get_user_model().objects.create_user(
            username="docente_sin_cursos",
            password=secrets.token_urlsafe(24),
        )
        TeacherProfile.objects.create(user=other_user)
        self.client.force_login(other_user)
        response = self.client.get(reverse("teacher_panel"))
        self.assertContains(response, "Aún no tiene cursos asignados.")

    def test_panel_views_only_accept_get(self):
        self.client.force_login(self.teacher_user)
        for url in (
            reverse("teacher_panel"),
            reverse("teacher_course_panel", args=[self.course.code]),
        ):
            with self.subTest(pantalla=url):
                self.assertEqual(self.client.post(url).status_code, 405)


class RoleHomeTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="rol_s008",
            password=secrets.token_urlsafe(24),
        )

    def test_anonymous_access_redirects_to_login(self):
        response = self.client.get(reverse("role_home"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('role_home')}",
        )

    def test_student_is_redirected_to_student_home(self):
        StudentProfile.objects.create(
            user=self.user,
            student_id="2026-40001",
            career="Carrera Sintética",
            semester=1,
        )
        self.client.force_login(self.user)
        response = self.client.get(reverse("role_home"))
        self.assertRedirects(
            response,
            reverse("student_home"),
            fetch_redirect_response=False,
        )

    def test_teacher_is_redirected_to_teacher_panel(self):
        TeacherProfile.objects.create(user=self.user)
        self.client.force_login(self.user)
        response = self.client.get(reverse("role_home"))
        self.assertRedirects(
            response,
            reverse("teacher_panel"),
            fetch_redirect_response=False,
        )

    def test_user_without_profile_is_denied(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("role_home"))
        self.assertContains(
            response,
            "Su cuenta no tiene autorización académica",
            status_code=403,
        )
