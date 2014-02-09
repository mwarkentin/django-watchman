from django.conf import settings
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from functools import wraps

from watchman.settings import WATCHMAN_TOKEN, WATCHMAN_TOKEN_NAME


def token_required(view_func):
    """Decorator which ensures the user has provided a correct user and token pair."""

    @csrf_exempt
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if WATCHMAN_TOKEN is None or WATCHMAN_TOKEN == request.GET.get(WATCHMAN_TOKEN_NAME):
            return view_func(request, *args, **kwargs)

        return HttpResponseForbidden()

    return _wrapped_view
