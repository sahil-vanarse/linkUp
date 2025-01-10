"""
This module contains forms for user and room management using Django's ModelForm and UserCreationForm.

Forms:
1. MyUserCreationForm:
   - Inherits from UserCreationForm to handle user registration.
   - Fields:
     - name: The user's name.
     - username: A unique identifier for the user.
     - email: The user's email address, which must be unique and indexed in the User model.
     - password1: The user's chosen password.
     - password2: A confirmation of the user's chosen password.

2. RoomForm:
   - Inherits from ModelForm to manage Room instances.
   - Fields:
     - All fields from the Room model are included except:
       - host: The user who created the room (set automatically).
       - participants: Users participating in the room (set automatically).
       - search_vector: Used for full-text search capabilities, managed by PostgreSQL.

3. UserForm:
   - Inherits from ModelForm to manage User instances.
   - Fields:
     - avatar: The user's profile picture.
     - name: The user's name.
     - username: A unique identifier for the user.
     - email: The user's email address, which must be unique and indexed in the User model.
     - bio: A short biography of the user.

Usage:
- These forms can be used in views to handle user registration and room creation.
- Ensure that the fields align with the User and Room models defined in the application.
"""

from django.forms import ModelForm # type: ignore
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm # type: ignore

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants', 'search_vector']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']