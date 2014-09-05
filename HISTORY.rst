.. :changelog:

History
-------

0.2.1 (2014-09-04)
++++++++++++++++++

* Initialize django during tests to prevent app loading issue for Django >= 1.7
* Suppress ``MIDDLEWARE_CLASSES`` warning for Django >= 1.7
* Reorganize test imports
* Fix ``make test``, ``make coverage``, ``make release`` commands
* Add htmlcov/ directory to .gitignore
* Test django 1.4, 1.6, 1.7

0.2.0 (2014-09-04)
++++++++++++++++++

* Custom checks can now be written and run using the ``WATCHMAN_CHECKS`` setting
* A subset of the available checks can be run by passing the ``check`` GET param
  when hitting the watchman url

0.1.2 (2014-02-21)
++++++++++++++++++

* Move package requirements out of requirements.txt and into setup.py

0.1.1 (2014-02-09)
++++++++++++++++++

* Remove ``django>=1.5.5`` version specification
* Remove ``wheel`` requirement


0.1.0 (2014-02-08)
++++++++++++++++++

* First release on PyPI.
