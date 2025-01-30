from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from base.models import Topic, User
from base.api.serializers import TopicSerializer, UserSerializer

class APIViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            username='testuser'
        )
        self.topic = Topic.objects.create(name='Test Topic')

    def test_get_topics(self):
        url = reverse('get-topics')
        response = self.client.get(url)
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_topic(self):
        url = reverse('get-topic', kwargs={'pk': self.topic.pk})
        response = self.client.get(url)
        serializer = TopicSerializer(self.topic)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_topic_404(self):
        url = reverse('get-topic', kwargs={'pk': 999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_users(self):
        url = reverse('get-users')
        response = self.client.get(url)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_user(self):
        url = reverse('get-user', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        serializer = UserSerializer(self.user)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)