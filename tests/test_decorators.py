"""
test_django-watchman
------------

Tests for `django-watchman` decorators module.
"""

import logging
import unittest
from unittest import mock
from unittest.mock import MagicMock, patch

from django.test.client import Client
from django.urls import reverse

from watchman import settings as watchman_settings
from watchman.decorators import check


class FakeException(Exception):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)


class TestDBConnection(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    @patch("watchman.checks.connections")
    def test_cursor_is_called(self, mock_connections):
        cursor_mock = MagicMock()
        mock_connections["default"].cursor().__enter__.return_value = cursor_mock
        data = {
            "watchman-token": "t1",
        }
        self.client.get(reverse("status"), data)
        cursor_mock.execute.assert_called_once_with("SELECT 1")


class TestWatchmanMultiTokens(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        watchman_settings.WATCHMAN_TOKEN = None
        watchman_settings.WATCHMAN_TOKENS = "t1,t2"

    def test_200_ok_if_matching_first_token_in_list(self):
        data = {
            "watchman-token": "t1",
        }
        response = self.client.get(reverse("status"), data)
        self.assertEqual(response.status_code, 200)

    def test_200_ok_if_matching_second_token_in_list(self):
        data = {
            "watchman-token": "t2",
        }
        response = self.client.get(reverse("status"), data)
        self.assertEqual(response.status_code, 200)

    def test_403_raised_if_missing_token(self):
        response = self.client.get(reverse("status"))
        self.assertEqual(response.status_code, 403)

    def test_403_raised_if_invalid_token(self):
        data = {
            "watchman-token": "bar",
        }
        response = self.client.get(reverse("status"), data)
        self.assertEqual(response.status_code, 403)


class TestWatchmanNoTokens(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        watchman_settings.WATCHMAN_TOKEN = None
        watchman_settings.WATCHMAN_TOKENS = None

    def test_200_ok_if_no_token_set(self):
        response = self.client.get(reverse("status"))
        self.assertEqual(response.status_code, 200)

    def test_200_ok_if_no_token_set_but_passed_in(self):
        data = {
            "watchman-token": "foo",
        }
        response = self.client.get(reverse("status"), data)
        self.assertEqual(response.status_code, 200)


class TestWatchmanSingleToken(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.logger = logging.getLogger("watchman")
        watchman_settings.WATCHMAN_TOKEN = "foo"
        watchman_settings.WATCHMAN_TOKENS = None

    def test_200_ok_if_tokens_match(self):
        data = {
            "watchman-token": "foo",
        }
        response = self.client.get(reverse("status"), data)
        self.assertEqual(response.status_code, 200)

    def test_required_token_param_can_be_renamed(self):
        watchman_settings.WATCHMAN_TOKEN_NAME = "custom-token"
        data = {
            "custom-token": "foo",
        }
        response = self.client.get(reverse("status"), data)
        self.assertEqual(response.status_code, 200)
        watchman_settings.WATCHMAN_TOKEN_NAME = "watchman-token"

    def test_403_raised_if_missing_token(self):
        response = self.client.get(reverse("status"))
        self.assertEqual(response.status_code, 403)

    def test_403_raised_if_invalid_token(self):
        data = {
            "watchman-token": "bar",
        }
        response = self.client.get(reverse("status"), data)
        self.assertEqual(response.status_code, 403)

    # We cannot easily mock a stacktrace, since:
    #
    #   1. it is not a property of the exception,
    #   2. file paths will change between systems
    #
    # Instead, assert all other response parameters are correct.
    def test_exception_caught_if_no_arguments(self):
        def test_func():
            raise FakeException("test error")

        with (
            mock.patch.object(self.logger, "exception") as mock_exception,
            mock.patch.object(self.logger, "debug") as mock_debug,
        ):
            decorated_func = check(test_func)
            keys = ["ok", "error", "stacktrace"]
            response = decorated_func()
            self.assertIsInstance(response, dict)
            for key in keys:
                self.assertIn(key, response)
            self.assertEqual(response["ok"], False)
            self.assertEqual(response["error"], "test error")
            self.assertIsInstance(response["stacktrace"], str)
            mock_debug.assert_called_once_with("Checking '%s'", "test_func")
            mock_exception.assert_called_once_with(
                "Error calling '%s': %s", "test_func", "test error"
            )

    def test_exception_caught_with_argument(self):
        def test_func(arg):
            raise FakeException("test error")

        with (
            mock.patch.object(self.logger, "exception") as mock_exception,
            mock.patch.object(self.logger, "debug") as mock_debug,
        ):
            decorated_func = check(test_func)
            keys = ["ok", "error", "stacktrace"]
            response = decorated_func("default")
            self.assertIsInstance(response, dict)
            for key in keys:
                self.assertIn(key, response["default"])
            self.assertEqual(response["default"]["ok"], False)
            self.assertEqual(response["default"]["error"], "test error")
            self.assertIsInstance(response["default"]["stacktrace"], str)
            mock_debug.assert_called_once_with(
                "Checking '%s' for '%s'", "test_func", "default"
            )
            mock_exception.assert_called_once_with(
                "Error calling '%s' for '%s': %s",
                "test_func",
                "default",
                "test error",
            )

    def tearDown(self):
        watchman_settings.WATCHMAN_TOKEN = None
