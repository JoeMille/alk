from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")

        self.assertNotEqual(user.password, "testpass123")

        self.assertTrue(user.check_password("testpass123"))

        self.assertTrue(user.is_active)

        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpass123"
        )

        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_user_str(self):
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        self.assertEqual(str(user), "testuser")

    def test_email_normalization(self):
        email = "test@EXAMPLE.COM"
        user = User.objects.create_user(
            username="test_user", email=email, password="testpass123"
        )

        self.assertEqual(user.email, "test@example.com")
