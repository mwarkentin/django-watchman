from collections.abc import Generator
from typing import Any

from django.core import cache as django_cache
from django.core.cache.backends.base import BaseCache
from django.utils.module_loading import import_string

from watchman.settings import WATCHMAN_CHECKS


def get_cache(cache_name: str) -> BaseCache:
    return django_cache.caches[cache_name]


def get_checks(
    check_list: list[str] | None = None,
    skip_list: list[str] | None = None,
) -> Generator[Any]:
    checks_to_run = frozenset(WATCHMAN_CHECKS)

    if check_list is not None:
        checks_to_run = checks_to_run.intersection(check_list)
    if skip_list is not None:
        checks_to_run = checks_to_run.difference(skip_list)

    for python_path in checks_to_run:
        yield import_string(python_path)
