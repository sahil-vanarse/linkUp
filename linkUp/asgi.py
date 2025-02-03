import os
import django

# Set the default settings module for the Django project.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linkUp.settings')

# Initialize Django. This must be done before importing any models.
django.setup()

# Import the necessary modules for ASGI application and Channels routing.
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from base.routing import websocket_urlpatterns  # Import WebSocket URL patterns from the base app.

# Define the ASGI application routing.
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handle HTTP requests.
    "websocket": AuthMiddlewareStack(  # Handle WebSocket connections with authentication.
        URLRouter(
            websocket_urlpatterns  # Route WebSocket connections to the defined URL patterns.
        )
    ),
})