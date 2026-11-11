import secrets

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from accounts.forms import GENERIC_LOGIN_ERROR
from academics.models import (
    Course,
    Enrollment,
    StudentProfile,
    TeacherProfile,
    TeachingAssignment,
)


class UserModelTests(TestCase):
    def test_configured_user_uses_django_password_hash(self):
        password = secrets.token_urlsafe(24)
        user = get_user_model().objects.create_user(
            username="usuario_prueba",
            password=password,
        )

        self.assertEqual(user._meta.label, "accounts.User")
        self.assertNotEqual(user.password, password)
        self.assertTrue(user.check_password(password))


class AuthenticationViewTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.password = secrets.token_urlsafe(24)
        self.user = get_user_model().objects.create_user(
            username="estudiante_login",
            password=self.password,
        )
        self.career = "Carrera de integración"
        profile = StudentProfile.objects.create(
            user=self.user,
            student_id="2026-30001",
            career=self.career,
            semester=3,
        )
        course = Course.objects.create(
            code="PROG-COM",
            name="Programación Comercial",
        )
        Enrollment.objects.create(student=profile, course=course)

    def login_token(self, client=None):
        client = client or self.client
        response = client.get(reverse("login"))
        return response.cookies["csrftoken"].value

    def test_login_correct_authenticates_and_redirects(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": self.user.username,
                "password": self.password,
                "csrfmiddlewaretoken": self.login_token(),
            },
        )

        self.assertRedirects(
            response,
            reverse("role_home"),
            fetch_redirect_response=False,
        )
        self.assertEqual(
            self.client.session.get("_auth_user_id"),
            str(self.user.pk),
        )
        home_response = self.client.get(reverse("student_home"))
        self.assertEqual(home_response.status_code, 200)
        self.assertContains(home_response, self.career)

    def test_login_ignores_unsafe_external_next_url(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": self.user.username,
                "password": self.password,
                "next": "https://sitio-no-permitido.example/",
                "csrfmiddlewaretoken": self.login_token(),
            },
        )

        self.assertRedirects(
            response,
            reverse("role_home"),
            fetch_redirect_response=False,
        )

    def test_wrong_password_and_unknown_user_share_generic_error(self):
        attempts = (
            (self.user.username, secrets.token_urlsafe(24)),
            ("usuario_inexistente", secrets.token_urlsafe(24)),
        )

        for username, password in attempts:
            with self.subTest(username=username):
                client = Client(enforce_csrf_checks=True)
                response = client.post(
                    reverse("login"),
                    {
                        "username": username,
                        "password": password,
                        "csrfmiddlewaretoken": self.login_token(client),
                    },
                )

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, GENERIC_LOGIN_ERROR)
                self.assertNotIn("_auth_user_id", client.session)

    def test_inactive_user_receives_same_generic_error(self):
        self.user.is_active = False
        self.user.save(update_fields=["is_active"])

        response = self.client.post(
            reverse("login"),
            {
                "username": self.user.username,
                "password": self.password,
                "csrfmiddlewaretoken": self.login_token(),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, GENERIC_LOGIN_ERROR)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_post_without_csrf_is_rejected(self):
        response = self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": self.password},
        )

        self.assertEqual(response.status_code, 403)
        self.assertNotIn("_auth_user_id", self.client.session)


class AccessSecurityTests(TestCase):
    def setUp(self):
        self.password = secrets.token_urlsafe(24)
        self.course = Course.objects.create(
            code="SEG-WEB",
            name="Seguridad Web",
        )

    def create_student(self, username="estudiante_seguridad"):
        user = get_user_model().objects.create_user(
            username=username,
            password=self.password,
        )
        profile = StudentProfile.objects.create(
            user=user,
            student_id=f"2026-{user.pk:05d}",
            career="Ingeniería en Sistemas",
            semester=8,
        )
        Enrollment.objects.create(student=profile, course=self.course)
        return user

    def create_teacher(self, username="docente_seguridad"):
        user = get_user_model().objects.create_user(
            username=username,
            password=self.password,
        )
        profile = TeacherProfile.objects.create(user=user)
        TeachingAssignment.objects.create(teacher=profile, course=self.course)
        return user

    def test_teacher_login_reaches_teacher_panel(self):
        teacher = self.create_teacher()
        login_page = self.client.get(reverse("login"))

        response = self.client.post(
            reverse("login"),
            {
                "username": teacher.username,
                "password": self.password,
                "csrfmiddlewaretoken": login_page.cookies["csrftoken"].value,
            },
        )

        self.assertRedirects(
            response,
            reverse("role_home"),
            fetch_redirect_response=False,
        )
        self.assertRedirects(
            self.client.get(reverse("role_home")),
            reverse("teacher_panel"),
            fetch_redirect_response=False,
        )

    def test_navigation_only_shows_options_for_available_profile(self):
        student = self.create_student()
        self.client.force_login(student)
        student_response = self.client.get(reverse("student_home"))

        self.assertContains(student_response, reverse("role_home"))
        self.assertContains(student_response, reverse("student_profile"))
        self.assertNotContains(student_response, reverse("teacher_courses"))

        self.client.logout()
        teacher = self.create_teacher()
        self.client.force_login(teacher)
        teacher_response = self.client.get(reverse("teacher_panel"))

        self.assertContains(teacher_response, reverse("role_home"))
        self.assertContains(teacher_response, reverse("teacher_courses"))
        self.assertNotContains(teacher_response, reverse("student_profile"))

    def test_dual_profile_keeps_student_priority_and_both_navigation_groups(self):
        user = self.create_student("perfil_dual")
        teacher = TeacherProfile.objects.create(user=user)
        TeachingAssignment.objects.create(teacher=teacher, course=self.course)
        self.client.force_login(user)

        self.assertRedirects(
            self.client.get(reverse("role_home")),
            reverse("student_home"),
            fetch_redirect_response=False,
        )
        response = self.client.get(reverse("student_home"))
        self.assertContains(response, reverse("student_profile"))
        self.assertContains(response, reverse("teacher_panel"))
        self.assertContains(response, reverse("teacher_courses"))

    def test_private_entry_routes_redirect_anonymous_user_to_login(self):
        private_routes = (
            "student_home",
            "student_profile",
            "role_home",
            "teacher_panel",
            "teacher_courses",
        )

        for route_name in private_routes:
            with self.subTest(route_name=route_name):
                url = reverse(route_name)
                self.assertRedirects(
                    self.client.get(url),
                    f"{reverse('login')}?next={url}",
                    fetch_redirect_response=False,
                )

    def test_common_logout_requires_post_and_csrf_then_blocks_private_page(self):
        student = self.create_student()
        client = Client(enforce_csrf_checks=True)
        client.force_login(student)
        home_response = client.get(reverse("student_home"))
        csrf_token = home_response.cookies["csrftoken"].value

        self.assertContains(home_response, "Cerrar sesión")
        self.assertEqual(client.get(reverse("logout")).status_code, 405)
        self.assertEqual(client.post(reverse("logout")).status_code, 403)
        response = client.post(
            reverse("logout"),
            {"csrfmiddlewaretoken": csrf_token},
        )

        self.assertRedirects(response, reverse("login"))
        self.assertRedirects(
            client.get(reverse("student_home")),
            f"{reverse('login')}?next={reverse('student_home')}",
            fetch_redirect_response=False,
        )

    def test_bootstrap_is_loaded_from_local_static_path(self):
        response = self.client.get(reverse("login"))

        self.assertContains(response, "/static/css/bootstrap.min.css")
        self.assertNotContains(response, "cdn.jsdelivr.net")
