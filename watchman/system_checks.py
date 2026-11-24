"""Django system checks for watchman configuration.

These are Django's ``manage.py check`` checks, not watchman health checks
(see [`watchman.checks`][watchman.checks]).
"""

from typing import Any

from django.conf import settings
from django.core.checks import CheckMessage, Warning

DEFAULT_AUTH_DECORATOR = "watchman.decorators.token_required"


def check_endpoint_authentication(
    app_configs: Any = None, **kwargs: Any
) -> list[CheckMessage]:
    """Warn when the status endpoint and dashboard are open to anyone.

    Fires when the default ``token_required`` decorator is in use but
    ``WATCHMAN_TOKENS`` is unset, which lets every request through. In
    django-watchman 3.0 those requests will be denied, so this also warns
    about that change.
    """
    auth_decorator = getattr(
        settings, "WATCHMAN_AUTH_DECORATOR", DEFAULT_AUTH_DECORATOR
    )
    tokens = getattr(settings, "WATCHMAN_TOKENS", None)

    if auth_decorator == DEFAULT_AUTH_DECORATOR and not tokens:
        return [
            Warning(
                "WATCHMAN_TOKENS isn't set, so the watchman status endpoint and "
                "dashboard don't require authentication. In django-watchman 3.0 "
                "they will deny every request instead.",
                hint=(
                    "Set WATCHMAN_TOKENS to require a token, or set "
                    "WATCHMAN_AUTH_DECORATOR = None to keep the endpoint open. "
                    "Health checks that can't send a token can use the "
                    "watchman ping endpoint or the bare_status view, which "
                    "don't require authentication."
                ),
                id="watchman.W001",
            )
        ]
    return []
