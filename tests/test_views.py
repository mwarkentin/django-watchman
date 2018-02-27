# -*- coding: utf-8 -*-

"""
test_django-watchman
------------

Tests for `django-watchman` views module.
"""

from __future__ import unicode_literals

import json
from _threading_local import local
from copy import copy

from django.db import connections
from django.db.utils import DEFAULT_DB_ALIAS
from django.test.testcases import TransactionTestCase


try:
    from importlib import reload
except ImportError:  # Python < 3
    pass
import sys
import unittest

import django
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core import mail
from django.test import TestCase as DjangoTestCase
from django.test.client import RequestFactory, Client
from django.test.utils import override_settings

from mock import patch

from watchman import checks, views

PYTHON_VERSION = sys.version_info[0]


class AuthenticatedUser(AnonymousUser):
    @property
    def is_authenticated(self):
        class CallableTrue(object):
            def __call__(self, *args, **kwargs):
                return True

            def __bool__(self):
                return True

            __nonzero__ = __bool__

        return CallableTrue()


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
        if django.VERSION < (1, 7):
            expected_error = "Could not find backend 'foo': Could not find backend 'foo': foo doesn't look like a module path"
        else:
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
    def test_login_not_required_with_get_param(self):
        # Have to manually reload settings here because override_settings
        # happens after self.setUp(), but before self.tearDown()
        reload_settings()
        request = RequestFactory().get('/', data={
            'watchman-token': 'ABCDE',
        })

        response = views.status(request)

        self.assertEqual(response.status_code, 200)

    @override_settings(WATCHMAN_TOKEN='ABCDE')
    def test_version_header_not_included_when_token_auth_fails(self):
        # Have to manually reload settings here because override_settings
        # happens after self.setUp(), but before self.tearDown()
        reload_settings()
        request = RequestFactory().get('/')

        response = views.status(request)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(response.has_header('X-Watchman-Version'))

    @override_settings(WATCHMAN_TOKEN='ABCDE')
    @override_settings(WATCHMAN_AUTH_DECORATOR='watchman.decorators.token_required')
    def test_login_not_required_with_authorization_header(self):
        # Have to manually reload settings here because override_settings
        # happens after self.setUp(), but before self.tearDown()
        reload_settings()
        request = RequestFactory().get('/', HTTP_AUTHORIZATION='WATCHMAN-TOKEN Token="ABCDE"')
        response = views.status(request)
        self.assertEqual(response.status_code, 200)

    @override_settings(WATCHMAN_TOKEN='123-456-ABCD')
    @override_settings(WATCHMAN_AUTH_DECORATOR='watchman.decorators.token_required')
    def test_login_not_required_with_authorization_header_dashes_in_token(self):
        # Have to manually reload settings here because override_settings
        # happens after self.setUp(), but before self.tearDown()
        reload_settings()
        request = RequestFactory().get('/', HTTP_AUTHORIZATION='WATCHMAN-TOKEN Token="123-456-ABCD"')
        response = views.status(request)
        self.assertEqual(response.status_code, 200)

    @override_settings(WATCHMAN_TOKEN='ABCDE')
    @override_settings(WATCHMAN_AUTH_DECORATOR='watchman.decorators.token_required')
    def test_login_fails_with_invalid_get_param(self):
        # Have to manually reload settings here because override_settings
        # happens after self.setUp(), but before self.tearDown()
        reload_settings()
        request = RequestFactory().get('/', data={
            'watchman-token': '12345',
        })

        response = views.status(request)

        self.assertEqual(response.status_code, 403)

    @override_settings(WATCHMAN_TOKEN='ABCDE')
    @override_settings(WATCHMAN_AUTH_DECORATOR='watchman.decorators.token_required')
    def test_login_fails_with_invalid_authorization_header(self):
        # Have to manually reload settings here because override_settings
        # happens after self.setUp(), but before self.tearDown()
        reload_settings()
        request = RequestFactory().get('/', HTTP_AUTHORIZATION='WATCHMAN-TOKEN Token="12345"')
        response = views.status(request)
        self.assertEqual(response.status_code, 403)

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
        request.user = AuthenticatedUser()

        response = views.status(request)
        self.assertEqual(response.status_code, 200)

    def test_response_version_header_missing_by_default(self):
        request = RequestFactory().get('/')
        response = views.status(request)
        self.assertFalse(response.has_header('X-Watchman-Version'))

    @override_settings(EXPOSE_WATCHMAN_VERSION=True)
    def test_response_version_header(self):
        # Have to manually reload settings here because override_settings
        # happens after self.setUp()
        reload_settings()
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


class TestDBError(TransactionTestCase):
    """
    Ensure that we produce a valid response even in case of database
    connection issues with `ATOMIC_REQUESTS` enabled.

    Since overriding `DATABASES` isn't officially supported we need to perform
    some gymnastics here to convince django.
    """
    def setUp(self):
        # Cache current database connections
        self.databases = copy(connections._databases)
        self.connection = getattr(connections._connections, DEFAULT_DB_ALIAS, None)
        del connections.__dict__['databases']  # remove cached_property value
        connections._databases = None
        connections._connections = local()

    def tearDown(self):
        # Restore previous database connections
        connections._databases = self.databases
        setattr(connections._connections, DEFAULT_DB_ALIAS, self.connection)
        del connections.__dict__['databases']  # remove cached_property value

    @override_settings(
        DATABASES={
            'default': {
                "ENGINE": "django.db.backends.mysql",
                "HOST": "no.host.by.this.name.some-tld-that-doesnt-exist",
                "ATOMIC_REQUESTS": True
            },
        }
    )
    # can't use override_settings because of
    # https://github.com/mwarkentin/django-watchman/issues/13
    @patch('watchman.settings.WATCHMAN_ERROR_CODE', 201)
    def test_db_error_w_atomic_requests(self):
        # Ensure we don't trigger django's generic 500 page in case of DB error
        response = Client().get('/', data={
            'check': 'watchman.checks.databases',
        })
        self.assertEqual(response.status_code, 201)


class TestWatchmanDashboard(unittest.TestCase):
    def setUp(self):
        # Ensure that every test executes with separate settings
        reload_settings()

    def test_dashboard_response_code(self):
        request = RequestFactory().get('/')
        response = views.dashboard(request)
        self.assertEqual(response.status_code, 200)

    def test_response_version_header_and_html_missing_by_default(self):
        request = RequestFactory().get('/')
        response = views.dashboard(request)
        self.assertFalse(response.has_header('X-Watchman-Version'))
        self.assertNotIn('Watchman version:', response.content.decode())

    @override_settings(EXPOSE_WATCHMAN_VERSION=True)
    def test_response_has_version_header_and_html(self):
        # Have to manually reload settings here because override_settings
        # happens after self.setUp()
        reload_settings()
        request = RequestFactory().get('/')
        response = views.dashboard(request)
        self.assertTrue(response.has_header('X-Watchman-Version'))
        self.assertIn('Watchman version:', response.content.decode())


class TestPing(unittest.TestCase):
    def setUp(self):
        # Ensure that every test executes with separate settings
        reload_settings()

    def test_returns_pong(self):
        request = RequestFactory().get('/')
        response = views.ping(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'pong')
        self.assertEqual(response['Content-Type'], 'text/plain')


class TestBareStatus(unittest.TestCase):
    def setUp(self):
        # Ensure that every test executes with separate settings
        reload_settings()

    def test_bare_status_success(self):
        request = RequestFactory().get('/')
        response = views.bare_status(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), '')

    @patch('watchman.checks._check_databases')
    @override_settings(WATCHMAN_ERROR_CODE=503)
    def test_bare_status_error(self, patched_check_databases):
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
        response = views.bare_status(request)
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.content.decode(), '')

    @patch('watchman.checks._check_databases')
    def test_bare_status_default_error(self, patched_check_databases):
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
        response = views.bare_status(request)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.content.decode(), '')


class TestEmailCheck(DjangoTestCase):
    def setUp(self):
        # Ensure that every test executes with separate settings
        reload_settings()

    def def_test_email_with_default_recipient(self):
        checks._check_email()

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        sent_email = mail.outbox[0]
        expected_recipients = ['to@example.com']
        self.assertEqual(sent_email.to, expected_recipients)

    @override_settings(WATCHMAN_EMAIL_RECIPIENTS=['custom@example.com'])
    def def_test_email_with_custom_recipient(self):
        # Have to manually reload settings here because override_settings
        # happens after self.setUp()
        reload_settings()
        checks._check_email()

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        sent_email = mail.outbox[0]
        expected_recipients = ['custom@example.com']
        self.assertEqual(sent_email.to, expected_recipients)

    @override_settings(WATCHMAN_EMAIL_RECIPIENTS=['to1@example.com', 'to2@example.com'])
    def def_test_email_with_multiple_recipients(self):
        # Have to manually reload settings here because override_settings
        # happens after self.setUp()
        reload_settings()
        checks._check_email()

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        sent_email = mail.outbox[0]
        expected_recipients = ['to1@example.com', 'to2@example.com']
        self.assertEqual(sent_email.to, expected_recipients)

    def test_email_check_with_default_headers(self):
        checks._check_email()

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        sent_email = mail.outbox[0]
        expected_headers = {
            'X-DJANGO-WATCHMAN': True,
        }
        self.assertEqual(sent_email.extra_headers, expected_headers)

    @override_settings(WATCHMAN_EMAIL_HEADERS={'foo': 'bar'})
    def test_email_check_with_custom_headers(self):
        # Have to manually reload settings here because override_settings
        # happens after self.setUp()
        reload_settings()
        checks._check_email()

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        sent_email = mail.outbox[0]
        expected_headers = {
            'X-DJANGO-WATCHMAN': True,
            'foo': 'bar',
        }
        self.assertEqual(sent_email.extra_headers, expected_headers)

    def def_test_email_with_default_sender(self):
        checks._check_email()

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        sent_email = mail.outbox[0]
        expected_sender = 'watchman@example.com'
        self.assertEqual(sent_email.from_email, expected_sender)

    @override_settings(WATCHMAN_EMAIL_SENDER='custom@example.com')
    def def_test_email_with_custom_sender(self):
        # Have to manually reload settings here because override_settings
        # happens after self.setUp()
        reload_settings()
        checks._check_email()

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        sent_email = mail.outbox[0]
        expected_sender = 'custom@example.com'
        self.assertEqual(sent_email.from_email, expected_sender)
