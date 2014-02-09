# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import traceback
import uuid

from django.conf import settings
from django.core.cache import get_cache
from django.db import connections

from jsonview.decorators import json_view


@json_view
def status(request):
    response = {
        "databases": check_databases(settings.DATABASES),
        "caches": check_caches(settings.CACHES),
    }
    return response


def check_databases(databases):
    return [check_database(database) for database in databases]


def check_database(database):
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


def check_caches(caches):
    return [check_cache(cache) for cache in caches]


def check_cache(cache_name):
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
