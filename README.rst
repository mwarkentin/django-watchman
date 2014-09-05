=============================
django-watchman
=============================

.. image:: http://img.shields.io/pypi/v/django-watchman.svg
    :target: http://badge.fury.io/py/django-watchman

.. image:: http://img.shields.io/travis/mwarkentin/django-watchman/master.svg
    :target: https://travis-ci.org/mwarkentin/django-watchman

.. image:: http://img.shields.io/coveralls/mwarkentin/django-watchman.svg
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

Custom checks
*************

django-watchman allows you to customize the checks which are run by modifying
the ``WATCHMAN_CHECKS`` setting. In ``settings.py``::

    WATCHMAN_CHECKS = (
        'module.path.to.callable',
        'another.module.path.to.callable',
    )

Checks now have the same contract as context processors: they consume a
``request`` and return a ``dict`` whose keys are applied to the JSON response::

    def my_check(request):
        return {'x': 1}

In the absence of any checks, a 404 is thrown, which is then handled by the
``json_view`` decorator.

Run a subset of available checks
********************************

A subset of checks may be run, by passing ``?check=module.path.to.callable&check=...``
in the request URL. Only the callables given in querystring, which are in the
``WATCHMAN_CHECKS`` should be run, eg::

    curl -XGET http://127.0.0.1:8080/watchman/?check=watchman.views.caches_status

Default checks
--------------

By default, django-watchman will run checks against your databases
(``watchman.views.databases_status``) and caches (``watchman.views.caches_status``).
These will function even if you haven't configured the respective settings.
