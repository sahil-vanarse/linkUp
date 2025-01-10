"""
This module contains unit tests for the Message model in the linkUp application.

Key Components:
- Test Case: MessageModelTest
    - Inherits from unittest.TestCase to provide a framework for testing the Message model.

Methods:
1. setUp:
    - Prepares the test environment by creating a user, a topic, and a room.
    - This method is called before each test method to ensure a fresh environment.

2. test_message_creation:
    - Tests the creation of a Message instance.
    - Asserts that the message is correctly associated with the user and room, and that the message body is as expected.

Usage:
- To run these tests, use the Django test runner with the command:
  python manage.py test base.test_messages

This will execute all test methods in this module, providing feedback on the success or failure of each test.
"""
from unittest import TestCase
from base.models import Message, Room, Topic, User

class MessageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@example.com", password="password")
        self.topic = Topic.objects.create(name="Python")
        self.room = Room.objects.create(
            host=self.user,
            topic=self.topic,
            name="Advanced Python"
        )

    def test_message_creation(self):
        message = Message.objects.create(
            user=self.user,
            room=self.room,
            body="Hello, this is a test message."
        )
        self.assertEqual(message.user, self.user)
        self.assertEqual(message.room, self.room)
        self.assertEqual(message.body, "Hello, this is a test message.")
