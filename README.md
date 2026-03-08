# django-watchman

[![PyPI version](https://img.shields.io/pypi/v/django-watchman.svg)](https://pypi.org/project/django-watchman/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-watchman.svg)](https://pypi.org/project/django-watchman/)
[![PyPI - Django Version](https://img.shields.io/pypi/frameworkversions/django/django-watchman.svg)](https://pypi.org/project/django-watchman/)
[![CI](https://github.com/mwarkentin/django-watchman/actions/workflows/ci.yml/badge.svg)](https://github.com/mwarkentin/django-watchman/actions/workflows/ci.yml)
[![Docs](https://readthedocs.org/projects/django-watchman/badge/?version=stable)](https://django-watchman.readthedocs.io/en/stable/)

django-watchman exposes a status endpoint for your backing services like
databases, caches, etc.

![Ozymandias](https://mwarkentin-snaps.s3.amazonaws.com/Watchmen_The_One_Thing_Nobody_Says_about_Adrian_Veidt_aka_Ozymandias_2022-03-23_08-36-18.png)

## Features

- **Status endpoint** -- JSON response with the health of all backing services
- **Human-friendly dashboard** -- HTML dashboard at `/watchman/dashboard/`
- **Built-in checks** -- Databases, caches, storage, and email out of the box
- **Custom checks** -- Write your own checks and plug them in
- **Token-based authentication** -- Protect the endpoint with configurable tokens
- **Management command** -- Run checks from the CLI via `python manage.py watchman`
- **Ping endpoint** -- Lightweight `/watchman/ping/` endpoint returning `pong`
- **Bare status view** -- Minimal HTTP 200/500 response for load balancers
- **APM integration** -- Suppress tracing for health check endpoints (Datadog, New Relic)

## Endpoints

Including `watchman.urls` gives you three endpoints. The bare status view is added separately in your own `urls.py`.

| Endpoint               | Description                                            | Auth |
|------------------------|--------------------------------------------------------|------|
| `/watchman/`           | JSON response with full check results                  | Yes  |
| `/watchman/dashboard/` | Human-friendly HTML dashboard                          | Yes  |
| `/watchman/ping/`      | Returns `pong` -- no checks run, just a liveness probe | No   |
| `/watchman/bare/`      | Empty response, HTTP 200 or 500 -- wire up manually via `watchman.views.bare_status` | No |

## Built-in Checks

| Check | Module path | Default | Description |
|-------|-------------|---------|-------------|
| Databases | `watchman.checks.databases` | Yes | Verifies connectivity for each database in `DATABASES` |
| Caches | `watchman.checks.caches` | Yes | Sets, gets, and deletes a test key in each cache from `CACHES` |
| Storage | `watchman.checks.storage` | Yes | Writes, reads, and deletes a test file using `default_storage` |
| Email | `watchman.checks.email` | No | Sends a test email -- disabled by default since it may incur costs with third-party providers |

Enable email and other paid checks with `WATCHMAN_ENABLE_PAID_CHECKS = True`, or customize the full list with the `WATCHMAN_CHECKS` setting. You can also write [custom checks](https://django-watchman.readthedocs.io/en/latest/configuration/#custom-checks).

## Documentation

The full documentation is at [django-watchman.readthedocs.io](https://django-watchman.readthedocs.io).

## Testimonials

> We're in love with django-watchman. External monitoring is a vital part of our service offering. Using django-watchman we can introspect the infrastructure of an application via a secure URL. It's very well written and easy to extend. We've recommended it to many of our clients already.

-- Hany Fahim, CEO, [VM Farms](https://vmfarms.com/).

## Quickstart

1. Install `django-watchman`:

    ```bash
    pip install django-watchman
    ```

    Or with [uv](https://docs.astral.sh/uv/):

    ```bash
    uv add django-watchman
    ```

2. Add `watchman` to your `INSTALLED_APPS` setting:

    ```python
    INSTALLED_APPS = (
        ...
        'watchman',
    )
    ```

3. Include the watchman URLconf in your project `urls.py`:

    ```python
    re_path(r'^watchman/', include('watchman.urls')),
    ```

4. Start the development server and visit `http://127.0.0.1:8000/watchman/` to
   get a JSON response of your backing service statuses:

    ```json
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
    ```

5. You can also run checks from the command line:

    ```bash
    python manage.py watchman
    ```

    Use `-v 2` for verbose output, `-c` to run specific checks, or `-s` to skip checks.

## Configuration Highlights

| Setting | Description |
|---------|-------------|
| `WATCHMAN_TOKENS` | Comma-separated tokens to protect the endpoint |
| `WATCHMAN_TOKEN_NAME` | Custom GET parameter name for the token (default: `watchman-token`) |
| `WATCHMAN_AUTH_DECORATOR` | Dotted path to a custom auth decorator (default: `watchman.decorators.token_required`) |
| `WATCHMAN_CHECKS` | Tuple of dotted paths to the checks to run |
| `WATCHMAN_ENABLE_PAID_CHECKS` | Enable paid checks like email (default: `False`) |
| `WATCHMAN_DATABASES` | Subset of `DATABASES` to check |
| `WATCHMAN_CACHES` | Subset of `CACHES` to check |
| `WATCHMAN_ERROR_CODE` | HTTP status code for failing checks (default: `500`) |
| `WATCHMAN_DISABLE_APM` | Suppress APM tracing on watchman views (default: `False`) |
| `EXPOSE_WATCHMAN_VERSION` | Include `X-Watchman-Version` response header (default: `False`) |

See the [full configuration documentation](https://django-watchman.readthedocs.io/en/latest/configuration/) for details and examples.

## Contributing

Contributions are welcome! Please see the [contributing guide](https://github.com/mwarkentin/django-watchman/blob/main/CONTRIBUTING.md) for details on how to get started.

## License

BSD-3-Clause
