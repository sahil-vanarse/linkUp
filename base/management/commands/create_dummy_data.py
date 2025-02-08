from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from base.models import Room, Message, Topic
from faker import Faker
import random
from datetime import datetime, timedelta

User = get_user_model()
fake = Faker(['en_IN'])

class Command(BaseCommand):
    help = 'Creates dummy users with Indian names and generates automated messages'

    def add_arguments(self, parser):
        parser.add_argument('num_users', type=int, help='Number of dummy users to create')
        parser.add_argument('num_messages', type=int, help='Number of messages per user')

    def handle(self, *args, **kwargs):
        num_users = kwargs['num_users']
        num_messages = kwargs['num_messages']

        # Create dummy users with Indian names
        dummy_users = []
        indian_surnames = ['Tambe', 'Gadge', 'Dhande', 'Sawant', 'Khairnar',  
                           'Dabholkar', 'Lad', 'Palande', 'Ketkar', 'Ambekar']
        
        for i in range(num_users):
            first_name = fake.first_name()
            last_name = random.choice(indian_surnames)
            email = f"{first_name.lower()}.{last_name.lower()}{i}@example.com"

            user = User.objects.create_user(
                email=email,
                password="dummypass123",
                name=f"{first_name} {last_name}",
                username=f"{first_name.lower()}",
            )
            dummy_users.append(user)
            self.stdout.write(f"Created user: {user.name} ({email})")

        # New set of room names with assigned topics
        rooms_with_topics = {
            "Deep Learning Innovations": "AI",
            "Cybersecurity Best Practices": "Security",
            "Cloud-Native Architectures": "Cloud",
            "Data Science with Python": "ML",
            "Kubernetes for Scalable Applications": "DevOps",
            "SQL vs NoSQL Databases": "DBMS",
            "Advanced Git Strategies": "Git",
            "Smart Contracts with Solidity": "Blockchain",
            "Big Data Analytics": "DBMS",
            "CI/CD Best Practices": "DevOps"
        }

        # Ensure topics exist in the database
        topic_instances = {name: Topic.objects.get_or_create(name=name)[0] for name in set(rooms_with_topics.values())}

        # Create rooms
        rooms = []
        for room_name, topic_name in rooms_with_topics.items():
            host = random.choice(dummy_users)
            topic = topic_instances[topic_name]

            room = Room.objects.create(
                host=host,
                topic=topic,
                name=room_name,
                description=fake.sentence(),
            )

            # Add 1-5 random participants
            participants = random.sample(dummy_users, random.randint(1, 5))
            room.participants.add(*participants)
            rooms.append(room)
            self.stdout.write(f"Created room: {room.name} under topic {topic.name}")

        # Technical messages
        technical_messages = [
            "Deep learning models are getting better at NLP tasks. Any favorite frameworks?",
            "Security breaches are increasing! MFA and zero-trust policies are a must.",
            "Cloud-native apps with Kubernetes are the future! How are you managing workloads?",
            "Python dominates in data science. Pandas and NumPy make life easy!",
            "Microservices with Kubernetes helped us scale like never before!",
            "SQL is great for structured data, but NoSQL rocks for scalability. Thoughts?",
            "Advanced Git workflows like cherry-picking and interactive rebase can be lifesavers.",
            "Ethereum's transition to Proof-of-Stake is game-changing for smart contracts!",
            "Big Data tools like Apache Spark and Hadoop help process petabytes of data!",
            "CI/CD automation cuts deployment time in half. What's your favorite CI tool?"
        ]

        # Generate messages
        for user in dummy_users:
            for _ in range(num_messages):
                room = random.choice(rooms)
                created_time = datetime.now() - timedelta(
                    days=random.randint(0, 30),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
                message = Message.objects.create(
                    user=user,
                    room=room,
                    body=random.choice(technical_messages) if random.random() < 0.3 else fake.sentence(),
                    created=created_time,
                    updated=created_time
                )
                self.stdout.write(f"Created message by {user.name} in room {room.name}")

        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_users} users and {num_users * num_messages} messages'))
