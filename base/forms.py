from django.forms import ModelForm # type: ignore
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm # type: ignore

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']
        # These fields match the User model which works with PostgreSQL
        # email is unique and indexed in the User model
        # username has an index in the User model

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants', 'search_vector']
        # Excluding search_vector since it's handled by PostgreSQL

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']
        # These fields match the User model columns in PostgreSQL
        # email and username are indexed