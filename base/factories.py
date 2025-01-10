import factory # type: ignore
from base.models import User

class UserFactory(factory.django.DjangoModelFactory):
    """
    UserFactory is a factory for creating User instances for testing purposes.

    This factory uses the `factory_boy` library to generate User objects with
    predefined attributes. It ensures that each generated User has unique
    email and username values.

    Attributes:
        email (str): A unique email address for the User, generated in the
                     format user{n}@example.com, where n is a sequence number.
        password (str): A default password for the User, set to "password123"
                        using the `set_password` method to ensure it is hashed.
        username (str): A unique username for the User, generated in the
                        format username{n}, where n is a sequence number.
        name (str): A randomly generated name for the User, created using
                    the Faker library.

    Usage:
        To create a User instance, simply call UserFactory.create() or
        UserFactory.build() as needed in your tests.
    """
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "password123")
    username = factory.Sequence(lambda n: f"username{n}")  # Ensure unique username
    name = factory.Faker("name")
