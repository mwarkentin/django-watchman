from __future__ import absolute_import

import json

from django.core.management.base import BaseCommand, CommandError

from watchman.utils import get_checks


class Command(BaseCommand):
    help = 'Runs the default django-watchman checks'

    def handle(self, *args, **options):
        verbosity = options['verbosity']
        print_all_checks = verbosity == '2' or verbosity == '3'

        for check in get_checks():
            if callable(check):
                resp = json.dumps(check())
                if '"ok": false' in resp:
                    raise CommandError(resp)
                elif print_all_checks:
                    print resp
