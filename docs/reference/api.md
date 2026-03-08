# API Reference

This is the auto-generated reference for django-watchman's Python API.
For a higher-level overview see the [Getting Started](../getting-started.md)
guide and the [Configuration](../configuration.md) page.

---

## Views

The Django views that power watchman's HTTP endpoints.

::: watchman.views
    options:
      show_source: false
      members:
        - status
        - bare_status
        - ping
        - dashboard
        - run_checks

## Checks

Built-in health-check functions for Django backing services.  Each function
can be referenced by its dotted path in
[`WATCHMAN_CHECKS`][watchman.settings.WATCHMAN_CHECKS].

::: watchman.checks
    options:
      members:
        - caches
        - databases
        - email
        - storage

## Settings

All settings are read from your Django `settings` module with sensible
defaults.  See the [Configuration](../configuration.md) guide for usage
details.

::: watchman.settings

## URLs

Include these in your root URL configuration with
`url(r'^watchman/', include('watchman.urls'))`.

| URL pattern  | View                                          | Name        |
|--------------|-----------------------------------------------|-------------|
| `/`          | [`status`][watchman.views.status]              | `status`    |
| `/dashboard/`| [`dashboard`][watchman.views.dashboard]        | `dashboard` |
| `/ping/`     | [`ping`][watchman.views.ping]                  | `ping`      |

## Constants

::: watchman.constants

## Decorators

::: watchman.decorators
    options:
      show_source: false
      members:
        - check
        - parse_auth_header
        - token_required
        - auth

## Utils

::: watchman.utils
