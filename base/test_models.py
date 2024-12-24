from django.test import TestCase # type: ignore
from unittest import TestCase

from base.models import User

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email="testuser@example.com",
            password="testpassword123",
            name="Test User"
        )
        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.check_password("testpassword123"))
        self.assertEqual(user.name, "Test User")

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpassword123"
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
