from django.conf import settings
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from functools import wraps

def token_required(view_func):
    """Decorator which ensures the user has provided a correct user and token pair."""

    @csrf_exempt
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        required_token = getattr(settings, 'WATCHMAN_TOKEN', None)
        token_name = getattr(settings, 'WATCHMAN_TOKEN_NAME', 'watchman-token')
        if required_token is None or required_token == request.GET.get(token_name):
            return view_func(request, *args, **kwargs)

        return HttpResponseForbidden()

    return _wrapped_view
