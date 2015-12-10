# -*- coding: utf-8 -*-

"""
test_django-watchman
------------

Tests for `django-watchman` views module.
"""

from __future__ import unicode_literals

import json
try:
    from importlib import reload
except ImportError:  # Python < 3
    pass
import sys
import unittest

import django
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.test.client import RequestFactory
from django.test.utils import override_settings

from mock import patch

from watchman import checks, views

PYTHON_VERSION = sys.version_info[0]

if django.VERSION >= (1, 7):
    # Initialize Django
    django.setup()

    # Silence MIDDLEWARE_CLASSES warning as this is not an actual Django project
    settings.SILENCED_SYSTEM_CHECKS = ['1_7.W001']


def reload_settings():
    # Reload settings - and all dependent modules - from scratch
    reload(sys.modules['watchman.settings'])
    reload(sys.modules['watchman.decorators'])
    reload(sys.modules['watchman.views'])


class TestWatchman(unittest.TestCase):
    def setUp(self):
        # Ensure that every test executes with separate settings
        reload_settings()

    def test_response_content_type_json(self):
        request = RequestFactory().get('/')
        response = views.status(request)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_response_contains_expected_checks(self):
        expected_checks = ['caches', 'databases', 'storage', ]
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
        expected_error = "Could not find config for 'foo' in settings.CACHES"

        response = checks._check_cache('foo')
        self.assertFalse(response['foo']['ok'])
        self.assertIn(response['foo']['error'], expected_error)

    def test_response_skipped_checks(self):
        expected_checks = ['caches', 'storage', ]
        request = RequestFactory().get('/', data={
            'skip': 'watchman.checks.databases',
        })
        response = views.status(request)

        if PYTHON_VERSION == 2:
            content = json.loads(response.content)
            self.assertItemsEqual(expected_checks, content.keys())
        else:
            content = json.loads(response.content.decode('utf-8'))
            self.assertCountEqual(expected_checks, content.keys())

    def test_response_is_404_for_checked_and_skipped_check(self):
        # This is a bit of a weird one, basically if you explicitly include and
        # skip the same check, you should get back a 404 as they cancel each
        # other out
        request = RequestFactory().get('/', data={
            'check': 'watchman.checks.email',
            'skip': 'watchman.checks.email',
        })
        response = views.status(request)
        self.assertEqual(response.status_code, 404)

    @patch('watchman.checks._check_databases')
    def test_response_only_single_check(self, patched_check_databases):
        patched_check_databases.return_value = []
        request = RequestFactory().get('/', data={
            'check': 'watchman.checks.databases',
        })
        response = views.status(request)
        self.assertEqual(response.status_code, 200)

        if PYTHON_VERSION == 2:
            content = json.loads(response.content)
            self.assertItemsEqual({'databases': []}, content)
        else:
            content = json.loads(response.content.decode('utf-8'))
            self.assertCountEqual({'databases': []}, content)

    def test_response_404_when_none_specified(self):
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

    @override_settings(WATCHMAN_TOKEN='ABCDE')
    @override_settings(WATCHMAN_AUTH_DECORATOR='watchman.decorators.token_required')
    def test_login_not_required(self):
        # Have to manually reload settings here because override_settings
        # happens after self.setUp(), but before self.tearDown()
        reload_settings()
        request = RequestFactory().get('/', data={
            'watchman-token': 'ABCDE',
        })

        response = views.status(request)

        self.assertEqual(response.status_code, 200)

    @override_settings(WATCHMAN_AUTH_DECORATOR='django.contrib.auth.decorators.login_required')
    def test_response_when_login_required_is_redirect(self):
        # Have to manually reload settings here because override_settings
        # happens after self.setUp()
        reload_settings()
        request = RequestFactory().get('/')
        request.user = AnonymousUser()

        response = views.status(request)

        self.assertEqual(response.status_code, 302)

    @override_settings(WATCHMAN_AUTH_DECORATOR='django.contrib.auth.decorators.login_required')
    def test_response_when_login_required(self):
        # Have to manually reload settings here because override_settings
        # happens after self.setUp()
        reload_settings()
        request = RequestFactory().get('/')
        request.user = AnonymousUser()
        # Fake logging the user in
        request.user.is_authenticated = lambda: True

        response = views.status(request)
        self.assertEqual(response.status_code, 200)

    def test_response_version_header(self):
        request = RequestFactory().get('/')
        response = views.status(request)
        self.assertTrue(response.has_header('X-Watchman-Version'))

    @patch('watchman.checks._check_databases')
    @override_settings(WATCHMAN_ERROR_CODE=503)
    def test_custom_error_code(self, patched_check_databases):
        reload_settings()
        # Fake a DB error, ensure we get our error code
        patched_check_databases.return_value = [{
            "foo": {
                "ok": False,
                "error": "Fake DB Error",
                "stacktrace": "Fake DB Stack Trace",
            },
        }]
        request = RequestFactory().get('/', data={
            'check': 'watchman.checks.databases',
        })
        response = views.status(request)
        self.assertEqual(response.status_code, 503)

    @patch('watchman.checks._check_databases')
    def test_default_error_code(self, patched_check_databases):
        reload_settings()
        # Fake a DB error, ensure we get our error code
        patched_check_databases.return_value = [{
            "foo": {
                "ok": False,
                "error": "Fake DB Error",
                "stacktrace": "Fake DB Stack Trace",
            },
        }]
        request = RequestFactory().get('/', data={
            'check': 'watchman.checks.databases',
        })
        response = views.status(request)
        self.assertEqual(response.status_code, 500)

    def tearDown(self):
        pass


class TestWatchmanDashboard(unittest.TestCase):
    def setUp(self):
        # Ensure that every test executes with separate settings
        reload_settings()

    def test_dashboard_response_code(self):
        request = RequestFactory().get('/')
        response = views.dashboard(request)
        self.assertEqual(response.status_code, 200)

    def test_response_version_header(self):
        request = RequestFactory().get('/')
        response = views.dashboard(request)
        self.assertTrue(response.has_header('X-Watchman-Version'))
