"""
TopicModelTest is a unit test case class that verifies the functionality of the Topic model in the base application.

This class inherits from Django's TestCase, providing a framework for testing the Topic model's behavior.

Methods:
- test_topic_creation: This method tests the creation of a Topic instance. It verifies that a Topic can be created with a specified name and that the name is correctly set.

Usage:
To run this test, use the Django test runner with the command:
    python manage.py test base.test_topics

This will execute all test methods in this module, providing feedback on the success or failure of each test.
"""

from unittest import TestCase
from base.models import Topic

class TopicModelTest(TestCase):
    def test_topic_creation(self):
        topic = Topic.objects.create(name="Django")
        self.assertEqual(topic.name, "Django")
