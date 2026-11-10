
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
from academics.teacher_forms import (
    StudentEnrollmentForm,
    TopicForm,
)


# =====================================================
# S-004: PRUEBAS DEL MÓDULO DOCENTE
# =====================================================

class S004TeacherCoursesTests(TestCase):

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

    # =================================================
    # CA-1: MOSTRAR SOLO CURSOS ASIGNADOS
    # =================================================

    def test_teacher_sees_only_assigned_courses(self):
        self.client.force_login(self.teacher_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Programación Comercial",
        )
        self.assertNotContains(
            response,
            "Base de Datos III",
        )

    # =================================================
    # CA-7: RECHAZAR USUARIOS SIN PERMISOS
    # =================================================

    def test_user_without_teacher_profile_gets_403(self):
        self.client.force_login(self.other_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(
            response,
            "academics/access_denied.html",
        )

    # =================================================
    # SEGURIDAD: USUARIO SIN AUTENTICACIÓN
    # =================================================

    def test_anonymous_user_must_login(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("next=", response.url)

    # =================================================
    # CA-1: DOCENTE SIN CURSOS ASIGNADOS
    # =================================================

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

    # =================================================
    # NAVEGACIÓN HACIA TEMAS, ESTUDIANTES Y NOTAS
    # =================================================

    def test_teacher_can_navigate_to_course_management(self):
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
        grades_url = reverse(
            "teacher_course_grades",
            kwargs={"course_code": self.course.code},
        )

        self.assertContains(response, topics_url)
        self.assertContains(response, students_url)
        self.assertContains(response, grades_url)

    # =================================================
    # CA-8: RECHAZAR TEMAS DUPLICADOS
    # =================================================

    def test_topic_form_rejects_duplicate_name(self):
        Topic.objects.create(
            course=self.course,
            name="Variables",
        )

        form = TopicForm(
            data={"name": "Variables"},
            course=self.course,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    # =================================================
    # CA-8: RECHAZAR NOMBRES VACÍOS
    # =================================================

    def test_topic_form_rejects_empty_name(self):
        form = TopicForm(
            data={"name": "   "},
            course=self.course,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    # =================================================
    # CA-6: EVITAR INSCRIPCIONES DUPLICADAS
    # =================================================

    def test_student_enrollment_form_rejects_duplicate(self):
        user_model = get_user_model()

        student_user = user_model.objects.create_user(
            username="estudiante_s004",
            password="PruebaSegura123!",
        )

        student = StudentProfile.objects.create(
            user=student_user,
            student_id="2026-00001",
            career="Ingeniería en Sistemas",
            semester=8,
        )

        Enrollment.objects.create(
            student=student,
            course=self.course,
        )

        form = StudentEnrollmentForm(
            data={"student": student.pk},
            course=self.course,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("student", form.errors)
