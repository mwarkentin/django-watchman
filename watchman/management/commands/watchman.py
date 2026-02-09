import json
from argparse import ArgumentParser
from typing import Any

from django.core.management.base import BaseCommand, CommandError

from watchman.utils import get_checks


class Command(BaseCommand):
    help = "Runs the default django-watchman checks"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "-c",
            "--checks",
            dest="checks",
            help="A comma-separated list of watchman checks to run (full python dotted paths)",
        )
        parser.add_argument(
            "-s",
            "--skips",
            dest="skips",
            help="A comma-separated list of watchman checks to skip (full python dotted paths)",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        check_list: list[str] | None = None
        skip_list: list[str] | None = None

        checks: str | None = options["checks"]
        skips: str | None = options["skips"]

        if checks is not None:
            check_list = checks.split(",")

        if skips is not None:
            skip_list = skips.split(",")

        for check in get_checks(check_list=check_list, skip_list=skip_list):
            if callable(check):
                resp = json.dumps(check())
                if '"ok": false' in resp:
                    raise CommandError(resp)
                elif int(options["verbosity"]) >= 2:
                    self.stdout.write(resp)
