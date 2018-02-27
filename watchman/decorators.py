from functools import wraps
import logging
import re
import traceback

from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from watchman import settings

logger = logging.getLogger('watchman')


def check(func):
    """
    Decorator which wraps checks and returns an error response on failure.
    """
    def wrapped(*args, **kwargs):
        check_name = func.__name__
        arg_name = None
        if args:
            arg_name = args[0]
        try:
            if arg_name:
                logger.debug("Checking '%s' for '%s'", check_name, arg_name)
            else:
                logger.debug("Checking '%s'", check_name)
            response = func(*args, **kwargs)
        except Exception as e:
            message = str(e)
            response = {
                "ok": False,
                "error": message,
                "stacktrace": traceback.format_exc(),
            }
            # The check contains several individual checks (e.g., one per
            # database). Preface the results by name.
            if arg_name:
                response = {arg_name: response}
                logger.exception(
                    "Error calling '%s' for '%s': %s",
                    check_name,
                    arg_name,
                    message
                )
            else:
                logger.exception(
                    "Error calling '%s': %s",
                    check_name,
                    message
                )

        return response
    return wrapped


def token_required(view_func):
    """
    Decorator which ensures that one of the WATCHMAN_TOKENS is provided if set.

    WATCHMAN_TOKEN_NAME can also be set if the token GET parameter must be
    customized.

    """

    def _parse_auth_header(auth_header):
        """
        Parse the `Authorization` header

        Expected format: `WATCHMAN-TOKEN Token="ABC123"`
        """

        # TODO: Figure out full set of allowed characters
        # http://stackoverflow.com/questions/19028068/illegal-characters-in-http-headers
        # https://www.w3.org/Protocols/rfc2616/rfc2616-sec2.html#sec2.2
        # https://www.w3.org/Protocols/rfc2616/rfc2616-sec4.html#sec4.2
        reg = re.compile('(\w+)[=] ?"?([\w-]+)"?')
        header_dict = dict(reg.findall(auth_header))
        return header_dict['Token']

    def _get_passed_token(request):
        """
        Try to get the passed token, starting with the header and fall back to `GET` param
        """

        try:
            auth_header = request.META['HTTP_AUTHORIZATION']
            token = _parse_auth_header(auth_header)
        except KeyError:
            token = request.GET.get(settings.WATCHMAN_TOKEN_NAME)
        return token

    def _validate_token(request):
        if settings.WATCHMAN_TOKENS:
            watchman_tokens = settings.WATCHMAN_TOKENS.split(',')
        elif settings.WATCHMAN_TOKEN:
            watchman_tokens = [settings.WATCHMAN_TOKEN, ]
        else:
            return True

        return _get_passed_token(request) in watchman_tokens

    @csrf_exempt
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if _validate_token(request):
            return view_func(request, *args, **kwargs)

        return HttpResponseForbidden()

    return _wrapped_view


if settings.WATCHMAN_AUTH_DECORATOR is None:
    def auth(view_func):
        @csrf_exempt
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)

        return _wrapped_view
elif settings.WATCHMAN_AUTH_DECORATOR == 'watchman.decorators.token_required':
    # Avoid import loops
    auth = token_required
else:
    try:
        from importlib import import_module
    except ImportError:  # Django < 1.8
        from django.utils.importlib import import_module

    mod_name, dec = settings.WATCHMAN_AUTH_DECORATOR.rsplit('.', 1)
    auth = getattr(import_module(mod_name), dec)
