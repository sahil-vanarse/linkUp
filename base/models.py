"""
This module defines the data models for the application using Django's ORM.

Models:
1. User: Extends Django's AbstractUser to create a custom user model with additional fields.
   - Fields:
     - name: CharField for the user's name.
     - email: EmailField that is unique and indexed.
     - username: CharField that is optional, unique, and can be blank.
     - bio: TextField for user biography.
     - avatar: ImageField with a default avatar.
     - search_vector: SearchVectorField for full-text search capabilities.
   - Manager: UserManager for creating users and superusers.

2. Topic: Represents a discussion topic.
   - Fields:
     - name: CharField for the topic name, indexed for faster lookups.

3. Room: Represents a chat room.
   - Fields:
     - host: ForeignKey to the User model, can be null.
     - topic: ForeignKey to the Topic model, can be null.
     - name: CharField for the room name, indexed.
     - description: TextField for room description, optional.
     - participants: ManyToManyField to the User model for room participants.
     - updated: DateTimeField that auto-updates on save, indexed.
     - created: DateTimeField that auto-sets on creation, indexed.
     - search_vector: SearchVectorField for full-text search capabilities.
   - Meta:
     - Ordering: Rooms are ordered by updated and created timestamps.
     - Indexes: Indexed by name, updated, and created fields.

4. Message: Represents a message in a room.
   - Fields:
     - user: ForeignKey to the User model.
     - room: ForeignKey to the Room model.
     - body: TextField for the message content.
     - updated: DateTimeField that auto-updates on save, indexed.
     - created: DateTimeField that auto-sets on creation, indexed.
   - Meta:
     - Ordering: Messages are ordered by updated and created timestamps.
     - Indexes: Indexed by updated and created fields.

Usage:
- Use the UserManager to create users and superusers.
- The User model can be used for authentication and user-related operations.
- Topics can be created to categorize rooms.
- Rooms can have multiple participants and messages.
"""

from django.db import models # type: ignore
from django.contrib.auth.models import AbstractUser, BaseUserManager # type: ignore
from django.contrib.postgres.fields import ArrayField # type: ignore
from django.contrib.postgres.search import SearchVectorField # type: ignore # type: ignore  

from cloudinary_storage.storage import RawMediaCloudinaryStorage  # made the changes here 
from .custom_storage import CustomCloudinaryStorage

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True, db_index=True)
    username = models.CharField(max_length=200, null=True, blank=True, unique=True)  # Make username optional and unique
    bio = models.TextField(null=True, default="Hey there! I'm using this app.")
    avatar = models.ImageField(null=True, blank=True, default="avatar.svg", storage=CustomCloudinaryStorage(), upload_to='avatars/')  # here changed
    search_vector = SearchVectorField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # No additional fields required for superuser creation

    objects = UserManager()

    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['username'])
        ]

    def __str__(self):
        return self.email
    
    def get_avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return '/media/avatar.svg'  # Replace with your default avatar path



class Topic(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    search_vector = SearchVectorField(null=True)

    class Meta:
        ordering = ['-updated', '-created']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['updated']),
            models.Index(fields=['created'])
        ]

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-updated', '-created']
        indexes = [
            models.Index(fields=['updated']),
            models.Index(fields=['created'])
        ]

    def __str__(self):
        return self.body[:50]
