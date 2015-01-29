# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import traceback
import uuid
from django.conf import settings
from django.core.cache import get_cache
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
from django.db import connections


def _check_caches(caches):
    return [_check_cache(cache) for cache in caches]


def _check_cache(cache_name):
    key = 'django-watchman-{}'.format(uuid.uuid4())
    value = 'django-watchman-{}'.format(uuid.uuid4())
    try:
        cache = get_cache(cache_name)
        cache.set(key, value)
        cache.get(key)
        cache.delete(key)
        response = {cache_name: {"ok": True}}
    except Exception as e:
        response = {
            cache_name: {
                "ok": False,
                "error": str(e),
                "stacktrace": traceback.format_exc(),
            },
        }
    return response


def _check_databases(databases):
    return [_check_database(database) for database in databases]


def _check_database(database):
    try:
        connections[database].introspection.table_names()
        response = {database: {"ok": True}}
    except Exception as e:
        response = {
            database: {
                "ok": False,
                "error": str(e),
                "stacktrace": traceback.format_exc(),
            },
        }
    return response


def _check_email():
    try:
        headers = {"X-DJANGO-WATCHMAN": True}
        email = EmailMessage(
            "django-watchman email check",
            "This is an automated test of the email system.",
            "watchman@example.com",
            ["to@example.com"],
            headers=headers
        )
        email.send()
        response = {"ok": True}
    except Exception as e:
        response = {
            "ok": False,
            "error": str(e),
            "stacktrace": traceback.format_exc(),
        }
    return response


def _check_storage():
    try:
        filename = 'django-watchman-{}.txt'.format(uuid.uuid4())
        content = 'django-watchman test file'
        path = default_storage.save(filename, ContentFile(content))
        default_storage.size(path)
        default_storage.open(path).read()
        default_storage.delete(path)
        response = {"ok": True}
    except Exception as e:
        response = {
            "ok": False,
            "error": str(e),
            "stacktrace": traceback.format_exc(),
        }
    return response


def caches():
    return {"caches": _check_caches(settings.CACHES)}


def databases():
    return {"databases": _check_databases(settings.DATABASES)}


def email():
    return {"email": _check_email()}


def storage():
    return {"storage": _check_storage()}
