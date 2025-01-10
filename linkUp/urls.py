"""
URL Configuration for the linkUp Project

This module defines the URL patterns for the linkUp Django application. It includes the admin interface, 
the main application URLs, and API endpoints. Additionally, it handles serving static and media files 
during development.

Key Components:
- Admin Interface: Accessible at '/admin/' for managing the application.
- Base Application URLs: Included from 'base.urls' for the main application routes.
- API Endpoints: Included from 'base.api.urls' for API-related routes.

Static and Media Files:
- When in DEBUG mode, the application serves static files and media files from the specified directories.

Usage:
- To add new URL patterns, include them in the urlpatterns list.
- Ensure to import any necessary views or modules at the top of this file.

"""

from django.contrib import admin  # type: ignore 
from django.urls import path, include  # type: ignore
from django.conf import settings  # type: ignore
from django.conf.urls.static import static  # type: ignore

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('api/', include('base.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
