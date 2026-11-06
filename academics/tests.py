import os
import secrets
from io import StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import IntegrityError, transaction
from django.test import TestCase

from academics.management.commands.rebuild_synthetic_data import (
    DEMO_CAREER,
    DEMO_SEMESTER,
    DEMO_STUDENT_ID,
    DEMO_USERNAME,
    PILOT_COURSE_CODE,
    PILOT_COURSE_NAME,
)
from academics.models import Course, Enrollment, StudentProfile


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


class RebuildSyntheticDataTests(TestCase):
    password = secrets.token_urlsafe(24)

    def run_command(self):
        stdout = StringIO()
        with patch.dict(os.environ, {"DEMO_STUDENT_PASSWORD": self.password}):
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

    def test_command_creates_exact_minimum_with_hashed_password(self):
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
        self.assertEqual(get_user_model().objects.count(), 2)
        self.assertEqual(StudentProfile.objects.count(), 2)
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(Enrollment.objects.count(), 2)

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
