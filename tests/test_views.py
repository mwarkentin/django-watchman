#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-watchman
------------

Tests for `django-watchman` views module.
"""

import json
import unittest

from mock import patch

from watchman import views


class TestWatchman(unittest.TestCase):

    def setUp(self):
        pass

    @patch('watchman.views.check_databases')
    def test_response_contains_expected_checks(self, patched_check_databases):
        expected_checks = ['databases']
        patched_check_databases.return_value = []
        response = views.status('')
        content = json.loads(response.content)
        self.assertItemsEqual(expected_checks, content.keys())

    def tearDown(self):
        pass
