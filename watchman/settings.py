from django.conf import settings

# TODO: these should not be module level.
WATCHMAN_ENABLE_PAID_CHECKS = getattr(settings, 'WATCHMAN_ENABLE_PAID_CHECKS', False)
WATCHMAN_AUTH_DECORATOR = getattr(settings, 'WATCHMAN_AUTH_DECORATOR', 'watchman.decorators.token_required')
WATCHMAN_TOKEN = getattr(settings, 'WATCHMAN_TOKEN', None)
WATCHMAN_TOKEN_NAME = getattr(settings, 'WATCHMAN_TOKEN_NAME', 'watchman-token')
WATCHMAN_ERROR_CODE = getattr(settings, 'WATCHMAN_ERROR_CODE', 200)

DEFAULT_CHECKS = (
    'watchman.checks.caches',
    'watchman.checks.databases',
    'watchman.checks.storage',
)
PAID_CHECKS = (
    'watchman.checks.email',
)

if WATCHMAN_ENABLE_PAID_CHECKS:
    DEFAULT_CHECKS = DEFAULT_CHECKS + PAID_CHECKS

WATCHMAN_CHECKS = getattr(settings, 'WATCHMAN_CHECKS', DEFAULT_CHECKS)
