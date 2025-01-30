from django.test import TestCase
from base.models import Room, Topic, User, Message

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            username='testuser'
        )
        self.topic = Topic.objects.create(name='Test Topic')
        self.room = Room.objects.create(
            host=self.user,
            topic=self.topic,
            name='Test Room',
            description='Test Description'
        )

    def test_room_str_method(self):
        self.assertEqual(str(self.room), 'Test Room')

    def test_topic_str_method(self):
        self.assertEqual(str(self.topic), 'Test Topic')

    def test_message_str_method(self):
        message = Message.objects.create(
            user=self.user,
            room=self.room,
            body='Test Message Body That Is Longer Than Fifty Characters To Test Truncation'
        )
        self.assertEqual(str(message), 'Test Message Body That Is Longer Than Fifty Characters')

    def test_room_participants(self):
        self.room.participants.add(self.user)
        self.assertIn(self.user, self.room.participants.all())