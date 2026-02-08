# django-watchman

[![PyPI version](http://img.shields.io/pypi/v/django-watchman.svg)](http://badge.fury.io/py/django-watchman)
[![Coverage](http://img.shields.io/coveralls/mwarkentin/django-watchman.svg)](https://coveralls.io/r/mwarkentin/django-watchman?branch=main)

django-watchman exposes a status endpoint for your backing services like
databases, caches, etc.

![Ozymandias](https://mwarkentin-snaps.s3.amazonaws.com/Watchmen_The_One_Thing_Nobody_Says_about_Adrian_Veidt_aka_Ozymandias_2022-03-23_08-36-18.png)

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

## License

BSD-3-Clause
