# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.http import Http404

from jsonview.decorators import json_view
from watchman.utils import get_checkers
from watchman.settings import WATCHMAN_CHECKS
from watchman.decorators import token_required


@token_required
@json_view
def status(request):
    response = {}
    available_checkers = frozenset(WATCHMAN_CHECKS)
    # allow for asking for only a subset back.
    if len(request.GET) > 0 and 'only_check' in request.GET:
        possible_filters = frozenset(request.GET.getlist('only_check'))
        available_checkers &= possible_filters
    for func in get_checkers(paths_to_checkers=available_checkers):
        if callable(func):
            response.update(func(request))
    if len(response) == 0:
        raise Http404('No checks found')
    return response
