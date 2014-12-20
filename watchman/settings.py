from django.conf import settings

# TODO: these should not be module level.
WATCHMAN_TOKEN = getattr(settings, 'WATCHMAN_TOKEN', None)
WATCHMAN_TOKEN_NAME = getattr(settings, 'WATCHMAN_TOKEN_NAME', 'watchman-token')
DEFAULT_CHECKS = (
    'watchman.checks.caches_status',
    'watchman.checks.databases_status',
    'watchman.checks.email_status',
    'watchman.checks.storage_status',
)

WATCHMAN_CHECKS = getattr(settings, 'WATCHMAN_CHECKS', DEFAULT_CHECKS)
