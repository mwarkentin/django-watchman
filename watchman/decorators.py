from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from functools import wraps
import traceback

from watchman import settings


def check(func):
    """
    Decorator which wraps checks and returns an error response on failure.
    """
    def wrapped(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
        except Exception as e:
            response = {
                "ok": False,
                "error": str(e),
                "stacktrace": traceback.format_exc(),
            }
            # The check contains several individual checks (e.g., one per
            # database). Preface the results by name.
            if args:
                response = {args[0]: response}
        return response
    return wrapped


def token_required(view_func):
    """
    Decorator which ensures that WATCHMAN_TOKEN is provided if set.

    WATCHMAN_TOKEN_NAME can also be set if the token GET parameter must be
    customized.

    """

    def _validate_token(request):
        watchman_token = settings.WATCHMAN_TOKEN
        if watchman_token is None:
            return True

        watchman_token_name = settings.WATCHMAN_TOKEN_NAME
        return watchman_token == request.GET.get(watchman_token_name)

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
