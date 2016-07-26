import sys
import traceback


try:
    from django.conf import settings

    from pymysql import install_as_MySQLdb

    install_as_MySQLdb()

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
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
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
        NOSE_ARGS=['-s'],
    )

    from django_nose import NoseTestSuiteRunner
except ImportError:
    traceback.print_exc()
    raise RuntimeError("To fix this error, run: pip install django -r requirements-test.txt")


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    test_runner = NoseTestSuiteRunner(verbosity=1)

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(failures)


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
