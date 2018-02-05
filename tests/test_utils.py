# -*- coding: utf-8 -*-

"""
test_django-watchman
------------

Tests for `django-watchman` utils module.
"""

from __future__ import unicode_literals

import unittest

import django
from mock import patch

from watchman.utils import get_cache, get_checks


class TestWatchman(unittest.TestCase):

    def assert_lists_equal(self, list1, list2):
        try:
            # Python 3
            self.assertCountEqual(list1, list2)
        except AttributeError:
            # Python 2
            self.assertItemsEqual(list1, list2)

    @unittest.skipIf(
        django.VERSION < (1, 7),
        'caches interface is not added until Django 1.7',
    )
    @patch('watchman.utils.django_cache.caches', spec_set=dict)
    def test_get_cache_django_17_or_greater(self, get_cache_mock):
        get_cache('foo')
        get_cache_mock.__getitem__.called_once_with('foo')

    @unittest.skipIf(
        django.VERSION >= (1, 7),
        'get_cache has been deprecated as of Django 1.7'
    )
    @patch('django.core.cache.get_cache')
    def test_get_cache_less_than_django_17(self, get_cache_mock):
        get_cache('foo')
        get_cache_mock.assert_called_once_with('foo')

    def test_get_checks_returns_all_available_checks_by_default(self):
        checks = [check.__name__ for check in get_checks()]
        expected_checks = ['caches', 'databases', 'storage']
        self.assert_lists_equal(checks, expected_checks)

    def test_get_checks_with_check_list_returns_union(self):
        check_list = ['watchman.checks.caches']
        checks = [check.__name__ for check in get_checks(check_list=check_list)]
        expected_checks = ['caches']
        self.assert_lists_equal(checks, expected_checks)

    def test_get_checks_with_skip_list_returns_difference(self):
        skip_list = ['watchman.checks.caches']
        checks = [check.__name__ for check in get_checks(skip_list=skip_list)]
        expected_checks = ['databases', 'storage']
        self.assert_lists_equal(checks, expected_checks)

    def test_get_checks_with_matching_check_and_skip_list_returns_empty_list(self):
        check_list, skip_list = ['watchman.checks.caches'], ['watchman.checks.caches']
        checks = [check.__name__ for check in get_checks(check_list=check_list, skip_list=skip_list)]
        expected_checks = []
        self.assert_lists_equal(checks, expected_checks)

    def test_get_checks_with_check_and_skip_list(self):
        check_list = ['watchman.checks.caches', 'watchman.checks.databases']
        skip_list = ['watchman.checks.caches']
        checks = [check.__name__ for check in get_checks(check_list=check_list, skip_list=skip_list)]
        expected_checks = ['databases']
        self.assert_lists_equal(checks, expected_checks)

    def test_get_checks_with_paid_checks_disabled_returns_expected_checks(self):
        expected_checks = ['caches', 'databases', 'storage']
        checks = [check.__name__ for check in get_checks()]
        self.assert_lists_equal(checks, expected_checks)

    @unittest.skip("Unsure how to test w/ modified settings")
    def test_get_checks_with_paid_checks_enabled_returns_expected_checks(self):
        pass
