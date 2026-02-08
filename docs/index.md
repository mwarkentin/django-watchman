# django-watchman

[![PyPI version](http://img.shields.io/pypi/v/django-watchman.svg)](http://badge.fury.io/py/django-watchman)
[![Coverage](http://img.shields.io/coveralls/mwarkentin/django-watchman.svg)](https://coveralls.io/r/mwarkentin/django-watchman?branch=main)

django-watchman exposes a status endpoint for your backing services like
databases, caches, etc.

![Ozymandias](https://mwarkentin-snaps.s3.amazonaws.com/Watchmen_The_One_Thing_Nobody_Says_about_Adrian_Veidt_aka_Ozymandias_2022-03-23_08-36-18.png)

## Testimonials

> We're in love with django-watchman. External monitoring is a vital part of our service offering. Using django-watchman we can introspect the infrastructure of an application via a secure URL. It's very well written and easy to extend. We've recommended it to many of our clients already.

-- Hany Fahim, CEO, [VM Farms](https://vmfarms.com/).

## PyCon Canada Presentation (10 minutes)

[![PyCon Canada Talk](https://mwarkentin-snaps.s3.amazonaws.com/Full-stack_Django_application_monitoring_with_django-watchman_Michael_Warkentin_-_YouTube_2022-03-23_08-34-24.png)](https://www.youtube.com/watch?v=iEgOCY7_zGI)

## Features

- **Status endpoint** -- JSON response with the status of all backing services
- **Human-friendly dashboard** -- HTML dashboard at `/watchman/dashboard/`
- **Token-based authentication** -- Protect the endpoint with configurable tokens
- **Custom checks** -- Write your own checks and plug them in
- **Management command** -- Run checks from the command line
- **Ping endpoint** -- Simple `/watchman/ping/` endpoint returning `pong`
- **Bare status view** -- Minimal HTTP 200/500 response for load balancers
- **APM integration** -- Disable tracing for health check endpoints (Datadog, New Relic)

Get started with the [installation guide](getting-started.md) or explore the full [configuration options](configuration.md).
