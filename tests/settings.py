"""
Test settings for django-watchman tests.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True
USE_TZ = True

SECRET_KEY = "test-secret-key-for-django-watchman"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    },
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ROOT_URLCONF = "watchman.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "watchman",
]

SITE_ID = 1

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Media files for storage checks
MEDIA_ROOT = os.path.join(BASE_DIR, ".test_media")
MEDIA_URL = "/media/"

# Email backend for testing
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
