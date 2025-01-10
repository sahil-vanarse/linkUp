"""
UserTest is a unit test case class that verifies the functionality of user creation using the UserFactory.

This class inherits from Django's TestCase, providing a framework for testing user-related functionalities.

Methods:
- setUpTestData: This class method is called once for the entire test case. It sets up the test data by creating a user instance with a predefined email using the UserFactory. This user instance is accessible to all test methods in the class.

- test_user_creation: This method tests the creation of a user. It asserts that the email of the created user matches the expected email address ("testuser@example.com").

- test_another_user_creation: This method tests the creation of another user using the UserFactory. It ensures that the newly created user's email is unique by asserting that it does not equal the email of the previously created user.

Usage:
To run these tests, use the Django test runner with the command:
    python manage.py test base.tests

This will execute all test methods in this module, providing feedback on the success or failure of each test.
"""

from django.test import TestCase # type: ignore
from base.factories import UserFactory

class UserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(email="testuser@example.com")

    def test_user_creation(self):
        self.assertEqual(self.user.email, "testuser@example.com")

    def test_another_user_creation(self):
        new_user = UserFactory()  # This will create a user with a unique username and email
        self.assertNotEqual(new_user.email, self.user.email)  # Ensure emails are unique
