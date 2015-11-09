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

Testimonials
------------

    We're in love with django-watchman. External monitoring is a vital part of our service offering. Using django-watchman we can introspect the infrastructure of an application via a secure URL. It's very well written and easy to extend. We've recommended it to many of our clients already.

— Hany Fahim, CEO, `VM Farms <https://vmfarms.com/>`_.

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
        ],
        "storage": {"ok": true}
    }

Features
--------

Human-friendly dashboard
************************

Visit ``http://127.0.0.1:8000/watchman/dashboard/`` to get a human-friendly HTML
representation of all of your watchman checks.

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

Custom authentication/authorization
***********************************

If you want to protect the status endpoint with a customized
authentication/authorization decorator, you can add ``WATCHMAN_AUTH_DECORATOR``
to your settings. This needs to be a dotted-path to a decorator, and defaults
to ``watchman.decorators.token_required``::

    WATCHMAN_AUTH_DECORATOR = 'django.contrib.admin.views.decorators.staff_member_required'

Note that the ``token_required`` decorator does not protect a view unless the
``WATCHMAN_TOKEN`` is set in settings.

Custom checks
*************

django-watchman allows you to customize the checks which are run by modifying
the ``WATCHMAN_CHECKS`` setting. In ``settings.py``::

    WATCHMAN_CHECKS = (
        'module.path.to.callable',
        'another.module.path.to.callable',
    )

Checks take no arguments, and must return a ``dict`` whose keys are applied to the JSON response. Use the ``watchman.decorators.check`` decorator to capture exceptions::

    from watchman.decorators import check

    @check
    def my_check():
        return {'x': 1}

In the absence of any checks, a 404 is thrown, which is then handled by the
``json_view`` decorator.

Run a subset of available checks
********************************

A subset of checks may be run, by passing ``?check=module.path.to.callable&check=...``
in the request URL. Only the callables given in the querystring which are also
in ``WATCHMAN_CHECKS`` should be run, eg::

    curl -XGET http://127.0.0.1:8080/watchman/?check=watchman.checks.caches

Skip specific checks
********************

You can skip any number of checks, by passing ``?skip=module.path.to.callable&skip=...``
in the request URL. Only the checks in ``WATCHMAN_CHECKS`` which are not in the
querystring should be run, eg::

    curl -XGET http://127.0.0.1:8080/watchman/?skip=watchman.checks.email

Django management command
*************************

You can also run your checks without starting the webserver and making requests.
This can be useful for testing your configuration before enabling a server,
checking configuration on worker servers, etc. Run the management command like so::

    python manage.py watchman

By default, successful checks will not print any output. If all checks pass
successfully, the exit code will be ``0``. If a check fails, the exit code will
be ``1``, and the error message including stack trace will be printed to ``stderr``.

If you'd like to see output for successful checks as well, set verbosity to
``2`` or higher::

    python manage.py watchman -v 2
    {"storage": {"ok": true}}
    {"caches": [{"default": {"ok": true}}]}
    {"databases": [{"default": {"ok": true}}]}

If you'd like to run a subset of checks, use ``-c`` and a comma-separated list
of python module paths::

    python manage.py watchman -c watchman.checks.caches,watchman.checks.databases -v 2
    {"caches": [{"default": {"ok": true}}]}
    {"databases": [{"default": {"ok": true}}]}

If you'd like to skip certain checks, use ``-s`` and a comma-separated list of
python module paths::

    python manage.py watchman -s watchman.checks.caches,watchman.checks.databases -v 2
    {"storage": {"ok": true}}

Use ``-h`` to see a full list of options::

    python manage.py watchman -h

X-Watchman-Version response header
**********************************

Watchman can return the version of watchman which is running to help you keep
track of whether or not your sites are using an up-to-date version. This is
disabled by default to prevent any unintended information leakage for websites
without authentication. To enable, update the ``WATCHMAN_VERSION_HEADER``
setting::

    WATCHMAN_VERSION_HEADER = True

Custom response code
********************

By default, watchman will return a ``200`` HTTP response code, even if there's a
failing check. You can specify a different response code for failing checks
using the ``WATCHMAN_ERROR_CODE`` setting::

    WATCHMAN_ERROR_CODE = 500

Available checks
----------------

caches
******

For each cache in ``django.conf.settings.CACHES``:

* Set a test cache item
* Get test item
* Delete test item

databases
*********

For each database in ``django.conf.settings.DATABASES``:

* Verify connection by calling ``connections[database].introspection.table_names()``

email
*****

Send a test email to ``to@example.com`` using ``django.core.mail.send_mail``.

If you're using a 3rd party mail provider, this check could end up costing you
money, depending how aggressive you are with your monitoring. For this reason,
this check is **not enabled** by default.

For reference, if you were using Mandrill, and hitting your watchman endpoint
once per minute, this would cost you ~$5.60/month.

storage
*******

Using ``django.core.files.storage.default_storage``:

* Write a test file
* Check the test file's size
* Read the test file's contents
* Delete the test file

Default checks
**************

By default, django-watchman will run checks against your databases
(``watchman.checks.databases``), caches (``watchman.checks.caches``), and
storage (``watchman.checks.storage``).

Paid checks
***********

Currently there is only one "paid" check - ``watchman.checks.email``. You can
enable it by setting the ``WATCHMAN_ENABLE_PAID_CHECKS`` to ``True``, or by
overriding the ``WATCHMAN_CHECKS`` setting.

Trying it out with Vagrant
--------------------------

A sample project is available along with a Vagrantfile to make it easy to try
out django-watchman.

Requirements
************

* `Vagrant <https://www.vagrantup.com/>`_
* `Virtualbox <https://www.virtualbox.org/>`_
* `Ansible <http://www.ansible.com/>`_

Instructions
************

1. Launch vagrant box: ``vagrant up``
2. SSH into vagrant: ``vagrant ssh``
3. Activate the virtualenv: ``workon watchman``
4. Launch the development server: ``python manage.py runserver 0.0.0.0:8000``
5. Visit watchman json endpoint in your browser: http://127.0.0.1:8000/watchman/
6. Visit watchman dashboard in your browser: http://127.0.0.1:8000/watchman/dashboard/
