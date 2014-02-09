# -*- coding: utf-8 -*-

import traceback

from django.conf import settings
from django.db import connections
from django.db.utils import DatabaseError

from jsonview.decorators import json_view


@json_view
def status(request):
    response = {
        "databases": check_databases(),
    }
    return response

def check_databases():
    return [check_database(database) for database in settings.DATABASES]

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
