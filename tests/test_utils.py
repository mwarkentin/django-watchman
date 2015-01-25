#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-watchman
------------

Tests for `django-watchman` decorators module.
"""

from __future__ import unicode_literals

import unittest

from watchman.utils import get_checks


class TestWatchman(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_checks_returns_all_available_checks_by_default(self):
        self.assertEqual([check.__name__ for check in get_checks()], ['caches_status', 'email_status', 'databases_status'])

    def test_get_checks_with_check_list_returns_union(self):
        check_list = ['watchman.checks.caches_status']
        self.assertEqual([check.__name__ for check in get_checks(check_list=check_list)], ['caches_status'])

    def test_get_checks_with_skip_list_returns_difference(self):
        skip_list = ['watchman.checks.caches_status']
        self.assertEqual([check.__name__ for check in get_checks(skip_list=skip_list)], ['databases_status', 'email_status'])

    def test_get_checks_with_matching_check_and_skip_list_returns_empty_list(self):
        check_list, skip_list = ['watchman.checks.caches_status'], ['watchman.checks.caches_status']
        self.assertEqual([check.__name__ for check in get_checks(check_list=check_list, skip_list=skip_list)], [])

    def test_get_checks_with_check_and_skip_list(self):
        check_list = ['watchman.checks.caches_status', 'watchman.checks.databases_status']
        skip_list = ['watchman.checks.caches_status']
        self.assertEqual([check.__name__ for check in get_checks(check_list=check_list, skip_list=skip_list)], ['databases_status'])
