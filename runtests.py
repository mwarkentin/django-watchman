#!/usr/bin/env python
import sys

import django
from django.conf import settings

settings.configure(
    DEBUG=True,
    USE_TZ=True,
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
        },
    },
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "APP_DIRS": True,
        },
    ],
    ROOT_URLCONF="watchman.urls",
    INSTALLED_APPS=[
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sites",
        "watchman",
    ],
    SITE_ID=1,
    SECRET_KEY="test-secret-key",
    DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
)

django.setup()


def run_tests():
    import pytest

    sys.exit(pytest.main(["tests", "-v"]))


if __name__ == "__main__":
    run_tests()
