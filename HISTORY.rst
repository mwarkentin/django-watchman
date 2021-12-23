.. :changelog:

=======
History
=======

1.2.0 (2020-09-20)
------------------

* [`#163 <https://github.com/mwarkentin/django-watchman/pull/163>`_] Replaced deprecated url() calls with re_path() (@dominik-bln)

1.1.1 (2020-05-04)
------------------

* [`#159 <https://github.com/mwarkentin/django-watchman/pull/159>`_] Fixed invalid escape sequence in decorators by changing to a raw string

1.1.0 (2020-03-16)
------------------

* [`#154 <https://github.com/mwarkentin/django-watchman/pull/155>`_] Added custom path support for storage check

1.0.1 (YYYY-MM-DD)
------------------

* Fix modal popups on dashboards when Type or Name fields contains spaces (@maikeps)

1.0.0 (2019-12-18)
-------------------

* Official django-watchman 1.0 release! Releases will (try to) follow semantic versioning from now on.
* Drop support for python 2 and Django<2 (@JBKahn)
* Drop usage of ``django-jsonview`` in favor of the Django's built in JsonResponse (@JBKahn)

0.18.0 (2019-08-19)
-------------------

* [`#142 <https://github.com/mwarkentin/django-watchman/pull/142>`_] Skip traces in Datadog if ``WATCHMAN_DISABLE_APM`` is enabled (@robatwave)

0.17.0 (2019-06-14)
-------------------

* [`#141 <https://github.com/mwarkentin/django-watchman/pull/141>`_] Disable APM monitoring on ``ping`` endpoint if ``settings.WATCHMAN_DISABLE_APM`` is configured (@JBKahn)

0.16.0 (2019-03-19)
-------------------

* [`#131 <https://github.com/mwarkentin/django-watchman/pull/131>`_] Make watchman constants importable (@jonespm)
* [`#134 <https://github.com/mwarkentin/django-watchman/pull/134>`_] Update Django/Python versions & clean up sample site Docker (@JayH5)

0.15.0 (2018-02-27)
-------------------

* [`#114 <https://github.com/mwarkentin/django-watchman/pull/114>`_] Add "bare" status view (@jamesmallen)
* [`#115 <https://github.com/mwarkentin/django-watchman/pull/115>`_] Adds ``WATCHMAN_DISABLE_APM`` option (@xfxf)
* [`#63 <https://github.com/mwarkentin/django-watchman/pull/63>`_] Disable watchman version output by default, add ``EXPOSE_WATCHMAN_VERSION`` setting (@mwarkentin)

0.14.0 (2018-01-09)
-------------------

* [`#110 <https://github.com/mwarkentin/django-watchman/pull/110>`_] Replace vagrant + ansible with Dockerfile (@ryanwilsonperkin)
* [`#111 <https://github.com/mwarkentin/django-watchman/pull/111>`_] Configure Django logging for checks (@dhoffman34)
* [`#112 <https://github.com/mwarkentin/django-watchman/pull/112>`_] Add simple HTTP ping endpoint (@dhoffman34)

0.13.1 (2017-05-27)
-------------------

* [`#101 <https://github.com/mwarkentin/django-watchman/pull/101>`_] Write ``bytes`` to dummy file on storage check to fix an issue in Python 3 (thanks @saily!)

0.13.0 (2017-05-23)
-------------------

* [`#105 <https://github.com/mwarkentin/django-watchman/pull/105>`_] Add ``WATCHMAN_CACHES`` and ``WATCHMAN_DATABASES`` settings to override the Django defaults

  * When using watchman with a large number of databases, the default checks can cause an excess of connections to the database / cache
  * New settings allow you to check only a subset of databases / caches
  * Watchman will still default to checking all databases / caches, so no changes necessary for most apps

0.12.0 (2017-02-22)
-------------------

* [`#100 <https://github.com/mwarkentin/django-watchman/pull/100>`_] Add ``WATCHMAN_EMAIL_SENDER`` setting to customize email check "from" address

0.11.1 (2017-02-14)
-------------------

* [`#99 <https://github.com/mwarkentin/django-watchman/pull/99>`_] Fix verbose output in management command on Django 1.8+

0.11.0 (2016-08-02)
-------------------

* Update tests to run on Django 1.7 - 1.10
* [`#87 <https://github.com/mwarkentin/django-watchman/pull/87>`_] Fix 500 errors with ATOMIC_REQUESTS enabled

  * Disables atomic transactions on the watchman views to prevent generic 500 errors

* [`#88 <https://github.com/mwarkentin/django-watchman/pull/88>`_] Restructure dashboard and switch icon libraries

  * Make check types singular on dashboard
  * Switch to FontAwesome instead of Glyphicon to track Bootstrap updates
  * Improve traceback display width

* [`#92 <https://github.com/mwarkentin/django-watchman/pull/92>`_] Support multiple auth tokens

  * Fixes [`#86 <https://github.com/mwarkentin/django-watchman/pull/86>`_]
  * Deprecates ``settings.WATCHMAN_TOKEN`` and adds ``settings.WATCHMAN_TOKENS``

0.10.1 (2016-05-03)
-------------------

* [`#81 <https://github.com/mwarkentin/django-watchman/pull/81>`_] Fix header-based authentication for tokens w/ dashes (`-`)

  * Regex was overly specific for header values (`\w`)
  * Added TODO to follow up with a full regex for valid characters according to the spec

0.10.0 (2016-05-02)
-------------------

* [`#75 <https://github.com/mwarkentin/django-watchman/pull/75>`_] Enable header-based authentication

  * Set a header instead of passing the token via GET param: ``"Authorization: WATCHMAN-TOKEN Token=\":token\""``
  * Improves security by keeping tokens out of logs

* [`#79 <https://github.com/mwarkentin/django-watchman/pull/79>`_] Enable customization of email check

  * Add ``WATCHMAN_EMAIL_RECIPIENTS`` setting - pass a list of recipients the email should be sent to
  * Add ``WATCHMAN_EMAIL_HEADERS`` setting - pass a dict of custom headers to be set on the email


0.9.0 (2015-12-16)
------------------

* [`#51 <https://github.com/mwarkentin/django-watchman/pull/51>`_] Update TravisCI Python / Django versions
* [`#52 <https://github.com/mwarkentin/django-watchman/pull/52>`_] Fix deprecated ``url_patterns``
* [`#53 <https://github.com/mwarkentin/django-watchman/pull/54>`_] Change default error response code to ``500``
* [`#56 <https://github.com/mwarkentin/django-watchman/pull/56>`_] Add ``@check`` decorator and refactor existing checks to use it (thanks @benwebber!)
* [`#57 <https://github.com/mwarkentin/django-watchman/pull/57>`_] Sort ``caches`` / ``databases`` in response for more consistent responses
* [`#59 <https://github.com/mwarkentin/django-watchman/pull/59>`_] Add ``.editorconfig`` for improved consistency in contributions
* [`#61 <https://github.com/mwarkentin/django-watchman/pull/61>`_] Add ``Vagrantfile`` and docs for how to run and develop on Vagrant instance
* [`#65 <https://github.com/mwarkentin/django-watchman/pull/65>`_] Include assets in source tarball for Debian packaging (thanks @fladi)
* [`#71 <https://github.com/mwarkentin/django-watchman/pull/71>`_] Unpin `django-jsonview` in setup.py
* [`#72 <https://github.com/mwarkentin/django-watchman/pull/72>`_] Fix stacktrace on dashboard modal and increase width for better readability

0.8.0 (2015-10-03)
------------------

* [`#46 <https://github.com/mwarkentin/django-watchman/pull/46>`_] Allow custom response codes with the ``WATCHMAN_ERROR_CODE`` setting

0.7.1 (2015-08-14)
------------------

* Update headers in ``HISTORY.rst`` to attempt to fix localshop parsing issues

0.7.0 (2015-08-14)
------------------

* [`#40 <https://github.com/mwarkentin/django-watchman/pull/40>`_] Bump ``django-jsonview`` for improved Django 1.8 compatibility

  * Also brought travis Django test versions in line with currently supported Django versions (1.4.x, 1.7.x, 1.8.x)

0.6.0 (2015-07-02)
------------------

* [`#30 <https://github.com/mwarkentin/django-watchman/pull/30>`_] Allow users to specify a custom authentication/authorization decorator

  * Override the ``@auth`` decorator by setting ``WATCHMAN_AUTH_DECORATOR`` to a dot-separated path to your own decorator
  * eg. ``WATCHMAN_AUTH_DECORATOR = 'django.contrib.admin.views.decorators.staff_member_required'``
  * Token-based authentication remains the default

* [`#31 <https://github.com/mwarkentin/django-watchman/pull/31>`_], [`#34 <https://github.com/mwarkentin/django-watchman/pull/34>`_] Add a human-friendly status dashboard

  * Available at ``<watchman url>/dashboard/``
  * ``?check`` & ``?skip`` GET params work on the dashboard as well

* [`#35 <https://github.com/mwarkentin/django-watchman/pull/35>`_] Add ``X-Watchman-Version`` header to responses

0.5.0 (2015-01-25)
------------------

* Add ``watchman`` management command

  * Exit code of ``0`` if all checks pass, ``1`` otherwise
  * Print json stacktrace to ``stderr`` if check fails
  * Handles ``--verbosity`` option to print all status checks
  * ``-c``, ``--checks``, ``-s``, ``--skips`` options take comma-separated list of python paths to run / skip

* Improve identifiability of emails sent from a django-watchman endpoint

  * From: watchman@example.com
  * Subject: django-watchman email check
  * Body: This is an automated test of the email system.
  * Add ``X-DJANGO-WATCHMAN: True`` custom header

* Add new default check: ``storage`` check

  * Checks that files can be both written and read with the current Django storage engine
  * Add ``WATCHMAN_ENABLE_PAID_CHECKS`` setting to enable all paid checks without modifying ``WATCHMAN_CHECKS``

* Remove ``email_status`` from default checks
* Refactor ``utils.get_checks`` to allow reuse in management command

  * ``get_checks`` now performs the optional check inclusion / skipping
  * ``status`` refactored to pull ``check_list`` / ``skip_list`` from GET params and pass them to ``get_checks``

* Namespace cache keys
* Update documentation

0.4.0 (2014-09-08)
------------------

* Add the ability to skip certain checks by passing one or more
  ``skip=path.to.callable`` GET params when hitting the watchman URL

0.3.0 (2014-09-05)
------------------

* New check - email (``watchman.checks.email_status``)! django-watchman will now
  check that your email settings are working too!
* Fix a few small issues in the readme
* Rearrange some of the code in checks.py

0.2.2 (2014-09-05)
------------------

* Fix and run tests on Python 2.7 and 3.4
* Bump django-jsonview dependency to latest
* Update tox envlist and travis config to test 2.7 / 3.4

0.2.1 (2014-09-04)
------------------

* Initialize django during tests to prevent app loading issue for Django >= 1.7
* Suppress ``MIDDLEWARE_CLASSES`` warning for Django >= 1.7
* Reorganize test imports
* Fix ``make test``, ``make coverage``, ``make release`` commands
* Add htmlcov/ directory to .gitignore
* Test django 1.4, 1.6, 1.7

0.2.0 (2014-09-04)
------------------

* Custom checks can now be written and run using the ``WATCHMAN_CHECKS`` setting
* A subset of the available checks can be run by passing the ``check`` GET param
  when hitting the watchman url

0.1.2 (2014-02-21)
------------------

* Move package requirements out of requirements.txt and into setup.py

0.1.1 (2014-02-09)
------------------

* Remove ``django>=1.5.5`` version specification
* Remove ``wheel`` requirement


0.1.0 (2014-02-08)
------------------

* First release on PyPI.
