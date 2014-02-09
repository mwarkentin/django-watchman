=============================
django-watchman
=============================

.. image:: https://img.shields.io/pypi/v/django-watchman.svg
    :target: http://badge.fury.io/py/django-watchman

.. image:: https://img.shields.io/travis/mwarkentin/django-watchman/master.svg
    :target: https://travis-ci.org/mwarkentin/django-watchman

.. image:: http://img.shields.io/coveralls/mwarkentin/django-watchman.svg
    :target: https://coveralls.io/r/mwarkentin/django-watchman?branch=master

django-watchman exposes a status endpoint for your backing services like
databases, caches, etc.

Documentation
-------------

The full documentation is at http://django-watchman.rtfd.org.

Quickstart
----------

1. Install django-watchman::

    pip install django-watchman

2. Add "watchman" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'watchman',
    )

3. Include the watchman URLconf in your project urls.py like this::

    url(r'^watchman/', include('watchman.urls')),

4. Start the development server and visit http://127.0.0.1:8000/watchman/ to
   get a JSON response of your backing service statuses

Features
--------

* TODO
