from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from base.models import Room, Message, Topic
from faker import Faker
import random
from datetime import datetime, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile

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

        # Tech-focused topics
        topics = ["AI",
    "ML",
    "API",
    "DBMS",
    "Cloud",
    "Docker",
    "K8s",
    "Git",
    "Crypto"
    "Blockchain"]
        
        for topic_name in topics:
            Topic.objects.get_or_create(name=topic_name)

        # Create dummy users with Indian names
        dummy_users = []
        indian_surnames = ['Jadhav', 'Payelkar', 'Malavde', 'Kale', 'Landge', 'Shirshivkar', 'Korgaonkar', 'Das']
        
        for i in range(num_users):
            first_name = fake.first_name()
            last_name = random.choice(indian_surnames)
            email = f"{first_name.lower()}.{last_name.lower()}{i}@example.com"
            
            # Create user with all required fields from your User model
            user = User.objects.create_user(
                email=email,
                password="dummypass123",
                name=f"{first_name} {last_name}",
                username=f"{first_name.lower()}_{last_name.lower()}",
                # bio=fake.text(max_nb_chars=200),
                # avatar will use the default value from your model
            )
            dummy_users.append(user)
            self.stdout.write(f"Created user: {user.name} ({email})")

        # Technical room names
        room_names = [
            "MongoDB & NoSQL Databases",
    "CI/CD Pipelines with Jenkins",
    "Version Control with Git",
    "Serverless Computing with AWS Lambda",
    "Network Security Practices",
    "Artificial Intelligence Solutions",
    "Machine Learning Frameworks",
    "Blockchain Development",
    "Data Warehousing Concepts",
    "DevOps Automation Tools"
        ]

        room_descriptions = [
    "Discuss non-relational databases, MongoDB queries, and scaling strategies.",
    "Learn to build, test, and deploy applications using Jenkins pipelines.",
    "Master Git commands, branching strategies, and version control workflows.",
    "Explore serverless architectures and AWS Lambda use cases.",
    "Share best practices for securing networks and preventing intrusions.",
    "Explore AI frameworks and practical implementations for real-world problems.",
    "Learn TensorFlow, PyTorch, and other frameworks for predictive modeling.",
    "Discuss smart contracts, dApps, and blockchain protocols.",
    "Share insights on building and optimizing data warehouses for analytics.",
    "Explore tools for automating infrastructure and streamlining DevOps workflows."
]


        # Create rooms
        rooms = []
        for i in range(min(len(room_names), num_users // 2)):
            topic = Topic.objects.order_by('?').first()
            host = random.choice(dummy_users)
            room = Room.objects.create(
                host=host,
                topic=topic,
                name=room_names[i],
                description=room_descriptions[i],
            )
            # Add 1-5 random participants
            participants = random.sample(dummy_users, random.randint(1, 5))
            room.participants.add(*participants)
            rooms.append(room)
            self.stdout.write(f"Created room: {room.name}")



        technical_messages = [
    "I've been optimizing MongoDB queries lately. Indexing really improved performance! What are your thoughts?",
    "We automated our CI/CD pipeline using Jenkins last month. Deployments are so much smoother now!",
    "Handling merge conflicts in Git used to be a nightmare, but rebasing helped a lot. How do you guys manage it?",
    "Migrated a few workloads to AWS Lambda recently. Serverless is amazing but debugging can be tricky!",
    "Just updated our network security policies. Firewalls and 2FA made a big difference in preventing breaches.",
    "AI models are getting so powerful! I just built a small chatbot with transformers, and it works surprisingly well!",
    "TensorFlow vs PyTorch is always a debate. Personally, I find PyTorch easier to debug. What do you all prefer?",
    "Just deployed my first smart contract on Ethereum. Gas fees are high, but the experience was awesome!",
    "Optimizing data warehouse queries saved us hours of processing time. Partitioning made a huge difference!",
    "Infrastructure as code is a lifesaver. Terraform made scaling so much easier for our cloud setup!"
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