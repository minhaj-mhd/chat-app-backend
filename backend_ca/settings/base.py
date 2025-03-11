from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret Key
SECRET_KEY = os.getenv("SECRET_KEY")

# Application definition
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'accounts',
    'chat',
    'friends',
    'schema_graph',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTH_USER_MODEL = "accounts.User"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'accounts.tokenauthentication.JWTauthentication',
    ],
}

ASGI_APPLICATION = 'backend_ca.asgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
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




ROOT_URLCONF = 'backend_ca.urls'
# WSGI_APPLICATION = 'myproject.wsgi.application'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Static Files
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# settings.py

# Email Backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Email SMTP settings for Gmail (or any other service)
EMAIL_HOST = 'smtp-relay.brevo.com'  # Gmail SMTP server
EMAIL_PORT = 587  # Port for TLS
EMAIL_USE_TLS = True  # Use TLS encryption
EMAIL_HOST_USER = '8452bd001@smtp-brevo.com'  # Your Gmail address
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Your Gmail password (or app-specific password)
DEFAULT_FROM_EMAIL = '8452bd001@smtp-brevo.com'  # Default "From" email address

# Optional: Set the email for error reports
ADMINS = [('Admin', 'minhajmuhamad@gmail.com')]  # List of admin emails to receive error reports
