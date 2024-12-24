from unittest import TestCase
from base.models import Topic

class TopicModelTest(TestCase):
    def test_topic_creation(self):
        topic = Topic.objects.create(name="Django")
        self.assertEqual(topic.name, "Django")
