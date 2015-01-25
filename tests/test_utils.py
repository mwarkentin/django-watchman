#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-watchman
------------

Tests for `django-watchman` utils module.
"""

from __future__ import unicode_literals

import unittest

from watchman.utils import get_checks


class TestWatchman(unittest.TestCase):

    def assertListsEqual(self, l1, l2):
        try:
            # Python 3.4
            self.assertCountEqual(l1, l2)
        except AttributeError:
            # Python 2.7
            self.assertItemsEqual(l1, l2)

    def setUp(self):
        pass

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
