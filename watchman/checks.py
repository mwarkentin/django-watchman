# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import uuid
from django.conf import settings
from django.core.cache import get_cache
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
from django.db import connections

from watchman.decorators import check


def _check_caches(caches):
    return [_check_cache(cache) for cache in sorted(caches)]


@check
def _check_cache(cache_name):
    key = 'django-watchman-{}'.format(uuid.uuid4())
    value = 'django-watchman-{}'.format(uuid.uuid4())

    cache = get_cache(cache_name)
    cache.set(key, value)
    cache.get(key)
    cache.delete(key)
    return {cache_name: {"ok": True}}


def _check_databases(databases):
    return [_check_database(database) for database in sorted(databases)]


@check
def _check_database(database):
    connections[database].introspection.table_names()
    return {database: {"ok": True}}


@check
def _check_email():
    headers = {"X-DJANGO-WATCHMAN": True}
    email = EmailMessage(
        "django-watchman email check",
        "This is an automated test of the email system.",
        "watchman@example.com",
        ["to@example.com"],
        headers=headers
    )
    email.send()
    return {"ok": True}


@check
def _check_storage():
    filename = 'django-watchman-{}.txt'.format(uuid.uuid4())
    content = 'django-watchman test file'
    path = default_storage.save(filename, ContentFile(content))
    default_storage.size(path)
    default_storage.open(path).read()
    default_storage.delete(path)
    return {"ok": True}


def caches():
    return {"caches": _check_caches(settings.CACHES)}


def databases():
    return {"databases": _check_databases(settings.DATABASES)}


def email():
    return {"email": _check_email()}


def storage():
    return {"storage": _check_storage()}
