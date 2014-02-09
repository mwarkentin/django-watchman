from django.conf import settings
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from functools import wraps

from watchman import settings as watchman_settings


def token_required(view_func):
    """Decorator which ensures the user has provided a correct user and token pair."""

    @csrf_exempt
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        watchman_token = watchman_settings.WATCHMAN_TOKEN
        watchman_token_name = watchman_settings.WATCHMAN_TOKEN_NAME
        if watchman_token is None or watchman_token == request.GET.get(watchman_token_name):
            return view_func(request, *args, **kwargs)

        return HttpResponseForbidden()

    return _wrapped_view
