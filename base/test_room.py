from unittest import TestCase
from base.models import Room, Topic, User

class RoomModelTest(TestCase):
    """
    Unit test case for the Room model.

    This test case verifies the functionality of the Room model, specifically
    the creation of a room instance. It ensures that the room is correctly
    associated with its host user, topic, name, and description.

    Methods:
        setUp: Initializes a user and a topic for testing.
        test_room_creation: Tests the creation of a Room instance and
        verifies its attributes.
    """

    def setUp(self):
        """
        Set up the test environment by creating a user and a topic.

        This method is called before each test. It creates a user with a
        specified email and password, and a topic with a given name.
        """
        self.user = User.objects.create_user(email="host@example.com", password="password")
        self.topic = Topic.objects.create(name="Programming")

    def test_room_creation(self):
        """
        Test the creation of a Room instance.

        This method creates a Room instance with predefined attributes and
        asserts that the attributes of the created room match the expected
        values.
        """
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
