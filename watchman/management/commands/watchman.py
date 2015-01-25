from __future__ import absolute_import

import json
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from watchman.utils import get_checks


class Command(BaseCommand):
    help = 'Runs the default django-watchman checks'

    option_list = BaseCommand.option_list + (
        make_option(
            '-c',
            '--checks',
            dest='checks',
            help='A comma-separated list of watchman checks to run (full python dotted paths)'
        ),
        make_option(
            '-s',
            '--skips',
            dest='skips',
            help='A comma-separated list of watchman checks to skip (full python dotted paths)'
        ),
    )

    def handle(self, *args, **options):
        check_list = None
        skip_list = None
        verbosity = options['verbosity']
        print_all_checks = verbosity == '2' or verbosity == '3'

        checks = options['checks']
        skips = options['skips']

        if checks is not None:
            check_list = checks.split(',')

        if skips is not None:
            skip_list = skips.split(',')

        for check in get_checks(check_list=check_list, skip_list=skip_list):
            if callable(check):
                resp = json.dumps(check())
                if '"ok": false' in resp:
                    raise CommandError(resp)
                elif print_all_checks:
                    self.stdout.write(resp)
