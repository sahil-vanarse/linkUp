"""
Django settings for the linkUp project.

This file contains the configuration settings for the Django application, including
database settings, middleware, installed applications, and other important settings.

Key Sections:
- BASE_DIR: Defines the base directory for the project.
- SECRET_KEY: A secret key for the application, should be kept confidential in production.
- DEBUG: A boolean that turns on/off debug mode; should be False in production.
- ALLOWED_HOSTS: A list of strings representing the host/domain names that this Django site can serve.
- INSTALLED_APPS: A list of all Django applications that are activated in this project.
- MIDDLEWARE: A list of middleware components that process requests and responses.
- TEMPLATES: Configuration for template rendering.
- DATABASES: Database connection settings.
- AUTH_PASSWORD_VALIDATORS: Validators for user passwords.
- STATIC and MEDIA files configuration: Settings for serving static and media files.
- CORS configuration: Settings for Cross-Origin Resource Sharing.
"""

from pathlib import Path
import mimetypes
import dj_database_url


# Add MIME types for SVG files to ensure they are served correctly
mimetypes.add_type("image/svg+xml", ".svg", True)
mimetypes.add_type("image/svg+xml", ".svgz", True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-8xh327^ve7&+t*dj6&5sxop3)^g)$db_oo0nu$w)e0w2uj6&kw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Define the allowed hosts for the application
ALLOWED_HOSTS = ['*', 'https://toknex.onrender.com', 'toknex.onrender.com']

CSRF_TRUSTED_ORIGINS = ["https://your-app.onrender.com"]


# Application definition: List of installed applications
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'base.apps.BaseConfig',  # Custom application
    'rest_framework',  # Django REST framework
    "corsheaders",  # Middleware for handling CORS
    'channels',  # Django Channels for WebSocket support
    'whitenoise.runserver_nostatic',  # Whitenoise for serving static files
]

# Specify the custom user model
AUTH_USER_MODEL = 'base.User'

# Middleware configuration: List of middleware components
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Middleware for serving static files
    "corsheaders.middleware.CorsMiddleware",  # Middleware for handling CORS
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL configuration
ROOT_URLCONF = 'linkUp.urls'

# Template configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'  # Directory for template files
        ],
        'APP_DIRS': True,  # Enable loading templates from app directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI and ASGI application settings
WSGI_APPLICATION = 'linkUp.wsgi.application'
ASGI_APPLICATION = 'linkUp.asgi.application'

# Channel Layers configuration for Django Channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"  # In-memory channel layer for development
    }
}

# Database configuration
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',  # PostgreSQL database engine
#         'NAME': 'toknex',  # Database name
#         'USER': 'postgres',  # Database user
#         'PASSWORD': 'S#@5ahil1P',  # Database password
#         'HOST': 'localhost',  # Database host
#         'PORT': '5432',  # Database port
#     }
# }

# Database configuration
DATABASES = {
    'default': dj_database_url.parse('postgresql://toknex_user:9aM3rqYSn40M8hQaHxjEna5G81xY1bxB@dpg-cuj5jdbv2p9s73cic1eg-a.oregon-postgres.render.com/toknex')
}

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465  # SSL port
EMAIL_USE_SSL = True  # SSL must be True for port 465
EMAIL_HOST_USER = 'sahilvanarse4@gmail.com'
EMAIL_HOST_PASSWORD = 'pujz jwvv zglo vlhr'  # Ensure it's correct and no extra spaces
DEFAULT_FROM_EMAIL = 'sahilvanarse4@gmail.com'

# Password validation settings
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization settings
LANGUAGE_CODE = 'en-us'  # Default language
TIME_ZONE = 'UTC'  # Default time zone
USE_I18N = True  # Enable internationalization
USE_TZ = True  # Enable timezone support

# Static files configuration
STATIC_URL = '/static/'  # URL for static files
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Directory for collected static files

STATICFILES_DIRS = [
    BASE_DIR / 'static'  # Additional directories for static files
]

# Media files configuration
MEDIA_URL = '/media/'  # URL for media files
MEDIA_ROOT = BASE_DIR / 'media'  # Directory for uploaded media files

# Whitenoise configuration for serving static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS configuration for Cross-Origin Resource Sharing
CORS_ALLOW_ALL_ORIGINS = True  # Allow all origins
CORS_ALLOW_CREDENTIALS = True  # Allow credentials

# Specific allowed origins for CORS
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://localhost:3000',
]

# Jazzmin settings for the Django admin interface
JAZZMIN_SETTINGS = {
    "site_title": "TokneX Admin",  # Title displayed in the admin site
    "site_header": "TokneX",  # Header displayed at the top of the admin site
    "site_brand": "TokneX",  # Brand name displayed in the admin site
    "login_logo": "icons/admin_login_image.svg",  # Logo displayed on the login page
    "site_logo_classes": "img-circle",  # CSS classes for the site logo
    "site_icon": "logos/newLogo.svg",  # Favicon for the admin site
    "welcome_sign": "Welcome to the TokneX, your go-to platform for connecting and collaborating.",  # Welcome message for users
    "copyright": "Made from ❤️ by Sahil",  # Copyright notice
    # "user_avatar": "profile.photo",  # Path to user avatar image
    "topmenu_links": [  # Links displayed in the top menu
        {"name": "Dashboard", "url": "admin:index", "permissions": ["auth.view_user"]},  # Link to the dashboard with permissions
        {"name": "GitHub", "url": 'https://github.com/sahil-vanarse/linkUp', "new_window": True},  # Link to GitHub repository
        {"model": "auth.User"},  # Link to the User model
        {"app": "base"},  # Link to the base app
    ],
    "show_ui_builder": False,  # Enable UI builder for customization
}


SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
