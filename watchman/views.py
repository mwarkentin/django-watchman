# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings

from jsonview.decorators import json_view

from watchman.checks import check_caches, check_databases


@json_view
def status(request):
    response = {
        "caches": check_caches(settings.CACHES),
        "databases": check_databases(settings.DATABASES),
    }
    return response
