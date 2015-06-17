# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import Http404

from jsonview.decorators import json_view
from watchman.decorators import token_required, login_required
from watchman.utils import get_checks


@token_required
@login_required
@json_view
def status(request):
    response = {}

    check_list = None
    skip_list = None

    if len(request.GET) > 0:
        if 'check' in request.GET:
            check_list = request.GET.getlist('check')
        if 'skip' in request.GET:
            skip_list = request.GET.getlist('skip')

    for check in get_checks(check_list=check_list, skip_list=skip_list):
        if callable(check):
            response.update(check())

    if len(response) == 0:
        raise Http404('No checks found')

    return response
