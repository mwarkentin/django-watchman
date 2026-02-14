# Changelog

## Unreleased

### Security

- [#213](https://github.com/mwarkentin/django-watchman/pull/213) Fix ReDoS vulnerability in auth header parsing — replace regex-based `Authorization` header parser with simple string splitting to prevent polynomial backtracking on crafted input

### Added

- [#212](https://github.com/mwarkentin/django-watchman/pull/212) Add type annotations to all source modules and ship PEP 561 `py.typed` marker for downstream type checking
- [#212](https://github.com/mwarkentin/django-watchman/pull/212) Add Python 3.14 support
- [#214](https://github.com/mwarkentin/django-watchman/pull/214) Automate PyPI publishing with GitHub Actions trusted publishing (OIDC, no API tokens needed)

### Changed

- [#206](https://github.com/mwarkentin/django-watchman/pull/206) Modernize project infrastructure:
  - Replace black, flake8, and isort with ruff for linting and formatting
  - Switch from `make` to [`just`](https://github.com/casey/just) as the task runner
  - Migrate from `setup.py` / `MANIFEST.in` to `pyproject.toml` with Hatch build backend
  - Update CI test matrix: drop Django 5.0 (EOL), add Django 5.2 (LTS)
  - Expand Dependabot to cover GitHub Actions and pip dependencies
  - Modernize tests to use `pathlib`; remove legacy `runtests.py` wrapper
  - Add test runner and ty type checker to pre-commit hooks
- [#206](https://github.com/mwarkentin/django-watchman/pull/206) Fix storage check to handle `pathlib.Path` objects for `MEDIA_ROOT` and `WATCHMAN_STORAGE_PATH`
- [#214](https://github.com/mwarkentin/django-watchman/pull/214) Read version dynamically from `watchman/__init__.py` via Hatchling (eliminate duplication in `pyproject.toml`)

### Documentation

- [#211](https://github.com/mwarkentin/django-watchman/pull/211) Switch documentation from Sphinx/reStructuredText to MkDocs with Material theme
- [#190](https://github.com/mwarkentin/django-watchman/pull/190) Clarify custom checks and paid checks documentation
- [#201](https://github.com/mwarkentin/django-watchman/pull/201) Update `WATCHMAN_STORAGE_PATH` documentation in README
- [#189](https://github.com/mwarkentin/django-watchman/pull/189) Add custom check example to sample project

## 1.3.0 (2022-02-24)

- [#181](https://github.com/mwarkentin/django-watchman/pull/181) Update sample project to Django 4.x
- [#171](https://github.com/mwarkentin/django-watchman/pull/171) Improve database check performance: replace introspection.table_names() by a simple cursor query (@cristianemoyano)
- [#180](https://github.com/mwarkentin/django-watchman/pull/180), [#174](https://github.com/mwarkentin/django-watchman/pull/174) Switch testing to Github Actions from TravisCI, update to latest versions
- [#178](https://github.com/mwarkentin/django-watchman/pull/178) Add black, flake8, and isort linting

## 1.2.0 (2020-09-20)

- [#163](https://github.com/mwarkentin/django-watchman/pull/163) Replaced deprecated url() calls with re_path() (@dominik-bln)

## 1.1.1 (2020-05-04)

- [#159](https://github.com/mwarkentin/django-watchman/pull/159) Fixed invalid escape sequence in decorators by changing to a raw string

## 1.1.0 (2020-03-16)

- [#154](https://github.com/mwarkentin/django-watchman/pull/155) Added custom path support for storage check

## 1.0.1 (YYYY-MM-DD)

- Fix modal popups on dashboards when Type or Name fields contains spaces (@maikeps)

## 1.0.0 (2019-12-18)

- Official django-watchman 1.0 release! Releases will (try to) follow semantic versioning from now on.
- Drop support for python 2 and Django<2 (@JBKahn)
- Drop usage of `django-jsonview` in favor of the Django's built in JsonResponse (@JBKahn)

## 0.18.0 (2019-08-19)

- [#142](https://github.com/mwarkentin/django-watchman/pull/142) Skip traces in Datadog if `WATCHMAN_DISABLE_APM` is enabled (@robatwave)

## 0.17.0 (2019-06-14)

- [#141](https://github.com/mwarkentin/django-watchman/pull/141) Disable APM monitoring on `ping` endpoint if `settings.WATCHMAN_DISABLE_APM` is configured (@JBKahn)

## 0.16.0 (2019-03-19)

- [#131](https://github.com/mwarkentin/django-watchman/pull/131) Make watchman constants importable (@jonespm)
- [#134](https://github.com/mwarkentin/django-watchman/pull/134) Update Django/Python versions & clean up sample site Docker (@JayH5)

## 0.15.0 (2018-02-27)

- [#114](https://github.com/mwarkentin/django-watchman/pull/114) Add "bare" status view (@jamesmallen)
- [#115](https://github.com/mwarkentin/django-watchman/pull/115) Adds `WATCHMAN_DISABLE_APM` option (@xfxf)
- [#63](https://github.com/mwarkentin/django-watchman/pull/63) Disable watchman version output by default, add `EXPOSE_WATCHMAN_VERSION` setting (@mwarkentin)

## 0.14.0 (2018-01-09)

- [#110](https://github.com/mwarkentin/django-watchman/pull/110) Replace vagrant + ansible with Dockerfile (@ryanwilsonperkin)
- [#111](https://github.com/mwarkentin/django-watchman/pull/111) Configure Django logging for checks (@dhoffman34)
- [#112](https://github.com/mwarkentin/django-watchman/pull/112) Add simple HTTP ping endpoint (@dhoffman34)

## 0.13.1 (2017-05-27)

- [#101](https://github.com/mwarkentin/django-watchman/pull/101) Write `bytes` to dummy file on storage check to fix an issue in Python 3 (thanks @saily!)

## 0.13.0 (2017-05-23)

- [#105](https://github.com/mwarkentin/django-watchman/pull/105) Add `WATCHMAN_CACHES` and `WATCHMAN_DATABASES` settings to override the Django defaults
    - When using watchman with a large number of databases, the default checks can cause an excess of connections to the database / cache
    - New settings allow you to check only a subset of databases / caches
    - Watchman will still default to checking all databases / caches, so no changes necessary for most apps

## 0.12.0 (2017-02-22)

- [#100](https://github.com/mwarkentin/django-watchman/pull/100) Add `WATCHMAN_EMAIL_SENDER` setting to customize email check "from" address

## 0.11.1 (2017-02-14)

- [#99](https://github.com/mwarkentin/django-watchman/pull/99) Fix verbose output in management command on Django 1.8+

## 0.11.0 (2016-08-02)

- Update tests to run on Django 1.7 - 1.10
- [#87](https://github.com/mwarkentin/django-watchman/pull/87) Fix 500 errors with ATOMIC_REQUESTS enabled
    - Disables atomic transactions on the watchman views to prevent generic 500 errors
- [#88](https://github.com/mwarkentin/django-watchman/pull/88) Restructure dashboard and switch icon libraries
    - Make check types singular on dashboard
    - Switch to FontAwesome instead of Glyphicon to track Bootstrap updates
    - Improve traceback display width
- [#92](https://github.com/mwarkentin/django-watchman/pull/92) Support multiple auth tokens
    - Fixes [#86](https://github.com/mwarkentin/django-watchman/pull/86)
    - Deprecates `settings.WATCHMAN_TOKEN` and adds `settings.WATCHMAN_TOKENS`

## 0.10.1 (2016-05-03)

- [#81](https://github.com/mwarkentin/django-watchman/pull/81) Fix header-based authentication for tokens w/ dashes (`-`)
    - Regex was overly specific for header values (`\w`)
    - Added TODO to follow up with a full regex for valid characters according to the spec

## 0.10.0 (2016-05-02)

- [#75](https://github.com/mwarkentin/django-watchman/pull/75) Enable header-based authentication
    - Set a header instead of passing the token via GET param: `"Authorization: WATCHMAN-TOKEN Token=\":token\""`
    - Improves security by keeping tokens out of logs
- [#79](https://github.com/mwarkentin/django-watchman/pull/79) Enable customization of email check
    - Add `WATCHMAN_EMAIL_RECIPIENTS` setting - pass a list of recipients the email should be sent to
    - Add `WATCHMAN_EMAIL_HEADERS` setting - pass a dict of custom headers to be set on the email

## 0.9.0 (2015-12-16)

- [#51](https://github.com/mwarkentin/django-watchman/pull/51) Update TravisCI Python / Django versions
- [#52](https://github.com/mwarkentin/django-watchman/pull/52) Fix deprecated `url_patterns`
- [#53](https://github.com/mwarkentin/django-watchman/pull/54) Change default error response code to `500`
- [#56](https://github.com/mwarkentin/django-watchman/pull/56) Add `@check` decorator and refactor existing checks to use it (thanks @benwebber!)
- [#57](https://github.com/mwarkentin/django-watchman/pull/57) Sort `caches` / `databases` in response for more consistent responses
- [#59](https://github.com/mwarkentin/django-watchman/pull/59) Add `.editorconfig` for improved consistency in contributions
- [#61](https://github.com/mwarkentin/django-watchman/pull/61) Add `Vagrantfile` and docs for how to run and develop on Vagrant instance
- [#65](https://github.com/mwarkentin/django-watchman/pull/65) Include assets in source tarball for Debian packaging (thanks @fladi)
- [#71](https://github.com/mwarkentin/django-watchman/pull/71) Unpin `django-jsonview` in setup.py
- [#72](https://github.com/mwarkentin/django-watchman/pull/72) Fix stacktrace on dashboard modal and increase width for better readability

## 0.8.0 (2015-10-03)

- [#46](https://github.com/mwarkentin/django-watchman/pull/46) Allow custom response codes with the `WATCHMAN_ERROR_CODE` setting

## 0.7.1 (2015-08-14)

- Update headers in `HISTORY.rst` to attempt to fix localshop parsing issues

## 0.7.0 (2015-08-14)

- [#40](https://github.com/mwarkentin/django-watchman/pull/40) Bump `django-jsonview` for improved Django 1.8 compatibility
    - Also brought travis Django test versions in line with currently supported Django versions (1.4.x, 1.7.x, 1.8.x)

## 0.6.0 (2015-07-02)

- [#30](https://github.com/mwarkentin/django-watchman/pull/30) Allow users to specify a custom authentication/authorization decorator
    - Override the `@auth` decorator by setting `WATCHMAN_AUTH_DECORATOR` to a dot-separated path to your own decorator
    - eg. `WATCHMAN_AUTH_DECORATOR = 'django.contrib.admin.views.decorators.staff_member_required'`
    - Token-based authentication remains the default
- [#31](https://github.com/mwarkentin/django-watchman/pull/31), [#34](https://github.com/mwarkentin/django-watchman/pull/34) Add a human-friendly status dashboard
    - Available at `<watchman url>/dashboard/`
    - `?check` & `?skip` GET params work on the dashboard as well
- [#35](https://github.com/mwarkentin/django-watchman/pull/35) Add `X-Watchman-Version` header to responses

## 0.5.0 (2015-01-25)

- Add `watchman` management command
    - Exit code of `0` if all checks pass, `1` otherwise
    - Print json stacktrace to `stderr` if check fails
    - Handles `--verbosity` option to print all status checks
    - `-c`, `--checks`, `-s`, `--skips` options take comma-separated list of python paths to run / skip
- Improve identifiability of emails sent from a django-watchman endpoint
    - From: watchman@example.com
    - Subject: django-watchman email check
    - Body: This is an automated test of the email system.
    - Add `X-DJANGO-WATCHMAN: True` custom header
- Add new default check: `storage` check
    - Checks that files can be both written and read with the current Django storage engine
    - Add `WATCHMAN_ENABLE_PAID_CHECKS` setting to enable all paid checks without modifying `WATCHMAN_CHECKS`
- Remove `email_status` from default checks
- Refactor `utils.get_checks` to allow reuse in management command
    - `get_checks` now performs the optional check inclusion / skipping
    - `status` refactored to pull `check_list` / `skip_list` from GET params and pass them to `get_checks`
- Namespace cache keys
- Update documentation

## 0.4.0 (2014-09-08)

- Add the ability to skip certain checks by passing one or more `skip=path.to.callable` GET params when hitting the watchman URL

## 0.3.0 (2014-09-05)

- New check - email (`watchman.checks.email_status`)! django-watchman will now check that your email settings are working too!
- Fix a few small issues in the readme
- Rearrange some of the code in checks.py

## 0.2.2 (2014-09-05)

- Fix and run tests on Python 2.7 and 3.4
- Bump django-jsonview dependency to latest
- Update tox envlist and travis config to test 2.7 / 3.4

## 0.2.1 (2014-09-04)

- Initialize django during tests to prevent app loading issue for Django >= 1.7
- Suppress `MIDDLEWARE_CLASSES` warning for Django >= 1.7
- Reorganize test imports
- Fix `make test`, `make coverage`, `make release` commands
- Add htmlcov/ directory to .gitignore
- Test django 1.4, 1.6, 1.7

## 0.2.0 (2014-09-04)

- Custom checks can now be written and run using the `WATCHMAN_CHECKS` setting
- A subset of the available checks can be run by passing the `check` GET param when hitting the watchman url

## 0.1.2 (2014-02-21)

- Move package requirements out of requirements.txt and into setup.py

## 0.1.1 (2014-02-09)

- Remove `django>=1.5.5` version specification
- Remove `wheel` requirement

## 0.1.0 (2014-02-08)

- First release on PyPI.
