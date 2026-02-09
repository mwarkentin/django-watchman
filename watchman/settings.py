from typing import Any

from django.conf import settings

from watchman.constants import DEFAULT_CHECKS, PAID_CHECKS

# TODO: these should not be module level (https://github.com/mwarkentin/django-watchman/issues/13)
WATCHMAN_ENABLE_PAID_CHECKS: bool = getattr(
    settings, "WATCHMAN_ENABLE_PAID_CHECKS", False
)
WATCHMAN_AUTH_DECORATOR: str | None = getattr(
    settings, "WATCHMAN_AUTH_DECORATOR", "watchman.decorators.token_required"
)
# TODO: Remove for django-watchman 1.0
WATCHMAN_TOKEN: str | None = getattr(settings, "WATCHMAN_TOKEN", None)
WATCHMAN_TOKENS: str | None = getattr(settings, "WATCHMAN_TOKENS", None)
WATCHMAN_TOKEN_NAME: str = getattr(settings, "WATCHMAN_TOKEN_NAME", "watchman-token")
WATCHMAN_ERROR_CODE: int = getattr(settings, "WATCHMAN_ERROR_CODE", 500)
WATCHMAN_EMAIL_SENDER: str = getattr(
    settings, "WATCHMAN_EMAIL_SENDER", "watchman@example.com"
)
WATCHMAN_EMAIL_RECIPIENTS: list[str] = getattr(
    settings, "WATCHMAN_EMAIL_RECIPIENTS", ["to@example.com"]
)
WATCHMAN_EMAIL_HEADERS: dict[str, str] = getattr(settings, "WATCHMAN_EMAIL_HEADERS", {})

WATCHMAN_CACHES: dict[str, Any] = getattr(settings, "WATCHMAN_CACHES", settings.CACHES)
WATCHMAN_DATABASES: dict[str, Any] = getattr(
    settings, "WATCHMAN_DATABASES", settings.DATABASES
)

WATCHMAN_DISABLE_APM: bool = getattr(settings, "WATCHMAN_DISABLE_APM", False)

WATCHMAN_STORAGE_PATH: str = getattr(
    settings, "WATCHMAN_STORAGE_PATH", settings.MEDIA_ROOT
)

_checks: tuple[str, ...] = DEFAULT_CHECKS

if WATCHMAN_ENABLE_PAID_CHECKS:
    _checks = DEFAULT_CHECKS + PAID_CHECKS

WATCHMAN_CHECKS: tuple[str, ...] = getattr(settings, "WATCHMAN_CHECKS", _checks)

EXPOSE_WATCHMAN_VERSION: bool = getattr(settings, "EXPOSE_WATCHMAN_VERSION", False)
