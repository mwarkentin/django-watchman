from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from functools import wraps

from watchman import settings


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


if settings.WATCHMAN_LOGIN:
    from django.contrib.auth.decorators import login_required
else:
    def login_required(view_func):
        @csrf_exempt
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)

        return _wrapped_view
