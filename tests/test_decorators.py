#!/usr/bin/env python
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

from watchman import settings as watchman_settings


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

    def tearDown(self):
        watchman_settings.WATCHMAN_TOKEN = None
