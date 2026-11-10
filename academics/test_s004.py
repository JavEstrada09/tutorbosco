
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from academics.models import (
    Course,
    TeacherProfile,
    TeachingAssignment,
)


class S004TeacherCoursesTests(TestCase):
    """
    S-004: Pruebas del listado de cursos del docente.
    """

    def setUp(self):
        user_model = get_user_model()

        self.teacher_user = user_model.objects.create_user(
            username="docente_s004",
            password="PruebaSegura123!",
        )

        self.teacher = TeacherProfile.objects.create(
            user=self.teacher_user,
        )

        self.other_user = user_model.objects.create_user(
            username="usuario_s004",
            password="PruebaSegura456!",
        )

        self.course = Course.objects.create(
            code="PROG-COM",
            name="Programación Comercial",
        )

        self.other_course = Course.objects.create(
            code="BD-III",
            name="Base de Datos III",
        )

        TeachingAssignment.objects.create(
            teacher=self.teacher,
            course=self.course,
        )

        self.url = reverse("teacher_courses")

    def test_teacher_sees_only_assigned_courses(self):
        self.client.force_login(self.teacher_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Programación Comercial")
        self.assertNotContains(response, "Base de Datos III")

    def test_user_without_teacher_profile_gets_403(self):
        self.client.force_login(self.other_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(
            response,
            "academics/access_denied.html",
        )

    def test_anonymous_user_must_login(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("next=", response.url)

    def test_teacher_with_no_courses_sees_empty_state(self):
        user_model = get_user_model()

        another_teacher_user = user_model.objects.create_user(
            username="docente_sin_cursos",
            password="PruebaSegura789!",
        )

        TeacherProfile.objects.create(
            user=another_teacher_user,
        )

        self.client.force_login(another_teacher_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "No tiene cursos asignados",
        )

    def test_teacher_can_navigate_to_topics_and_students(self):
        self.client.force_login(self.teacher_user)

        response = self.client.get(self.url)

        topics_url = reverse(
            "teacher_course_topics",
            kwargs={"course_code": self.course.code},
        )

        students_url = reverse(
            "teacher_course_students",
            kwargs={"course_code": self.course.code},
        )

        self.assertContains(response, topics_url)
        self.assertContains(response, students_url)
