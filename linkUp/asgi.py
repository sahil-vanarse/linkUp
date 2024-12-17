"""
ASGI config for linkUp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linkUp.settings')

# application = ProtocolTypeRouter({
#     'http' : get_asgi_application()
# })

# linkUp/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import base.routing  # Ensure this is the correct import

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linkUp.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            base.routing.websocket_urlpatterns  # Ensure this is correct
        )
    ),
})


