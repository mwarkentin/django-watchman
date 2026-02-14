# Getting Started

## Installation

Install `django-watchman` using pip:

```bash
pip install django-watchman
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add django-watchman
```

## Quickstart

1. Add `watchman` to your `INSTALLED_APPS` setting:

    ```python
    INSTALLED_APPS = (
        ...
        'watchman',
    )
    ```

2. Include the watchman URLconf in your project `urls.py`:

    ```python
    from django.urls import re_path, include

    urlpatterns = [
        ...
        re_path(r'^watchman/', include('watchman.urls')),
    ]
    ```

3. Start the development server and visit `http://127.0.0.1:8000/watchman/` to
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
