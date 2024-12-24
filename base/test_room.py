from unittest import TestCase
from base.models import Room, Topic, User

class RoomModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="host@example.com", password="password")
        self.topic = Topic.objects.create(name="Programming")

    def test_room_creation(self):
        room = Room.objects.create(
            host=self.user,
            topic=self.topic,
            name="Python Basics",
            description="Discussion about Python basics."
        )
        self.assertEqual(room.name, "Python Basics")
        self.assertEqual(room.host, self.user)
        self.assertEqual(room.topic, self.topic)
        self.assertEqual(room.description, "Discussion about Python basics.")
