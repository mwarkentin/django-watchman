# -*- coding: utf-8 -*-

"""
test_django-watchman
------------

Tests for `django-watchman` utils module.
"""

from __future__ import unicode_literals

import unittest

from mock import patch

from watchman.utils import get_cache, get_checks


class TestWatchman(unittest.TestCase):

    def assertListsEqual(self, list1, list2):
        try:
            # Python 3.4
            self.assertCountEqual(list1, list2)
        except AttributeError:
            # Python 2.7
            self.assertItemsEqual(list1, list2)

    @patch('watchman.utils.django_cache')
    def test_get_cache(self, cache_mock):
        cache_key = 'my_cache'
        cache_value = 'i am a cache'
        cache = {cache_key: cache_value}

        def getitem(cache_name):
            return cache[cache_name]

        cache_mock.caches.__getitem__.side_effect = getitem

        result = get_cache(cache_key)

        self.assertEqual(result, cache_value)

    @unittest.skip("Seems to be blowing up on Django 1.9")
    @patch('django.core.cache.get_cache')
    @patch('watchman.utils.django')
    def test_get_cache_less_than_django_17(self, django_mock, get_cache_mock):
        django_mock.VERSION = (1, 6, 6, 'final', 0)

        get_cache('foo')

        get_cache_mock.assert_called_once_with('foo')

    def test_get_checks_returns_all_available_checks_by_default(self):
        checks = [check.__name__ for check in get_checks()]
        expected_checks = ['caches', 'databases', 'storage']
        self.assertListsEqual(checks, expected_checks)

    def test_get_checks_with_check_list_returns_union(self):
        check_list = ['watchman.checks.caches']
        checks = [check.__name__ for check in get_checks(check_list=check_list)]
        expected_checks = ['caches']
        self.assertListsEqual(checks, expected_checks)

    def test_get_checks_with_skip_list_returns_difference(self):
        skip_list = ['watchman.checks.caches']
        checks = [check.__name__ for check in get_checks(skip_list=skip_list)]
        expected_checks = ['databases', 'storage']
        self.assertListsEqual(checks, expected_checks)

    def test_get_checks_with_matching_check_and_skip_list_returns_empty_list(self):
        check_list, skip_list = ['watchman.checks.caches'], ['watchman.checks.caches']
        checks = [check.__name__ for check in get_checks(check_list=check_list, skip_list=skip_list)]
        expected_checks = []
        self.assertListsEqual(checks, expected_checks)

    def test_get_checks_with_check_and_skip_list(self):
        check_list = ['watchman.checks.caches', 'watchman.checks.databases']
        skip_list = ['watchman.checks.caches']
        checks = [check.__name__ for check in get_checks(check_list=check_list, skip_list=skip_list)]
        expected_checks = ['databases']
        self.assertListsEqual(checks, expected_checks)

    def test_get_checks_with_paid_checks_disabled_returns_expected_checks(self):
        expected_checks = ['caches', 'databases', 'storage']
        checks = [check.__name__ for check in get_checks()]
        self.assertListsEqual(checks, expected_checks)

    @unittest.skip("Unsure how to test w/ modified settings")
    def test_get_checks_with_paid_checks_enabled_returns_expected_checks(self):
        pass
