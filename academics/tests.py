import os
import secrets
from io import StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import IntegrityError, transaction
from django.test import Client, TestCase, override_settings
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

    def test_student_without_pilot_enrollment_is_denied(self):
        user, _ = self.create_student("Carrera sin inscripción", enrolled=False)
        self.client.force_login(user)

        response = self.client.get(reverse("student_home"))

        self.assertEqual(response.status_code, 403)
        self.assertNotContains(response, "Carrera sin inscripción", status_code=403)

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
