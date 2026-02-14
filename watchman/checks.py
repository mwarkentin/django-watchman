import uuid
from pathlib import PurePath
from typing import Any

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
from django.db import connections

from watchman import settings as watchman_settings
from watchman import utils
from watchman.decorators import check
from watchman.types import CheckResult, CheckStatus


def _check_caches(caches: dict[str, Any]) -> list[CheckResult]:
    return [_check_cache(cache) for cache in sorted(caches)]


@check
def _check_cache(cache_name: str) -> dict[str, CheckStatus]:
    key = f"django-watchman-{uuid.uuid4()}"
    value = f"django-watchman-{uuid.uuid4()}"

    cache = utils.get_cache(cache_name)

    cache.set(key, value)
    cache.get(key)
    cache.delete(key)
    return {cache_name: {"ok": True}}


def _check_databases(databases: dict[str, Any]) -> list[CheckResult]:
    return [_check_database(database) for database in sorted(databases)]


@check
def _check_database(database: str) -> dict[str, CheckStatus]:
    connection = connections[database]
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    return {database: {"ok": True}}


@check
def _check_email() -> CheckStatus:
    headers = {"X-DJANGO-WATCHMAN": "true"}
    headers.update(watchman_settings.WATCHMAN_EMAIL_HEADERS)
    email = EmailMessage(
        "django-watchman email check",
        "This is an automated test of the email system.",
        watchman_settings.WATCHMAN_EMAIL_SENDER,
        watchman_settings.WATCHMAN_EMAIL_RECIPIENTS,
        headers=headers,
    )
    email.send()
    return {"ok": True}


@check
def _check_storage() -> CheckStatus:
    # Use relative path within storage - Django handles the base location
    storage_subdir = watchman_settings.WATCHMAN_STORAGE_PATH
    # Convert absolute paths to empty string (use storage root)
    if storage_subdir and PurePath(storage_subdir).is_absolute():
        storage_subdir = ""
    filename = f"django-watchman-{uuid.uuid4()}.txt"
    if storage_subdir:
        filename = str(PurePath(storage_subdir) / filename)
    content = b"django-watchman test file"
    path = default_storage.save(filename, ContentFile(content))
    default_storage.size(path)
    default_storage.open(path).read()
    default_storage.delete(path)
    return {"ok": True}


def caches() -> dict[str, list[CheckResult]]:
    return {"caches": _check_caches(watchman_settings.WATCHMAN_CACHES)}


def databases() -> dict[str, list[CheckResult]]:
    return {"databases": _check_databases(watchman_settings.WATCHMAN_DATABASES)}


def email() -> dict[str, CheckResult]:
    return {"email": _check_email()}


def storage() -> dict[str, CheckResult]:
    return {"storage": _check_storage()}
