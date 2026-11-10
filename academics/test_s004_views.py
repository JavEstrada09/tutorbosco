
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
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

        self.student_user = user_model.objects.create_user(
            username="estudiante_vistas_s004",
            password="PruebaSegura456!",
        )

        self.student = StudentProfile.objects.create(
            user=self.student_user,
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

    def request_with_course(self, url, data=None, follow=False):
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
        other_user = get_user_model().objects.create_user(
            username="docente_ajeno_s004",
            password="PruebaSegura789!",
        )
        TeacherProfile.objects.create(user=other_user)
        self.client.force_login(other_user)

        response = self.client.get(self.topics_url)

        self.assertEqual(response.status_code, 403)

    def test_students_reject_unauthorized_access(self):
        self.client.force_login(self.student_user)

        response = self.client.get(self.students_url)

        self.assertEqual(response.status_code, 403)

    def test_nonexistent_course_returns_403(self):
        topics_url = reverse(
            "teacher_course_topics",
            kwargs={"course_code": "NO-EXISTE"},
        )
        students_url = reverse(
            "teacher_course_students",
            kwargs={"course_code": "NO-EXISTE"},
        )

        self.assertEqual(self.client.get(topics_url).status_code, 403)
        self.assertEqual(self.client.get(students_url).status_code, 403)

    def test_unauthorized_posts_do_not_modify_data(self):
        other_user = get_user_model().objects.create_user(
            username="docente_post_ajeno_s004",
            password="PruebaSegura789!",
        )
        TeacherProfile.objects.create(user=other_user)
        self.client.force_login(other_user)

        topics_response = self.client.post(
            self.topics_url,
            {"action": "create", "name": "Tema restringido"},
        )
        students_response = self.client.post(
            self.students_url,
            {"action": "enroll", "student": self.student.pk},
        )

        self.assertEqual(topics_response.status_code, 403)
        self.assertEqual(students_response.status_code, 403)
        self.assertFalse(
            Topic.objects.filter(
                course=self.course,
                name="Tema restringido",
            ).exists()
        )
        self.assertFalse(
            Enrollment.objects.filter(
                course=self.course,
                student=self.student,
            ).exists()
        )

    def test_anonymous_user_must_login(self):
        self.client.logout()

        for url in (self.topics_url, self.students_url):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertIn("next=", response.url)

    def test_post_requires_csrf_token(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.user)

        response = csrf_client.post(
            self.topics_url,
            {"action": "create", "name": "Tema sin CSRF"},
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(
            Topic.objects.filter(
                course=self.course,
                name="Tema sin CSRF",
            ).exists()
        )

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
