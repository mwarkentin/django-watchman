"""Django app configuration for watchman."""

from django.apps import AppConfig


class WatchmanConfig(AppConfig):
    name = "watchman"

    def ready(self) -> None:
        from django.core import checks

        from watchman.system_checks import check_endpoint_authentication

        checks.register(
            check_endpoint_authentication, checks.Tags.security, deploy=True
        )
