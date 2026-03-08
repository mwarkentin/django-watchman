"""Resolved watchman settings with their defaults.

All settings are read from your Django ``settings`` module via ``getattr``
with sensible defaults.  See the [Configuration](../configuration.md) guide for
full usage details.
"""

from typing import Any

from django.conf import settings

from watchman.constants import DEFAULT_CHECKS, PAID_CHECKS

WATCHMAN_ENABLE_PAID_CHECKS: bool = getattr(
    settings, "WATCHMAN_ENABLE_PAID_CHECKS", False
)
"""Include paid checks (e.g. email) in the default check list.  Default: ``False``."""

WATCHMAN_AUTH_DECORATOR: str | None = getattr(
    settings, "WATCHMAN_AUTH_DECORATOR", "watchman.decorators.token_required"
)
"""Dotted path to a decorator applied to protected views. Set to ``None`` to
disable authentication.  Default: ``"watchman.decorators.token_required"``."""

WATCHMAN_TOKENS: str | None = getattr(settings, "WATCHMAN_TOKENS", None)
"""Comma-separated list of accepted authentication tokens.  Default: ``None``
(no token required)."""

WATCHMAN_TOKEN_NAME: str = getattr(settings, "WATCHMAN_TOKEN_NAME", "watchman-token")
"""Name of the query-string parameter used to pass the token.
Default: ``"watchman-token"``."""

WATCHMAN_ERROR_CODE: int = getattr(settings, "WATCHMAN_ERROR_CODE", 500)
"""HTTP status code returned when a check fails.  Default: ``500``."""

WATCHMAN_EMAIL_SENDER: str = getattr(
    settings, "WATCHMAN_EMAIL_SENDER", "watchman@example.com"
)
"""``From`` address for the email check.  Default: ``"watchman@example.com"``."""

WATCHMAN_EMAIL_RECIPIENTS: list[str] = getattr(
    settings, "WATCHMAN_EMAIL_RECIPIENTS", ["to@example.com"]
)
"""List of ``To`` addresses for the email check.  Default: ``["to@example.com"]``."""

WATCHMAN_EMAIL_HEADERS: dict[str, str] = getattr(settings, "WATCHMAN_EMAIL_HEADERS", {})
"""Extra headers added to the test email.  Default: ``{}``."""

WATCHMAN_CACHES: dict[str, Any] = getattr(settings, "WATCHMAN_CACHES", settings.CACHES)
"""Cache aliases to check.  Defaults to Django's ``CACHES`` setting."""

WATCHMAN_DATABASES: dict[str, Any] = getattr(
    settings, "WATCHMAN_DATABASES", settings.DATABASES
)
"""Database aliases to check.  Defaults to Django's ``DATABASES`` setting."""

WATCHMAN_DISABLE_APM: bool = getattr(settings, "WATCHMAN_DISABLE_APM", False)
"""Suppress APM tracing (New Relic, Datadog) for watchman views.  Default: ``False``."""

WATCHMAN_STORAGE_PATH: str = getattr(
    settings, "WATCHMAN_STORAGE_PATH", settings.MEDIA_ROOT
)
"""Subdirectory within the default storage backend used for the storage check.
Defaults to ``MEDIA_ROOT``."""

_checks: tuple[str, ...] = DEFAULT_CHECKS

if WATCHMAN_ENABLE_PAID_CHECKS:
    _checks = DEFAULT_CHECKS + PAID_CHECKS

WATCHMAN_CHECKS: tuple[str, ...] = getattr(settings, "WATCHMAN_CHECKS", _checks)
"""Tuple of dotted paths to check functions that watchman will execute.
Defaults to [`DEFAULT_CHECKS`][watchman.constants.DEFAULT_CHECKS] (plus
[`PAID_CHECKS`][watchman.constants.PAID_CHECKS] when
[`WATCHMAN_ENABLE_PAID_CHECKS`][watchman.settings.WATCHMAN_ENABLE_PAID_CHECKS]
is ``True``)."""

EXPOSE_WATCHMAN_VERSION: bool = getattr(settings, "EXPOSE_WATCHMAN_VERSION", False)
"""Add an ``X-Watchman-Version`` header to responses.  Default: ``False``."""
