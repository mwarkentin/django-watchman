from __future__ import absolute_import

import json
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from watchman.utils import get_checks


def _add_options(target):
    return (
        target(
            '-c',
            '--checks',
            dest='checks',
            help='A comma-separated list of watchman checks to run (full python dotted paths)'
        ),
        target(
            '-s',
            '--skips',
            dest='skips',
            help='A comma-separated list of watchman checks to skip (full python dotted paths)'
        )
    )


class Command(BaseCommand):
    help = 'Runs the default django-watchman checks'

    if hasattr(BaseCommand, 'option_list'):
        # Django < 1.10
        option_list = BaseCommand.option_list + _add_options(make_option)
    else:
        # Django >= 1.10
        def add_arguments(self, parser):
            _add_options(parser.add_argument)

    def handle(self, *args, **options):
        check_list = None
        skip_list = None

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
                # Cast to int for Django < 1.8 (used to be a string value)
                elif int(options['verbosity']) >= 2:
                    self.stdout.write(resp)
