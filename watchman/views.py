# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import Http404
from django.shortcuts import render
from django.utils.translation import ugettext as _
from jsonview.decorators import json_view
from watchman import settings
from watchman import __version__
from watchman.decorators import auth
from watchman.utils import get_checks


WATCHMAN_VERSION_HEADER = 'X-Watchman-Version'


def _get_check_params(request):
    check_list = None
    skip_list = None

    if len(request.GET) > 0:
        if 'check' in request.GET:
            check_list = request.GET.getlist('check')
        if 'skip' in request.GET:
            skip_list = request.GET.getlist('skip')

    return (check_list, skip_list)


@auth
@json_view
def status(request):
    response = {}
    http_code = 200

    check_list, skip_list = _get_check_params(request)

    for check in get_checks(check_list=check_list, skip_list=skip_list):
        if callable(check):
            _check = check()
            # Set our HTTP status code if there were any errors
            if settings.WATCHMAN_ERROR_CODE != 200:
                for _type in _check:
                    if type(_check[_type]) == dict:
                        result = _check[_type]
                        if not result['ok']:
                            http_code = settings.WATCHMAN_ERROR_CODE
                    elif type(_check[_type]) == list:
                        for entry in _check[_type]:
                            for result in entry:
                                if not entry[result]['ok']:
                                    http_code = settings.WATCHMAN_ERROR_CODE
            response.update(_check)

    if len(response) == 0:
        raise Http404(_('No checks found'))

    return response, http_code, {WATCHMAN_VERSION_HEADER: __version__}


@auth
def dashboard(request):
    check_types = []

    check_list, skip_list = _get_check_params(request)

    for check in get_checks(check_list=check_list, skip_list=skip_list):
        if callable(check):
            _check = check()

            for _type in _check:
                # For other systems (eg: email, storage) _check[_type] is a
                # dictionary of status
                #
                # Example:
                # {
                #     'ok': True,  # Status
                # }
                #
                # Example:
                # {
                #     'ok': False,  # Status
                #     'error': "RuntimeError",
                #     'stacktrace': "...",
                # }
                #
                # For some systems (eg: cache, database) _check[_type] is a
                # list of dictionaries of dictionaries of statuses
                #
                # Example:
                # [
                #     {
                #         'default': {  # Cache/database name
                #             'ok': True,  # Status
                #         }
                #     },
                #     {
                #         'non-default': {  # Cache/database name
                #             'ok': False,  # Status
                #             'error': "RuntimeError",
                #             'stacktrace': "...",
                #         }
                #     },
                # ]
                #
                statuses = []

                if type(_check[_type]) == dict:
                    result = _check[_type]
                    statuses = [{
                        'name': '',
                        'ok': result['ok'],
                        'error': '' if result['ok'] else result['error'],
                        'stacktrace': '' if result['ok'] else result['stacktrace'],
                    }]

                    type_overall_status = _check[_type]['ok']

                elif type(_check[_type]) == list:
                    for result in _check[_type]:
                        for name in result:
                            statuses.append({
                                'name': name,
                                'ok': result[name]['ok'],
                                'error': '' if result[name]['ok'] else result[name]['error'],
                                'stacktrace': '' if result[name]['ok'] else result[name]['stacktrace'],
                            })

                    type_overall_status = all([s['ok'] for s in statuses])

                check_types.append({
                    'type': _type,
                    'ok': type_overall_status,
                    'statuses': statuses})

    overall_status = all([type_status['ok'] for type_status in check_types])

    response = render(request, 'watchman/dashboard.html', {
        'checks': check_types,
        'overall_status': overall_status
    })

    response[WATCHMAN_VERSION_HEADER] = __version__
    return response
