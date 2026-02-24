"""Django settings for djust-admin tests."""

import os

# Allow async unsafe operations for testing
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

SECRET_KEY = 'test-secret-key-not-for-production'

DEBUG = True

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'channels',
    'djust',
    'djust_admin',
    'tests.apps.TestsConfig',
]

# Static files (needed for djust client JavaScript)
STATIC_URL = '/static/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(__file__), 'test_db.sqlite3'),
    }
}

ROOT_URLCONF = 'tests.urls'

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
            ],
        },
    },
]

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

USE_TZ = True

# Password hashers (faster for tests)
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Middleware needed for auth
MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]

# Session settings
SESSION_ENGINE = "django.contrib.sessions.backends.db"

# Default auto field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
