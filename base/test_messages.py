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
