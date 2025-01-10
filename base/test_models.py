"""
UserModelTest is a test case class that contains unit tests for the User model in the base application.

This class inherits from Django's TestCase, which provides a framework for testing Django applications.

Methods:
- test_create_user: This method tests the creation of a regular user. It verifies that the user is created with the correct email, password, and name. 
  It checks if the email matches the expected value, if the password is correctly hashed and can be checked, and if the name is set correctly.

- test_create_superuser: This method tests the creation of a superuser. It verifies that the superuser is created with the correct permissions.
  It checks if the superuser has the 'is_staff' and 'is_superuser' attributes set to True, indicating that the user has administrative privileges.

Usage:
To run these tests, use the Django test runner. Ensure that the User model is properly defined in the base.models module before running the tests.
"""
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
