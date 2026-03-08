"""Default check tuples used to populate [`WATCHMAN_CHECKS`][watchman.settings.WATCHMAN_CHECKS]."""

DEFAULT_CHECKS: tuple[str, ...] = (
    "watchman.checks.caches",
    "watchman.checks.databases",
    "watchman.checks.storage",
)
"""Checks included by default: caches, databases, and storage."""

PAID_CHECKS: tuple[str, ...] = ("watchman.checks.email",)
"""Checks that may incur cost (e.g. sending an email).  Only included when
[`WATCHMAN_ENABLE_PAID_CHECKS`][watchman.settings.WATCHMAN_ENABLE_PAID_CHECKS]
is ``True``."""
