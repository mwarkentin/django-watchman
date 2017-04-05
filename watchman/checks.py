# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import uuid
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
from django.db import connections

import pika

from watchman.decorators import check
from watchman import settings as watchman_settings
from watchman import utils


def _check_caches(caches):
    return [_check_cache(cache) for cache in sorted(caches)]


@check
def _check_cache(cache_name):
    key = 'django-watchman-{}'.format(uuid.uuid4())
    value = 'django-watchman-{}'.format(uuid.uuid4())

    cache = utils.get_cache(cache_name)

    cache.set(key, value)
    cache.get(key)
    cache.delete(key)
    return {cache_name: {"ok": True}}


def _check_databases(databases):
    return [_check_database(database) for database in sorted(databases)]


def _check_amqp_connections(connection_urls):
    return [_check_amqp_connection(connection_url) for connection_url in sorted(connection_urls)]


@check
def _check_database(database):
    connections[database].introspection.table_names()
    return {database: {"ok": True}}


@check
def _check_email():
    headers = {"X-DJANGO-WATCHMAN": True}
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
def _check_storage():
    filename = 'django-watchman-{}.txt'.format(uuid.uuid4())
    content = 'django-watchman test file'
    path = default_storage.save(filename, ContentFile(content))
    default_storage.size(path)
    default_storage.open(path).read()
    default_storage.delete(path)
    return {"ok": True}


@check
def _check_amqp_connection(connection_url):
    conn_params = pika.URLParameters(connection_url)
    connection = pika.BlockingConnection(conn_params)
    connection.close()
    return {'ok': True}
    
    
def caches():
    return {"caches": _check_caches(settings.CACHES)}


def databases():
    return {"databases": _check_databases(settings.DATABASES)}


def email():
    return {"email": _check_email()}


def storage():
    return {"storage": _check_storage()}


def amqp():
    return {'amqp': _check_ampq(settings.AMQP_CONNECTIONS)}
