from django.conf import settings


WATCHMAN_TOKEN = getattr(settings, 'WATCHMAN_TOKEN', None)
WATCHMAN_TOKEN_NAME = getattr(settings, 'WATCHMAN_TOKEN_NAME', 'watchman-token')
