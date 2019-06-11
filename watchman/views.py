# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import warnings

from django.db.transaction import non_atomic_requests
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.utils.translation import ugettext as _
from jsonview.decorators import json_view
from watchman import __version__, settings
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


def _deprecation_warnings():
    if settings.WATCHMAN_TOKEN:
        warnings.warn("`WATCHMAN_TOKEN` setting is deprecated, use `WATCHMAN_TOKENS` instead. It will be removed in django-watchman 1.0", DeprecationWarning)


def _disable_apm():
    # New Relic
    try:
        import newrelic.agent
        newrelic.agent.ignore_transaction(flag=True)
    except ImportError:
        pass


def run_checks(request):
    _deprecation_warnings()

    if settings.WATCHMAN_DISABLE_APM:
        _disable_apm()

    checks = {}
    ok = True

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
                            ok = False
                    elif type(_check[_type]) == list:
                        for entry in _check[_type]:
                            for result in entry:
                                if not entry[result]['ok']:
                                    ok = False
            checks.update(_check)

    return checks, ok


@auth
@json_view
@non_atomic_requests
def status(request):
    checks, ok = run_checks(request)

    if not checks:
        raise Http404(_('No checks found'))

    http_code = 200 if ok else settings.WATCHMAN_ERROR_CODE

    response_headers = {}
    if settings.EXPOSE_WATCHMAN_VERSION:
        response_headers[WATCHMAN_VERSION_HEADER] = __version__

    return checks, http_code, response_headers


@non_atomic_requests
def bare_status(request):
    checks, ok = run_checks(request)
    http_code = 200 if ok else settings.WATCHMAN_ERROR_CODE
    return HttpResponse(status=http_code, content_type='text/plain')


def ping(request):
    if settings.WATCHMAN_DISABLE_APM:
        _disable_apm()
    return HttpResponse('pong', content_type='text/plain')


@auth
@non_atomic_requests
def dashboard(request):
    checks, overall_status = run_checks(request)

    expanded_checks = {}
    for key, value in checks.items():
        if isinstance(value, dict):
            # For some systems (eg: email, storage) value is a
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
            single_status = value.copy()
            single_status['name'] = ''
            expanded_check = {
                'ok': value['ok'],
                'statuses': [single_status],
            }
        else:
            # For other systems (eg: cache, database) value is a
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
            statuses = []
            for outer_status in value:
                for name, inner_status in outer_status.items():
                    detail = inner_status.copy()
                    detail['name'] = name
                    statuses.append(detail)

            expanded_check = {
                'ok': all(detail['ok'] for detail in statuses),
                'statuses': statuses,
            }
        expanded_checks[key] = expanded_check

    response = render(request, 'watchman/dashboard.html', {
        'checks': expanded_checks,
        'overall_status': overall_status,
        'watchman_version': __version__,
        'expose_watchman_version': settings.EXPOSE_WATCHMAN_VERSION,
    })

    if settings.EXPOSE_WATCHMAN_VERSION:
        response[WATCHMAN_VERSION_HEADER] = __version__

    return response
