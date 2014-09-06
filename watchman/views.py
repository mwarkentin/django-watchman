# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import Http404

from jsonview.decorators import json_view
from watchman.utils import get_checks
from watchman.settings import WATCHMAN_CHECKS
from watchman.decorators import token_required


@token_required
@json_view
def status(request):
    response = {}
    available_checks = frozenset(WATCHMAN_CHECKS)
    if len(request.GET) > 0:
        if 'check' in request.GET:
            possible_filters = frozenset(request.GET.getlist('check'))
            available_checks &= possible_filters
        if 'skip' in request.GET:
            skipped_filters = frozenset(request.GET.getlist('skip'))
            available_checks -= skipped_filters
    for func in get_checks(paths_to_checks=available_checks):
        if callable(func):
            response.update(func(request))
    if len(response) == 0:
        raise Http404('No checks found')
    return response
