"""Decorators used to protect and wrap watchman views and checks."""

import logging
import traceback
from collections.abc import Callable
from functools import wraps
from typing import Any

from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from watchman import settings
from watchman.types import CheckResult, CheckStatus

logger: logging.Logger = logging.getLogger("watchman")


def check(func: Callable[..., CheckResult]) -> Callable[..., CheckResult]:
    """Decorator that wraps a check function and converts exceptions into error results.

    If the wrapped function raises, the exception is caught and returned as a
    `CheckStatus` with ``ok=False``, the error message, and a stacktrace.
    """

    def wrapped(*args: Any, **kwargs: Any) -> CheckResult:
        check_name = getattr(func, "__name__", repr(func))
        arg_name = None
        if args:
            arg_name = args[0]
        try:
            if arg_name:
                logger.debug("Checking '%s' for '%s'", check_name, arg_name)
            else:
                logger.debug("Checking '%s'", check_name)
            response: CheckResult = func(*args, **kwargs)
        except Exception as e:
            message = str(e)
            error_status: CheckStatus = {
                "ok": False,
                "error": message,
                "stacktrace": traceback.format_exc(),
            }
            # The check contains several individual checks (e.g., one per
            # database). Preface the results by name.
            if arg_name:
                named_result: dict[str, CheckStatus] = {arg_name: error_status}
                response = named_result
                logger.exception(
                    "Error calling '%s' for '%s': %s", check_name, arg_name, message
                )
            else:
                response = error_status
                logger.exception("Error calling '%s': %s", check_name, message)

        return response

    return wrapped


def parse_auth_header(auth_header: str) -> str:
    """Parse the ``Authorization`` header and return the token value.

    Expected format: ``WATCHMAN-TOKEN Token="ABC123"``

    Raises :exc:`KeyError` when no ``Token`` parameter is found.
    """

    for part in auth_header.split():
        key, sep, value = part.partition("=")
        if sep and key == "Token":
            return value.strip('"')
    raise KeyError("Token")


def token_required(
    view_func: Callable[..., HttpResponse],
) -> Callable[..., HttpResponse]:
    """Decorator that enforces token-based authentication on a view.

    When [`WATCHMAN_TOKENS`][watchman.settings.WATCHMAN_TOKENS] (or the
    deprecated `WATCHMAN_TOKEN`) is set, the request must supply a matching
    token via the ``Authorization`` header or a query parameter named by
    [`WATCHMAN_TOKEN_NAME`][watchman.settings.WATCHMAN_TOKEN_NAME].

    Returns an ``HTTP 403`` response when the token is missing or invalid.
    """

    def _get_passed_token(request: HttpRequest) -> str | None:
        """
        Try to get the passed token, starting with the header and fall back to `GET` param
        """

        try:
            auth_header = request.META["HTTP_AUTHORIZATION"]
            token = parse_auth_header(auth_header)
        except KeyError:
            token = request.GET.get(settings.WATCHMAN_TOKEN_NAME)
        return token

    def _validate_token(request: HttpRequest) -> bool:
        if settings.WATCHMAN_TOKENS:
            watchman_tokens = settings.WATCHMAN_TOKENS.split(",")
        elif settings.WATCHMAN_TOKEN:
            watchman_tokens = [
                settings.WATCHMAN_TOKEN,
            ]
        else:
            return True

        return _get_passed_token(request) in watchman_tokens

    @csrf_exempt
    @wraps(view_func)
    def _wrapped_view(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if _validate_token(request):
            return view_func(request, *args, **kwargs)

        return HttpResponseForbidden()

    return _wrapped_view


if settings.WATCHMAN_AUTH_DECORATOR is None:

    def auth(view_func: Callable[..., HttpResponse]) -> Callable[..., HttpResponse]:
        @csrf_exempt
        @wraps(view_func)
        def _wrapped_view(
            request: HttpRequest, *args: Any, **kwargs: Any
        ) -> HttpResponse:
            return view_func(request, *args, **kwargs)

        return _wrapped_view

elif settings.WATCHMAN_AUTH_DECORATOR == "watchman.decorators.token_required":
    # Avoid import loops
    auth = token_required
else:
    from importlib import import_module

    mod_name, dec = settings.WATCHMAN_AUTH_DECORATOR.rsplit(".", 1)
    auth = getattr(import_module(mod_name), dec)
