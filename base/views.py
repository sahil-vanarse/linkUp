"""
This module contains views for handling user authentication, room management, and messaging in the linkUp application.

Key Functions:
- loginPage: Handles user login, including form submission and authentication.
- logoutUser: Logs out the current user and redirects to the home page.
- registerPage: Manages user registration, including form validation and user creation.
- home: Displays the home page with a list of rooms, topics, and recent messages based on search queries.
- room: Displays a specific room's details, including messages and participants.
- userProfile: Shows the profile of a specific user, including their rooms and messages.
- createRoom: Allows authenticated users to create a new room.
- updateRoom: Enables the host of a room to update its details.
- deleteRoom: Allows the host to delete a room.
- deleteMessage: Enables users to delete their own messages.
- updateUser: Allows users to update their profile information.
- topicsPage: Displays a list of topics based on search queries.
- activityPage: Shows all room messages for activity tracking.

Dependencies:
- Django's built-in authentication system for user management.
- Django Channels for real-time messaging capabilities.
- Custom models (Room, Topic, Message, User) and forms for handling data.

Usage:
- Each function corresponds to a specific URL pattern defined in the application's routing configuration.
- Ensure that the user is authenticated for actions that modify data (e.g., creating, updating, or deleting rooms/messages).

"""

from django.shortcuts import render, redirect # type: ignore
from django.db.models import Q # type: ignore
from django.http import HttpResponse # type: ignore
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Message, User # type: ignore
from .forms import RoomForm, UserForm, MyUserCreationForm # type: ignore
from django.contrib.auth import authenticate, login, logout # type: ignore
from django.contrib import messages # type: ignore
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.mail import send_mail  # Import send_mail for sending emails

def loginPage(request):
    """
    Handles user login. If the user is already authenticated, redirects to the home page.
    If the request method is POST, it attempts to authenticate the user with the provided email and password.
    Displays an error message if authentication fails.
    """
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "User does not Exist.")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    """Logs out the current user and redirects to the home page."""
    logout(request)
    return redirect('home')

def registerPage(request):
    """
    Manages user registration. If the request method is POST, it validates the registration form.
    If valid, creates a new user and logs them in, redirecting to the home page.
    Displays an error message if registration fails.
    """
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)

            # Send a welcome email to the user
            welcome_message = (
                f"Dear {user.username.upper()},\n\n"
                "We're thrilled to welcome you to the LinkUp family! 🎉\n\n"
                "Thank you for registering with us. At LinkUp, we believe in creating meaningful connections and empowering individuals to share knowledge, collaborate, and grow together. We are so glad to have you on board.\n\n"
                "We look forward to helping you explore new opportunities, meet like-minded individuals, and build lasting relationships in our vibrant community.\n\n"
                "If you have any questions or need assistance, feel free to reach out to us. We're here for you every step of the way!\n\n"
                "Welcome aboard, and let's make this journey unforgettable! 🚀\n\n"
                "Best regards,\n"
                "The LinkUp Team"
            )

            send_mail(
                'Welcome to LinkUp!',
                welcome_message,
                'sahilvanarse4@gmail.com',  # Replace with your from email
                [user.email],
                fail_silently=False,
            )

            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    """
    Displays the home page with a list of rooms, topics, recent messages, and all users.
    Filters rooms based on search queries provided in the request.
    """
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()[:10]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    )[:4]
    users = User.objects.all()  # Fetch all users

    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages': room_messages,
        'users': users  # Include users in the context
    }
    return render(request, 'base/home.html', context)

def room(request, pk):
    """
    Displays a specific room's details, including messages and participants.
    """
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants
    }
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    """
    Shows the profile of a specific user, including their rooms and messages.
    """
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    # topics = Topic.objects.all()
    users = User.objects.all()
    context = {
        'user': user,
        'rooms': rooms,
        'room_messages': room_messages,
        # 'topics': topics
        'users' : users
    }
    return render(request, 'base/profile.html', context)

@login_required(login_url="login")
def createRoom(request):
    """
    Allows authenticated users to create a new room.
    If the request method is POST, it retrieves the topic and creates a new room.
    Redirects to the home page after creation.
    """
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
        )
        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url="login")
def updateRoom(request, pk):
    """
    Enables the host of a room to update its details.
    If the user is not the host, returns an error message.
    If the request method is POST, updates the room's details and saves it.
    """
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed here !!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url="login")
def deleteRoom(request, pk):
    """
    Allows the host to delete a room.
    If the user is not the host, returns an error message.
    If the request method is POST, deletes the room and redirects to the home page.
    """
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not Allowed!!!')
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url="login")
def deleteMessage(request, pk):
    """
    Enables users to delete their own messages.
    If the user is not the message owner, returns an error message.
    If the request method is POST, deletes the message and redirects to the home page.
    """
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not Allowed!!!')
    if request.method == "POST":
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})

@login_required(login_url='login')
def updateUser(request):
    """
    Allows users to update their profile information.
    If the request method is POST, validates the form and saves the changes.
    Redirects to the user's profile page after updating.
    """
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'base/update-user.html', {'form': form})

def topicsPage(request):
    """
    Displays a list of topics based on search queries.
    """
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})

def UsersPage(request):
    """
    Displays a list of topics based on search queries.
    """
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    users = User.objects.filter(name__icontains=q)
    return render(request, 'base/users.html', {'users': users})

def activityPage(request):
    """
    Shows all room messages for activity tracking.
    """
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})
