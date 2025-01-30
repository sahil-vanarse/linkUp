from django.test import TestCase, Client
from django.urls import reverse
from base.models import Room, Topic, User, Message

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
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

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/home.html')

    def test_room_view(self):
        response = self.client.get(reverse('room', kwargs={'pk': self.room.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/room.html')

    def test_create_room(self):
        self.client.login(email='testuser@example.com', password='testpass123')
        response = self.client.post(reverse('create-room'), {
            'topic': self.topic.id,
            'name': 'New Room',
            'description': 'New Description'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Room.objects.filter(name='New Room').exists())

    def test_update_room(self):
        self.client.login(email='testuser@example.com', password='testpass123')
        response = self.client.post(
            reverse('update-room', kwargs={'pk': self.room.pk}),
            {
                'topic': self.topic.id,
                'name': 'Updated Room',
                'description': 'Updated Description'
            }
        )
        self.room.refresh_from_db()
        self.assertEqual(self.room.name, 'Updated Room')

    def test_delete_room(self):
        self.client.login(email='testuser@example.com', password='testpass123')
        response = self.client.post(reverse('delete-room', kwargs={'pk': self.room.pk}))
        self.assertFalse(Room.objects.filter(pk=self.room.pk).exists())