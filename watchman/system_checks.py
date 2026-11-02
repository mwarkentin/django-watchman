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

    Registered as a deployment check, so it only runs with
    ``manage.py check --deploy``. It fires when the default
    ``token_required`` decorator is in use but ``WATCHMAN_TOKENS`` is unset,
    which lets every request through.
    """
    auth_decorator = getattr(
        settings, "WATCHMAN_AUTH_DECORATOR", DEFAULT_AUTH_DECORATOR
    )
    tokens = getattr(settings, "WATCHMAN_TOKENS", None)

    if auth_decorator == DEFAULT_AUTH_DECORATOR and not tokens:
        return [
            Warning(
                "The watchman status endpoint and dashboard don't require "
                "authentication.",
                hint=(
                    "Set WATCHMAN_TOKENS, or set WATCHMAN_AUTH_DECORATOR to your "
                    "own decorator. If access is already restricted another way, "
                    "such as at a proxy, add 'watchman.W001' to "
                    "SILENCED_SYSTEM_CHECKS."
                ),
                id="watchman.W001",
            )
        ]
    return []
