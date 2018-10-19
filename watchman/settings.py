from django.conf import settings
from watchman.constants import DEFAULT_CHECKS, PAID_CHECKS

# TODO: these should not be module level (https://github.com/mwarkentin/django-watchman/issues/13)
WATCHMAN_ENABLE_PAID_CHECKS = getattr(settings, 'WATCHMAN_ENABLE_PAID_CHECKS', False)
WATCHMAN_AUTH_DECORATOR = getattr(settings, 'WATCHMAN_AUTH_DECORATOR', 'watchman.decorators.token_required')
# TODO: Remove for django-watchman 1.0
WATCHMAN_TOKEN = getattr(settings, 'WATCHMAN_TOKEN', None)
WATCHMAN_TOKENS = getattr(settings, 'WATCHMAN_TOKENS', None)
WATCHMAN_TOKEN_NAME = getattr(settings, 'WATCHMAN_TOKEN_NAME', 'watchman-token')
WATCHMAN_ERROR_CODE = getattr(settings, 'WATCHMAN_ERROR_CODE', 500)
WATCHMAN_EMAIL_SENDER = getattr(settings, 'WATCHMAN_EMAIL_SENDER', 'watchman@example.com')
WATCHMAN_EMAIL_RECIPIENTS = getattr(settings, 'WATCHMAN_EMAIL_RECIPIENTS', ['to@example.com'])
WATCHMAN_EMAIL_HEADERS = getattr(settings, 'WATCHMAN_EMAIL_HEADERS', {})

WATCHMAN_CACHES = getattr(settings, 'WATCHMAN_CACHES', settings.CACHES)
WATCHMAN_DATABASES = getattr(settings, 'WATCHMAN_DATABASES', settings.DATABASES)

WATCHMAN_DISABLE_APM = getattr(settings, 'WATCHMAN_DISABLE_APM', False)

if WATCHMAN_ENABLE_PAID_CHECKS:
    DEFAULT_CHECKS = DEFAULT_CHECKS + PAID_CHECKS

WATCHMAN_CHECKS = getattr(settings, 'WATCHMAN_CHECKS', DEFAULT_CHECKS)

EXPOSE_WATCHMAN_VERSION = getattr(settings, 'EXPOSE_WATCHMAN_VERSION', False)
