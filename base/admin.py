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
