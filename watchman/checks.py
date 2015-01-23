# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import traceback
import uuid
from django.conf import settings
from django.core.cache import get_cache
from django.core.mail import send_mail
from django.db import connections


def _check_caches(caches):
    return [_check_cache(cache) for cache in caches]


def _check_cache(cache_name):
    key = str(uuid.uuid4())
    value = str(uuid.uuid4())
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
        send_mail("subject", "message", "from@example.com", ["to@example.com"])
        response = {"ok": True}
    except Exception as e:
        response = {
            "ok": False,
            "error": str(e),
            "stacktrace": traceback.format_exc(),
        }
    return response


def caches_status():
    return {"caches": _check_caches(settings.CACHES)}


def databases_status():
    return {"databases": _check_databases(settings.DATABASES)}


def email_status():
    return {"email": _check_email()}
