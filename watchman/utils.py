"""Utility helpers used internally by watchman checks and views."""

from collections.abc import Generator
from typing import Any

from django.core import cache as django_cache
from django.core.cache.backends.base import BaseCache
from django.utils.module_loading import import_string

from watchman.settings import WATCHMAN_CHECKS


def get_cache(cache_name: str) -> BaseCache:
    """Return the Django cache backend for *cache_name*."""
    return django_cache.caches[cache_name]


def get_checks(
    check_list: list[str] | None = None,
    skip_list: list[str] | None = None,
) -> Generator[Any]:
    """Yield callable check functions from [`WATCHMAN_CHECKS`][watchman.settings.WATCHMAN_CHECKS].

    Args:
        check_list: If provided, only checks whose dotted path is in this list
            are yielded.
        skip_list: If provided, checks whose dotted path is in this list are
            excluded.

    Yields:
        Callable check functions resolved via `import_string`.
    """
    if isinstance(WATCHMAN_CHECKS, str):
        raise TypeError(
            "WATCHMAN_CHECKS should be a list or tuple of dotted paths, not a "
            "string. If you have a single check, use a list: "
            "WATCHMAN_CHECKS = ['module.path.to.callable'] "
            "or a tuple with a trailing comma: "
            "WATCHMAN_CHECKS = ('module.path.to.callable',)"
        )

    checks_to_run = frozenset(WATCHMAN_CHECKS)

    if check_list is not None:
        checks_to_run = checks_to_run.intersection(check_list)
    if skip_list is not None:
        checks_to_run = checks_to_run.difference(skip_list)

    for python_path in checks_to_run:
        yield import_string(python_path)
