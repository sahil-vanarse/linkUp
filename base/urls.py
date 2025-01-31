"""
URL Configuration for the linkUp Application

This module defines the URL patterns for the linkUp Django application. Each URL pattern is associated with a specific view function that handles the request and response for that URL.

Key URL Patterns:
- 'login/': Maps to the loginPage view for user authentication.
- 'logoutUser/': Maps to the logoutUser view for logging out the current user.
- 'register/': Maps to the registerPage view for user registration.

- '': Maps to the home view, displaying the main page with rooms and topics.
- 'room/<str:pk>/': Maps to the room view, displaying details of a specific room identified by its primary key (pk).
- 'profile/<str:pk>/': Maps to the userProfile view, showing the profile of a specific user identified by their primary key (pk).

- 'create-room': Maps to the createRoom view for authenticated users to create a new room.
- 'update-room/<str:pk>/': Maps to the updateRoom view for updating room details, identified by its primary key (pk).
- 'delete-room/<str:pk>/': Maps to the deleteRoom view for deleting a specific room, identified by its primary key (pk).
- 'delete-message/<str:pk>/': Maps to the deleteMessage view for deleting a specific message, identified by its primary key (pk).

- 'update-user/': Maps to the updateUser view for users to update their profile information.
- 'topics/': Maps to the topicsPage view, displaying a list of topics.
- 'activity/': Maps to the activityPage view, showing all room messages for activity tracking.

Usage:
- To add new URL patterns, include them in the urlpatterns list.
- Ensure to import any necessary views at the top of this file.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logoutUser/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-room', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    path('update-user/', views.updateUser, name="update-user"),
    path('delete-account/', views.deleteAccount, name='delete-account'),
    path('topics/', views.topicsPage, name="topics"),
    path('users/', views.UsersPage, name="users"),
    path('activity/', views.activityPage, name="activity"),
]
