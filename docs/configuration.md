# Configuration

## Human-friendly dashboard

Visit `http://127.0.0.1:8000/watchman/dashboard/` to get a human-friendly HTML
representation of all of your watchman checks.

## Token based authentication

If you want to protect the status endpoint, you can use the `WATCHMAN_TOKENS` setting.
This is a comma-separated list of tokens.
When this setting is added, you must pass one of the tokens in as the `watchman-token` **GET** parameter:

```
GET http://127.0.0.1:8000/watchman/?watchman-token=:token
```

Or by setting the `Authorization: WATCHMAN-TOKEN` header on the request:

```bash
curl -X GET -H "Authorization: WATCHMAN-TOKEN Token=\":token\"" http://127.0.0.1:8000/watchman/
```

If you want to change the token name, you can set the `WATCHMAN_TOKEN_NAME`.
The value of this setting will be the **GET** parameter that you must pass in:

```python
WATCHMAN_TOKEN_NAME = 'custom-token-name'
```

```
GET http://127.0.0.1:8000/watchman/?custom-token-name=:token
```

!!! warning "Deprecation Warning"
    `WATCHMAN_TOKEN` was replaced by the `WATCHMAN_TOKENS` setting to support multiple authentication tokens in django-watchman `0.11`. It will continue to work until it's removed in django-watchman `1.0`.

## Custom authentication/authorization

If you want to protect the status endpoint with a customized
authentication/authorization decorator, you can add `WATCHMAN_AUTH_DECORATOR`
to your settings. This needs to be a dotted-path to a decorator, and defaults
to `watchman.decorators.token_required`:

```python
WATCHMAN_AUTH_DECORATOR = 'django.contrib.admin.views.decorators.staff_member_required'
```

!!! note
    The `token_required` decorator does not protect a view unless `WATCHMAN_TOKENS` is set in settings.

## Custom checks

django-watchman allows you to customize the checks which are run by modifying
the `WATCHMAN_CHECKS` setting. In `settings.py`:

```python
WATCHMAN_CHECKS = (
    'module.path.to.callable',
    'another.module.path.to.callable',
)
```

You can also import the watchman.constants to include the DEFAULT_CHECKS and PAID_CHECKS in your `settings.py`:

```python
from watchman import constants as watchman_constants

WATCHMAN_CHECKS = watchman_constants.DEFAULT_CHECKS + ('module.path.to.callable', )
```

Checks take no arguments, and must return a `dict` whose keys are applied to the JSON response.

Use the `watchman.decorators.check` decorator to capture exceptions:

```python
from watchman.decorators import check

def custom_check():
    return {"custom_check": _custom_check()}

@check
def _custom_check():
    return {"ok": True, "extra_info": "if helpful"}
```

In the absence of any checks, a 404 is thrown, which is then handled by the
`json_view` decorator.

## Run a subset of available checks

A subset of checks may be run, by passing `?check=module.path.to.callable&check=...`
in the request URL. Only the callables given in the querystring which are also
in `WATCHMAN_CHECKS` should be run, e.g.:

```bash
curl -XGET http://127.0.0.1:8080/watchman/?check=watchman.checks.caches
```

## Skip specific checks

You can skip any number of checks, by passing `?skip=module.path.to.callable&skip=...`
in the request URL. Only the checks in `WATCHMAN_CHECKS` which are not in the
querystring should be run, e.g.:

```bash
curl -XGET http://127.0.0.1:8080/watchman/?skip=watchman.checks.email
```

## Check a subset of databases or caches

If your application has a large number of databases or caches configured,
watchman may open too many connections as it checks each database or cache.

You can set the `WATCHMAN_DATABASES` or `WATCHMAN_CACHES` settings in order
to override the default set of databases and caches to be monitored.

## Ping

If you want to simply check that your application is running and able to handle
requests, you can call ping:

```
GET http://127.0.0.1:8000/watchman/ping/
```

It will return the text `pong` with a 200 status code. Calling this doesn't
run any of the checks.

## Bare status view

If you would like a "bare" status view (one that doesn't report any details,
just `HTTP 200` if checks pass, and `HTTP 500` if any checks fail), you
can use the `bare_status` view by putting the following into `urls.py`:

```python
import watchman.views
# ...
re_path(r'^status/?$', watchman.views.bare_status),
```

## Django management command

You can also run your checks without starting the webserver and making requests.
This can be useful for testing your configuration before enabling a server,
checking configuration on worker servers, etc. Run the management command like so:

```bash
python manage.py watchman
```

By default, successful checks will not print any output. If all checks pass
successfully, the exit code will be `0`. If a check fails, the exit code will
be `1`, and the error message including stack trace will be printed to `stderr`.

If you'd like to see output for successful checks as well, set verbosity to
`2` or higher:

```bash
python manage.py watchman -v 2
{"storage": {"ok": true}}
{"caches": [{"default": {"ok": true}}]}
{"databases": [{"default": {"ok": true}}]}
```

If you'd like to run a subset of checks, use `-c` and a comma-separated list
of python module paths:

```bash
python manage.py watchman -c watchman.checks.caches,watchman.checks.databases -v 2
{"caches": [{"default": {"ok": true}}]}
{"databases": [{"default": {"ok": true}}]}
```

If you'd like to skip certain checks, use `-s` and a comma-separated list of
python module paths:

```bash
python manage.py watchman -s watchman.checks.caches,watchman.checks.databases -v 2
{"storage": {"ok": true}}
```

Use `-h` to see a full list of options:

```bash
python manage.py watchman -h
```

## X-Watchman-Version response header

Watchman can return the version of watchman which is running to help you keep
track of whether or not your sites are using an up-to-date version. This is
disabled by default to prevent any unintended information leakage for websites
without authentication. To enable, update the `EXPOSE_WATCHMAN_VERSION`
setting:

```python
EXPOSE_WATCHMAN_VERSION = True
```

## Custom response code

By default, watchman will return a `500` HTTP response code, even if there's a
failing check. You can specify a different response code for failing checks
using the `WATCHMAN_ERROR_CODE` setting:

```python
WATCHMAN_ERROR_CODE = 200
```

## Logging

watchman includes log messages using a logger called `watchman`.
You can configure this by configuring the `LOGGING` section of your Django
settings file.

Here is a simple example that would log to the console:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'watchman': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

More information is available in the [Django documentation](https://docs.djangoproject.com/en/stable/topics/logging/#configuring-logging).

## APM (Datadog, New Relic)

If you're using APM and watchman is being often hit for health checks (such as an ELB on
AWS), you will find some stats based on averages will be affected (average transaction
time, apdex, etc).

You can disable APM instrumentation for watchman by using the `WATCHMAN_DISABLE_APM`
setting:

```python
WATCHMAN_DISABLE_APM = True
```

This currently supports the following agents:

- Datadog
- New Relic

Please open an issue if there's another APM you use which is being affected.
