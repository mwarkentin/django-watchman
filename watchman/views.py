"""Django views that expose watchman health-check endpoints.

The three main endpoints are:

* **status** -- JSON response with the results of all configured checks.
* **dashboard** -- HTML page summarising check results.
* **ping** -- Lightweight ``pong`` response for simple uptime monitoring.
"""

import warnings
from typing import Any

from django.db.transaction import non_atomic_requests
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext as _

from watchman import __version__, settings
from watchman.decorators import auth
from watchman.utils import get_checks

WATCHMAN_VERSION_HEADER: str = "X-Watchman-Version"


def _get_check_params(
    request: HttpRequest,
) -> tuple[list[str] | None, list[str] | None]:
    check_list: list[str] | None = None
    skip_list: list[str] | None = None

    if len(request.GET) > 0:
        if "check" in request.GET:
            check_list = request.GET.getlist("check")
        if "skip" in request.GET:
            skip_list = request.GET.getlist("skip")

    return (check_list, skip_list)


def _deprecation_warnings() -> None:
    if settings.WATCHMAN_TOKEN:
        warnings.warn(
            "`WATCHMAN_TOKEN` setting is deprecated, use `WATCHMAN_TOKENS` instead. It will be removed in django-watchman 1.0",
            DeprecationWarning,
            stacklevel=2,
        )


def _disable_apm() -> None:
    # New Relic
    try:
        import newrelic.agent

        newrelic.agent.ignore_transaction(flag=True)
    except ImportError:
        pass
    # Datadog
    try:
        from ddtrace import tracer
        from ddtrace.constants import MANUAL_DROP_KEY

        tracer.current_span().set_tag(MANUAL_DROP_KEY)
    except (AttributeError, ImportError):
        pass


def run_checks(request: HttpRequest) -> tuple[dict[str, Any], bool]:
    """Execute all configured health checks and return the aggregated results.

    Reads ``check`` and ``skip`` query parameters from *request* to allow
    callers to filter which checks are executed.

    Returns:
        A ``(checks, ok)`` tuple where *checks* is a dictionary of check
        results and *ok* is ``False`` when any check reported an error
        (and [`WATCHMAN_ERROR_CODE`][watchman.settings.WATCHMAN_ERROR_CODE]
        is not ``200``).
    """
    _deprecation_warnings()

    if settings.WATCHMAN_DISABLE_APM:
        _disable_apm()

    checks: dict[str, Any] = {}
    ok: bool = True

    check_list, skip_list = _get_check_params(request)

    for check in get_checks(check_list=check_list, skip_list=skip_list):
        if callable(check):
            _check = check()
            # Set our HTTP status code if there were any errors
            if settings.WATCHMAN_ERROR_CODE != 200:
                for _type in _check:
                    if isinstance(_check[_type], dict):
                        result = _check[_type]
                        if not result["ok"]:
                            ok = False
                    elif isinstance(_check[_type], list):
                        for entry in _check[_type]:
                            for result in entry:
                                if not entry[result]["ok"]:
                                    ok = False
            checks.update(_check)

    return checks, ok


@auth
@non_atomic_requests
def status(request: HttpRequest) -> HttpResponse:
    """Return JSON health-check results for all configured checks.

    Protected by the configured
    [`WATCHMAN_AUTH_DECORATOR`][watchman.settings.WATCHMAN_AUTH_DECORATOR].

    **Example response:**

        {
            "caches": [{"default": {"ok": true}}],
            "databases": [{"default": {"ok": true}}],
            "storage": {"ok": true}
        }

    Query parameters:
        check: Run only the specified checks (repeatable).
        skip: Skip the specified checks (repeatable).
    """
    checks, ok = run_checks(request)

    if not checks:
        response = JsonResponse(
            {
                "error": 404,
                "message": _("No checks found"),
            },
            status=404,
        )
    else:
        http_code = 200 if ok else settings.WATCHMAN_ERROR_CODE
        response = JsonResponse(checks, status=http_code)

    if settings.EXPOSE_WATCHMAN_VERSION:
        response[WATCHMAN_VERSION_HEADER] = __version__

    return response


@non_atomic_requests
def bare_status(request: HttpRequest) -> HttpResponse:
    """Return an empty ``text/plain`` response whose status code reflects overall health.

    Unlike [`status`][watchman.views.status], this view has **no** auth
    decorator and returns no body -- only the HTTP status code matters.
    Useful for load-balancer health checks that only inspect the status code.
    """
    checks, ok = run_checks(request)
    http_code = 200 if ok else settings.WATCHMAN_ERROR_CODE
    return HttpResponse(status=http_code, content_type="text/plain")


def ping(request: HttpRequest) -> HttpResponse:
    """Return a plain-text ``pong`` response.

    This is the simplest possible liveness probe -- it does **not** run any
    backing-service checks.  Useful for Kubernetes liveness probes or simple
    uptime pings.
    """
    if settings.WATCHMAN_DISABLE_APM:
        _disable_apm()
    return HttpResponse("pong", content_type="text/plain")


@auth
@non_atomic_requests
def dashboard(request: HttpRequest) -> HttpResponse:
    """Render an HTML dashboard showing the status of all configured checks.

    Protected by the configured
    [`WATCHMAN_AUTH_DECORATOR`][watchman.settings.WATCHMAN_AUTH_DECORATOR].

    Query parameters:
        check: Run only the specified checks (repeatable).
        skip: Skip the specified checks (repeatable).
    """
    checks, overall_status = run_checks(request)

    expanded_checks: dict[str, Any] = {}
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
            single_status["name"] = ""
            expanded_check: dict[str, Any] = {
                "ok": value["ok"],
                "statuses": [single_status],
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
            statuses: list[dict[str, Any]] = []
            for outer_status in value:
                for name, inner_status in outer_status.items():
                    detail = inner_status.copy()
                    detail["name"] = name
                    statuses.append(detail)

            expanded_check = {
                "ok": all(detail["ok"] for detail in statuses),
                "statuses": statuses,
            }
        expanded_checks[key] = expanded_check

    response = render(
        request,
        "watchman/dashboard.html",
        {
            "checks": expanded_checks,
            "overall_status": overall_status,
            "watchman_version": __version__,
            "expose_watchman_version": settings.EXPOSE_WATCHMAN_VERSION,
        },
    )

    if settings.EXPOSE_WATCHMAN_VERSION:
        response[WATCHMAN_VERSION_HEADER] = __version__

    return response
