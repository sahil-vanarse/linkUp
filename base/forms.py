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
     - old_password: The user's current password for verification.
     - new_password1: The user's new password.
     - new_password2: Confirmation of the new password.

Usage:
- These forms can be used in views to handle user registration and room creation.
- Ensure that the fields align with the User and Room models defined in the application.
"""

from django import forms
from django.forms import ModelForm # type: ignore
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm # type: ignore
from django.contrib.auth import password_validation

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
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Current Password'}),
        required=False
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}),
        required=False,
        help_text=password_validation.password_validators_help_text_html()
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'}),
        required=False
    )

    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio', 'old_password', 'new_password1', 'new_password2']

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if (new_password1 or new_password2) and not old_password:
            raise forms.ValidationError("Please enter your current password to change your password")

        if old_password and not (new_password1 and new_password2):
            raise forms.ValidationError("Please enter both new password fields")

        if new_password1 != new_password2:
            raise forms.ValidationError("New passwords don't match")

        if old_password and not self.instance.check_password(old_password):
            raise forms.ValidationError("Current password is incorrect")

        return cleaned_data