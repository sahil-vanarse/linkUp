"""
This module registers the models for the Django admin interface, allowing for easy management of the application's data.

Admin Models:
1. UserAdmin:
   - Customizes the admin interface for the User model.
   - Displays the following fields in the list view:
     - email: The user's email address.
     - username: The user's unique username.
     - name: The user's name.
   - Enables searching by email, username, and name.
   - Orders the list by email.

2. RoomAdmin:
   - Customizes the admin interface for the Room model.
   - Displays the following fields in the list view:
     - name: The name of the room.
     - host: The user who created the room.
     - topic: The topic associated with the room.
     - created: The timestamp when the room was created.
   - Allows filtering by host and topic.
   - Enables searching by room name and description.
   - Orders the list by updated and created timestamps in descending order.

3. TopicAdmin:
   - Customizes the admin interface for the Topic model.
   - Displays the following field in the list view:
     - name: The name of the topic.
   - Enables searching by topic name.
   - Orders the list by name.

4. MessageAdmin:
   - Customizes the admin interface for the Message model.
   - Displays the following fields in the list view:
     - user: The user who sent the message.
     - room: The room where the message was sent.
     - created: The timestamp when the message was created.
   - Allows filtering by user and room.
   - Enables searching by message body.
   - Orders the list by created timestamp in descending order.

Usage:
- To register a model with the admin interface, use the `admin.site.register()` method with the model and its corresponding admin class.

Super User Email, Password:
Email - sahilvanarse4@gmail.com
Password - S#@5ahil1P
"""

from django.contrib import admin # type: ignore 
from django.contrib.postgres import search # type: ignore
from .models import Room, Topic, Message, User # type: ignore

class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'name']
    search_fields = ['email', 'username', 'name']
    ordering = ['email']

class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'host', 'topic', 'created']
    list_filter = ['host', 'topic']
    search_fields = ['name', 'description']
    ordering = ['-updated', '-created']

class TopicAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']

class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'created']
    list_filter = ['user', 'room']
    search_fields = ['body']
    ordering = ['-created']

admin.site.register(User, UserAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Message, MessageAdmin)
