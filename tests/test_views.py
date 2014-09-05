#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-watchman
------------

Tests for `django-watchman` views module.
"""

from __future__ import unicode_literals

import django
import json
import unittest
import sys
from django.conf import settings
from django.test.client import RequestFactory
from mock import patch

from watchman import checks, views

PYTHON_VERSION = sys.version_info[0]

if django.VERSION >= (1, 7):
    # Initialize Django
    django.setup()

    # Silence MIDDLEWARE_CLASSES warning as this is not an actual Django project
    settings.SILENCED_SYSTEM_CHECKS = ['1_7.W001']


class TestWatchman(unittest.TestCase):

    def setUp(self):
        pass

    @patch('watchman.checks._check_databases')
    def test_response_content_type_json(self, patched_check_databases):
        patched_check_databases.return_value = []
        request = RequestFactory().get('/')
        response = views.status(request)
        self.assertEqual(response['Content-Type'], 'application/json')

    @patch('watchman.checks._check_databases')
    def test_response_contains_expected_checks(self, patched_check_databases):
        expected_checks = ['caches', 'databases']
        patched_check_databases.return_value = []
        request = RequestFactory().get('/')
        response = views.status(request)

        if PYTHON_VERSION == 2:
            content = json.loads(response.content)
            self.assertItemsEqual(expected_checks, content.keys())
        else:
            content = json.loads(response.content.decode('utf-8'))
            self.assertCountEqual(expected_checks, content.keys())

    def test_check_database_handles_exception(self):
        response = checks._check_database('foo')
        self.assertFalse(response['foo']['ok'])
        self.assertEqual(response['foo']['error'], "The connection foo doesn't exist")

    def test_check_cache_handles_exception(self):
        expected_error = "Could not find backend 'foo': Could not find backend 'foo': foo doesn't look like a module path"
        response = checks._check_cache('foo')
        self.assertFalse(response['foo']['ok'])
        self.assertIn(response['foo']['error'], expected_error)

    @patch('watchman.checks._check_databases')
    def test_response_only_single_check(self, patched_check_databases):
        patched_check_databases.return_value = []
        request = RequestFactory().get('/', data={
            'check': 'watchman.checks.databases_status',
        })
        response = views.status(request)
        self.assertEqual(response.status_code, 200)

        if PYTHON_VERSION == 2:
            content = json.loads(response.content)
            self.assertItemsEqual({'databases': []}, content)
        else:
            content = json.loads(response.content.decode('utf-8'))
            self.assertCountEqual({'databases': []}, content)

    @patch('watchman.checks._check_databases')
    def test_response_404_when_none_specified(self, patched_check_databases):
        patched_check_databases.return_value = []
        request = RequestFactory().get('/', data={
            'check': '',
        })
        response = views.status(request)
        self.assertEqual(response.status_code, 404)

        if PYTHON_VERSION == 2:
            content = json.loads(response.content)
            self.assertItemsEqual({'message': 'No checks found', 'error': 404}, content)
        else:
            content = json.loads(response.content.decode('utf-8'))
            self.assertCountEqual({'message': 'No checks found', 'error': 404}, content)

    def tearDown(self):
        pass
