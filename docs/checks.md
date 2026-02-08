# Available Checks

## caches

For each cache in `django.conf.settings.CACHES`:

- Set a test cache item
- Get test item
- Delete test item

## databases

For each database in `django.conf.settings.DATABASES`:

- Verify connection by calling `connections[database].introspection.table_names()`

## email

Send a test email to `to@example.com` using `django.core.mail.send_mail`.

If you're using a 3rd party mail provider, this check could end up costing you
money, depending how aggressive you are with your monitoring. For this reason,
this check is **not enabled** by default.

For reference, if you were using Mandrill, and hitting your watchman endpoint
once per minute, this would cost you ~$5.60/month.

### Custom Settings

- `WATCHMAN_EMAIL_SENDER` (default: `watchman@example.com`): Specify an email to be the sender of the test email
- `WATCHMAN_EMAIL_RECIPIENTS` (default: `[to@example.com]`): Specify a list of email addresses to send the test email
- `WATCHMAN_EMAIL_HEADERS` (default: `{}`): Specify a dict of custom headers to be added to the test email

## storage

Using `django.core.files.storage.default_storage`:

- Write a test file
- Check the test file's size
- Read the test file's contents
- Delete the test file

By default the test file gets written on the root of the django `MEDIA_ROOT`.

There are two reasons why you may need to override this. You can use
the setting `WATCHMAN_STORAGE_PATH` to accomplish this.

1. Django triggers a [`django.core.exceptions.SuspiciousFileOperation`](https://docs.djangoproject.com/en/5.0/ref/exceptions/#suspiciousoperation) on the storage check.

2. If for whatever reason, the base of `MEDIA_ROOT` is not writable by
the user that runs Django.

In either case, choose a path within and relative to `MEDIA_ROOT`.

```python
WATCHMAN_STORAGE_PATH = "django-watchman/"
```

If the `MEDIA_ROOT` is already defined:

```python
from os.path import join as joinpath
WATCHMAN_STORAGE_PATH = joinpath(MEDIA_ROOT, "django-watchman/")
```

## Default checks

By default, django-watchman will run checks against your databases
(`watchman.checks.databases`), caches (`watchman.checks.caches`), and
storage (`watchman.checks.storage`).

## Paid checks

Paid checks are checks which may cost you money if they are run regularly.

Currently there is only one "paid" check - `watchman.checks.email`. Many
times email is sent using managed services like SendGrid or Mailgun. You can
enable it by setting the `WATCHMAN_ENABLE_PAID_CHECKS` to `True`, or by
overriding the `WATCHMAN_CHECKS` setting.
