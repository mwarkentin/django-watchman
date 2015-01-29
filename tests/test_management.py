# -*- coding: utf-8 -*-

"""
test_django-watchman
------------

Tests for `django-watchman` management commands.
"""

from __future__ import unicode_literals

import unittest

from django.core.management import call_command
from django.utils.six import StringIO


class TestWatchman(unittest.TestCase):

    def test_successful_management_command_outputs_nothing(self):
        out = StringIO()
        call_command('watchman', stdout=out)
        self.assertEquals('', out.getvalue())

    def test_successful_management_command_outputs_check_status_with_verbosity_2(self):
        out = StringIO()
        call_command('watchman', stdout=out, verbosity='2')
        self.assertIn('caches', out.getvalue())

    def test_successful_management_command_outputs_check_status_with_verbosity_3(self):
        out = StringIO()
        call_command('watchman', stdout=out, verbosity='3')
        self.assertIn('caches', out.getvalue())

    def test_successful_management_command_supports_check_list(self):
        out = StringIO()
        call_command('watchman', stdout=out, checks='watchman.checks.caches', verbosity='3')
        self.assertIn('caches', out.getvalue())
        self.assertNotIn('databases', out.getvalue())

    def test_successful_management_command_supports_skip_list(self):
        out = StringIO()
        call_command('watchman', stdout=out, skips='watchman.checks.email', verbosity='3')
        self.assertIn('caches', out.getvalue())
        self.assertIn('databases', out.getvalue())
        self.assertNotIn('email', out.getvalue())
