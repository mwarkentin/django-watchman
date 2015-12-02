# -*- coding: utf-8 -*-

"""
test_django-watchman
------------

Tests for `django-watchman` decorators module.
"""

from __future__ import unicode_literals

import unittest

from django.core.urlresolvers import reverse
from django.test.client import Client

import mock

from watchman import settings as watchman_settings
from watchman.decorators import benchmark, check


class FakeException(Exception):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)


class TestWatchman(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        watchman_settings.WATCHMAN_TOKEN = 'foo'

    def test_200_ok_if_no_token_set(self):
        watchman_settings.WATCHMAN_TOKEN = None
        response = self.client.get(reverse('watchman.views.status'))
        self.assertEqual(response.status_code, 200)
        watchman_settings.WATCHMAN_TOKEN = 'foo'

    def test_200_ok_if_tokens_match(self):
        data = {
            'watchman-token': 'foo',
        }
        response = self.client.get(reverse('watchman.views.status'), data)
        self.assertEqual(response.status_code, 200)

    def test_required_token_param_can_be_renamed(self):
        watchman_settings.WATCHMAN_TOKEN_NAME = 'custom-token'
        data = {
            'custom-token': 'foo',
        }
        response = self.client.get(reverse('watchman.views.status'), data)
        self.assertEqual(response.status_code, 200)
        watchman_settings.WATCHMAN_TOKEN_NAME = 'watchman-token'

    def test_403_raised_if_missing_token(self):
        response = self.client.get(reverse('watchman.views.status'))
        self.assertEqual(response.status_code, 403)

    def test_403_raised_if_invalid_token(self):
        data = {
            'watchman-token': 'bar',
        }
        response = self.client.get(reverse('watchman.views.status'), data)
        self.assertEqual(response.status_code, 403)

    # We cannot easily mock a stacktrace, since:
    #
    #   1. it is not a property of the exception,
    #   2. file paths will change between systems
    #
    # Instead, assert all other response parameters are correct.
    def test_exception_caught_if_no_arguments(self):
        keys = ['ok', 'error', 'stacktrace']
        func = mock.Mock(side_effect=FakeException('example error'))
        decorated_func = check(func)
        response = decorated_func()
        self.assertIsInstance(response, dict)
        for key in keys:
            self.assertIn(key, response)
        self.assertEqual(response['ok'], False)
        self.assertEqual(response['error'], 'example error')
        self.assertIsInstance(response['stacktrace'], str)

    def test_exception_caught_with_argument(self):
        keys = ['ok', 'error', 'stacktrace']
        func = mock.Mock(side_effect=FakeException('example error'))
        decorated_func = check(func)
        response = decorated_func('default')
        self.assertIsInstance(response, dict)
        for key in keys:
            self.assertIn(key, response['default'])
        self.assertEqual(response['default']['ok'], False)
        self.assertEqual(response['default']['error'], 'example error')
        self.assertIsInstance(response['default']['stacktrace'], str)

    def test_benchmark_decorator_for_dict_response(self):
        func = mock.Mock(return_value={'ok': True})
        decorated_func = benchmark(func)
        response = decorated_func()
        self.assertIn('time', response)

    def tearDown(self):
        watchman_settings.WATCHMAN_TOKEN = None
