import factory # type: ignore
from base.models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "password123")
    username = factory.Sequence(lambda n: f"username{n}")  # Ensure unique username
    name = factory.Faker("name")
