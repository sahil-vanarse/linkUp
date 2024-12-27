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
