# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import Http404
from django.shortcuts import render

from jsonview.decorators import json_view
from watchman.decorators import token_required
from watchman.utils import get_checks


@token_required
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


@token_required
def dashboard(request):
    check_types = []
    checks = {}

    for check in get_checks(None, None):
        if callable(check):
            _check = check()

            for _type in _check:
                # _check[_type] is a list of dictionaries:
                # Example: [{'default': {'ok': True}}]
                statuses = []

                for a in _check[_type]:
                    status = {}

                    # Systems like storage don't have names
                    if a == 'ok':
                        status['name'] = ''
                        status['status'] = 'OK'
                        status['error'] = ''
                        status['stacktrace'] = ''
                    else:
                        for name in a:
                            status['name'] = name
                            status['status'] = 'OK' if a[name]['ok'] else 'ERROR'
                            status['error'] = a[name]['error'] if not a[name]['ok'] else ''
                            status['stacktrace'] = a[name]['stacktrace'] if not a[name]['ok'] else ''

                    statuses.append(status)

                type_overall_status = 'OK' if all([status['status'] == 'OK' for status in statuses]) else 'ERROR'

                check_types.append({
                    'type': _type,
                    'overall_status': type_overall_status,
                    'statuses': statuses})

    overall_status = 'OK' if all([type_status['overall_status'] == 'OK' for type_status in check_types]) else 'ERROR'

    return render(request, 'watchman/dashboard.html', {'checks': check_types, 'overall_status': overall_status})
