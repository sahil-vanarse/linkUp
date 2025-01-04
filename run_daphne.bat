@echo off
set DJANGO_SETTINGS_MODULE=linkUp.settings
python -c "from django.core.wsgi import get_wsgi_application; get_wsgi_application()"  # Initialize Django before running Daphne
daphne -b 0.0.0.0 -p 8000 linkUp.asgi:application
