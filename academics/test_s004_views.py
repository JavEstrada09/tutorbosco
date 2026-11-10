
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from academics.models import (
    Course,
    Enrollment,
    StudentProfile,
    TeacherProfile,
    TeachingAssignment,
    Topic,
)


class S004TeacherViewsTests(TestCase):

    def setUp(self):
        user_model = get_user_model()

        self.user = user_model.objects.create_user(
            username="docente_vistas_s004",
            password="PruebaSegura123!",
        )

        teacher = TeacherProfile.objects.create(
            user=self.user
        )

        self.course = Course.objects.create(
            code="PROG-COM",
            name="Programación Comercial",
        )

        TeachingAssignment.objects.create(
            teacher=teacher,
            course=self.course,
        )

        student_user = user_model.objects.create_user(
            username="estudiante_vistas_s004",
            password="PruebaSegura456!",
        )

        self.student = StudentProfile.objects.create(
            user=student_user,
            student_id="2026-00002",
            career="Ingeniería en Sistemas",
            semester=8,
        )

        self.topics_url = reverse(
            "teacher_course_topics",
            kwargs={"course_code": self.course.code},
        )

        self.students_url = reverse(
            "teacher_course_students",
            kwargs={"course_code": self.course.code},
        )

        self.client.force_login(self.user)

    def request_with_course(
        self, url, data=None, authorized=True, follow=False
    ):
        course = self.course if authorized else None

        with patch(
            "academics.services.get_taught_course",
            return_value=course,
            create=True,
        ):
            if data is None:
                return self.client.get(url)

            return self.client.post(url, data, follow=follow)

    # CA-2: Consultar temas
    def test_view_lists_topics(self):
        Topic.objects.create(
            course=self.course,
            name="Variables",
        )
        other_course = Course.objects.create(
            code="BD-APL",
            name="Bases de Datos Aplicadas",
        )
        Topic.objects.create(
            course=other_course,
            name="Tema de otro curso",
        )

        response = self.request_with_course(
            self.topics_url
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Variables")
        self.assertNotContains(response, "Tema de otro curso")

    # CA-3: Crear temas
    def test_view_creates_topic(self):
        response = self.request_with_course(
            self.topics_url,
            {
                "action": "create",
                "name": "Estructuras de datos",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "El tema académico se registró correctamente.",
        )
        self.assertContains(response, "Estructuras de datos")
        self.assertTrue(
            Topic.objects.filter(
                course=self.course,
                name="Estructuras de datos",
            ).exists()
        )

    # CA-4: Modificar temas
    def test_view_updates_topic(self):
        topic = Topic.objects.create(
            course=self.course,
            name="Variables",
        )

        response = self.request_with_course(
            self.topics_url,
            {
                "action": "update",
                "topic_id": topic.pk,
                "name": "Variables avanzadas",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "El tema académico se actualizó correctamente.",
        )
        self.assertContains(response, "Variables avanzadas")
        topic.refresh_from_db()
        self.assertEqual(
            topic.name, "Variables avanzadas"
        )

    # CA-5: Asignar estudiantes
    def test_view_enrolls_student(self):
        response = self.request_with_course(
            self.students_url,
            {
                "action": "enroll",
                "student": self.student.pk,
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "El estudiante fue asignado correctamente.",
        )
        self.assertContains(response, self.student.student_id)
        self.assertEqual(
            Enrollment.objects.filter(
                student=self.student,
                course=self.course,
            ).count(),
            1,
        )

    # CA-6: Evitar asignaciones duplicadas
    def test_view_prevents_duplicate_enrollment(self):
        Enrollment.objects.create(
            student=self.student,
            course=self.course,
        )

        response = self.request_with_course(
            self.students_url,
            {
                "action": "enroll",
                "student": self.student.pk,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Este estudiante ya está asignado a este curso.",
        )
        self.assertEqual(
            Enrollment.objects.filter(
                student=self.student,
                course=self.course,
            ).count(),
            1,
        )

    # CA-7: Rechazar acceso sin autorización
    def test_topics_reject_unauthorized_access(self):
        response = self.request_with_course(
            self.topics_url,
            authorized=False,
        )

        self.assertEqual(response.status_code, 403)

    def test_students_reject_unauthorized_access(self):
        response = self.request_with_course(
            self.students_url,
            authorized=False,
        )

        self.assertEqual(response.status_code, 403)

    # CA-8: No guardar temas inválidos
    def test_view_rejects_empty_topic(self):
        response = self.request_with_course(
            self.topics_url,
            {
                "action": "create",
                "name": "   ",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "El nombre del tema es obligatorio.")
        self.assertEqual(
            Topic.objects.filter(
                course=self.course
            ).count(),
            0,
        )

    def test_view_preserves_invalid_topic_update(self):
        Topic.objects.create(
            course=self.course,
            name="Variables",
        )
        topic = Topic.objects.create(
            course=self.course,
            name="Condicionales",
        )

        response = self.request_with_course(
            self.topics_url,
            {
                "action": "update",
                "topic_id": topic.pk,
                "name": "Variables",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Este tema ya está registrado en el curso.",
        )
        self.assertContains(response, 'value="Variables"', html=False)
        topic.refresh_from_db()
        self.assertEqual(topic.name, "Condicionales")
