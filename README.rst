=============================
django-watchman
=============================

.. image:: https://badge.fury.io/py/django-watchman.png
    :target: http://badge.fury.io/py/django-watchman

.. image:: https://travis-ci.org/mwarkentin/django-watchman.png?branch=master
    :target: https://travis-ci.org/mwarkentin/django-watchman

.. image:: https://coveralls.io/repos/mwarkentin/django-watchman/badge.png?branch=master
    :target: https://coveralls.io/r/mwarkentin/django-watchman?branch=master

django-watchman exposes a status endpoint for your backing services like
databases, caches, etc.

.. image:: https://s3.amazonaws.com/snaps.michaelwarkentin.com/watchmenozy.jpg

Documentation
-------------

The full documentation is at http://django-watchman.rtfd.org.

Quickstart
----------

1. Install ``django-watchman``::

    pip install django-watchman

2. Add ``watchman`` to your ``INSTALLED_APPS`` setting like this::

    INSTALLED_APPS = (
        ...
        'watchman',
    )

3. Include the watchman URLconf in your project ``urls.py`` like this::

    url(r'^watchman/', include('watchman.urls')),

4. Start the development server and visit ``http://127.0.0.1:8000/watchman/`` to
   get a JSON response of your backing service statuses::

    {
        "databases": [
            {
                "default": {
                    "ok": true
                }
            }
        ],
        "caches": [
            {
                "default": {
                    "ok": true
                }
            }
        ]
    }

Features
--------

Token based authentication
**************************

If you want to protect the status endpoint, you can add a ``WATCHMAN_TOKEN`` to
your settings. When this setting is added, you must pass that value in as the
``watchman-token`` **GET** parameter::

    GET http://127.0.0.1:8000/watchman/?watchman-token=:token

If you want to change the token name, you can set the ``WATCHMAN_TOKEN_NAME``.
The value of this setting will be the **GET** parameter that you must pass in::

    WATCHMAN_TOKEN_NAME = 'custom-token-name'

    GET http://127.0.0.1:8000/watchman/?custom-token-name=:token
