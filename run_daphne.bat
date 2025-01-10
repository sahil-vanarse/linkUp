@echo off
set DJANGO_SETTINGS_MODULE=linkUp.settings
daphne linkUp.asgi:application
