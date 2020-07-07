# -*- coding: utf-8 -*-

from django.core import cache as django_cache
from django.utils.module_loading import import_string

from watchman.settings import WATCHMAN_CHECKS


imported_checks = {}


def import_check(python_path):
    if python_path not in imported_checks:
        imported_checks[python_path] = import_string(python_path)
    return imported_checks[python_path]


def get_cache(cache_name):
    return django_cache.caches[cache_name]


def get_checks(check_list=None, skip_list=None):
    checks_to_run = frozenset(WATCHMAN_CHECKS)

    if check_list is not None:
        checks_to_run = checks_to_run.intersection(check_list)
    if skip_list is not None:
        checks_to_run = checks_to_run.difference(skip_list)

    for python_path in checks_to_run:
        yield import_check(python_path)
