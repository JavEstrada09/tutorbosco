import secrets

from django.contrib.auth import get_user_model
from django.test import TestCase


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
