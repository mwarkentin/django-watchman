"""
test_django-watchman
------------

Tests for `django-watchman` system checks module.
"""

from django.core import checks
from django.test import SimpleTestCase, override_settings

from watchman.system_checks import check_endpoint_authentication


def _ids(messages):
    return [message.id for message in messages]


class TestEndpointAuthenticationCheck(SimpleTestCase):
    def test_warns_when_no_tokens_with_default_decorator(self):
        self.assertEqual(_ids(check_endpoint_authentication()), ["watchman.W001"])

    @override_settings(WATCHMAN_TOKENS="")
    def test_warns_when_tokens_empty(self):
        self.assertEqual(_ids(check_endpoint_authentication()), ["watchman.W001"])

    @override_settings(WATCHMAN_TOKENS="ABCDE")
    def test_no_warning_when_tokens_set(self):
        self.assertEqual(check_endpoint_authentication(), [])

    @override_settings(
        WATCHMAN_AUTH_DECORATOR="django.contrib.auth.decorators.login_required"
    )
    def test_no_warning_with_custom_decorator(self):
        self.assertEqual(check_endpoint_authentication(), [])

    @override_settings(WATCHMAN_AUTH_DECORATOR=None)
    def test_no_warning_when_auth_explicitly_disabled(self):
        self.assertEqual(check_endpoint_authentication(), [])

    def test_only_runs_as_deployment_check(self):
        self.assertNotIn("watchman.W001", _ids(checks.run_checks()))
        self.assertIn(
            "watchman.W001", _ids(checks.run_checks(include_deployment_checks=True))
        )
