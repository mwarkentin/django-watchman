# Monitoring Integrations

django-watchman exposes HTTP endpoints that external uptime monitoring services
can poll to determine the health of your Django application and its backing
services. This page describes how django-watchman's endpoints map to the
capabilities of common monitoring vendors.

## Endpoint Quick Reference

django-watchman provides three endpoint types, each suited to different
monitoring strategies:

| Endpoint | Response | Content-Type | Use Case |
|---|---|---|---|
| `/watchman/` | JSON with per-service status | `application/json` | Keyword/body matching, detailed health inspection |
| `/watchman/bare/` | Empty body, HTTP 200 or 500 | N/A | Simple status-code checks, load balancer health checks |
| `/watchman/ping/` | `pong` | `text/plain` | Lightweight liveness probes, heartbeat monitors |

The **status endpoint** (`/watchman/`) returns a JSON object containing the
result of each configured check. A successful response looks like:

```json
{
    "databases": [{"default": {"ok": true}}],
    "caches": [{"default": {"ok": true}}],
    "storage": {"ok": true}
}
```

When any check fails, the response includes error details and the HTTP status
code changes to 500 (configurable via `WATCHMAN_ERROR_CODE`).

The **bare status endpoint** (`/watchman/bare/`) runs the same checks but
returns only an HTTP status code with no body — 200 when all checks pass,
500 when any check fails.

The **ping endpoint** (`/watchman/ping/`) performs no checks and returns the
text `pong` with a 200 status code. It confirms only that the Django process
is running and can handle requests.

## Authentication

When `WATCHMAN_TOKENS` is configured, monitoring services must include a valid
token with each request. django-watchman accepts tokens via two methods:

**Query parameter** (supported by all vendors):

```
GET /watchman/?watchman-token=<token>
```

**Authorization header** (requires vendor support for custom headers):

```
Authorization: WATCHMAN-TOKEN Token="<token>"
```

The query parameter name defaults to `watchman-token` and can be changed with
the `WATCHMAN_TOKEN_NAME` setting. The `/watchman/ping/` endpoint does not
require authentication.

!!! tip
    If your monitoring vendor does not support custom HTTP headers, use the
    query parameter method. All vendors listed below support query parameters
    in the check URL.

---

## Vendors

### [Better Stack](https://betterstack.com) (formerly Better Uptime)

Better Stack is a SaaS observability platform whose uptime monitoring product
supports HTTP status code checks, keyword checks, and multi-step API monitors.

**Recommended endpoint:** `/watchman/bare/` for status-code monitoring, or
`/watchman/` with a keyword monitor to match against the JSON response body.

**Authentication:** Include the token as a query parameter in the check URL.
Better Stack supports custom request headers and HTTP authentication (bearer
token, basic auth) via advanced settings.

**Response interpretation:** The "status" monitor type checks for a 2xx HTTP
status code. The "keyword" monitor type verifies that a required keyword
appears in the response body. The "expected_status_code" type checks for a
specific HTTP status code.

**Vendor documentation:** [Uptime monitor](https://betterstack.com/docs/uptime/uptime-monitor)

---

### [Cronitor](https://cronitor.io)

Cronitor is a SaaS monitoring platform for cron jobs, heartbeats, and HTTP
endpoints. Its uptime monitoring product polls URLs and evaluates assertions
against the response.

**Recommended endpoint:** `/watchman/bare/` for simple status-code assertions,
or `/watchman/` for body-content assertions against the JSON response.

**Authentication:** Include the token as a query parameter in the check URL.
Cronitor supports custom request headers including `Authorization` for
header-based authentication.

**Response interpretation:** Cronitor evaluates configurable assertions on the
response: `response.code = 200` for status-code checks,
`response.body contains "ok"` for keyword checks, and
`response.time < 2s` for latency thresholds.

**Vendor documentation:** [Website & API Monitoring](https://cronitor.io/docs/uptime-monitoring)

---

### [Datadog Synthetics](https://www.datadoghq.com/product/synthetic-monitoring/)

Datadog Synthetics is a synthetic monitoring product within the Datadog
observability platform. It executes HTTP tests from managed or private
locations and evaluates assertions on the response.

**Recommended endpoint:** `/watchman/` for full assertion coverage (status
code, body content, headers), or `/watchman/bare/` for status-code-only
assertions.

**Authentication:** Include the token as a query parameter in the check URL,
or configure a custom request header in the test's advanced options. Datadog
Synthetics also supports basic auth, bearer tokens, and client certificate
(mTLS) authentication.

**Response interpretation:** Assertions can validate the HTTP status code,
response body content (including JSON path expressions), response headers, and
response time. Multiple assertions can be combined in a single test.

!!! note
    If you use Datadog APM alongside Synthetics, set `WATCHMAN_DISABLE_APM = True`
    to prevent health-check traffic from skewing your application's average
    transaction time and Apdex score.

**Vendor documentation:** [HTTP Testing](https://docs.datadoghq.com/synthetics/api_tests/http_tests)

---

### [Pingdom](https://www.pingdom.com)

Pingdom is a SaaS uptime monitoring service (now part of SolarWinds) that
polls URLs from multiple global locations.

**Recommended endpoint:** `/watchman/bare/` for simple uptime checks, or
`/watchman/` with string matching for detailed health verification.

**Authentication:** Include the token as a query parameter in the check URL.
Pingdom also supports custom request headers for header-based authentication.

**Response interpretation:** Pingdom evaluates checks by HTTP status code
(expects 2xx). The optional "string should contain" setting can verify that a
keyword such as `"ok": true` appears in the JSON response body.

**Vendor documentation:** [How to set up an HTTP(S) check](https://documentation.solarwinds.com/en/success_center/pingdom/content/topics/how-to-set-up-a-http-s-check.htm)

---

### [Sentry](https://sentry.io)

Sentry Uptime Monitoring continuously tracks configured URLs from multiple
geographic locations, delivering alerts and linking downtime to application
errors via distributed tracing.

**Recommended endpoint:** `/watchman/bare/` for status-code monitoring.

**Authentication:** Include the token as a query parameter in the check URL.
Sentry supports custom HTTP methods, headers, and request bodies when
configuring an uptime alert.

**Response interpretation:** Sentry expects a 2xx HTTP status code and marks
the check as failed if the response times out (10 seconds) or returns a
non-2xx status. An issue is created after three consecutive failures from
different geographic regions to reduce false positives.

**Vendor documentation:** [Uptime Monitoring](https://docs.sentry.io/product/uptime-monitoring/)

---

### [StatusCake](https://www.statuscake.com)

StatusCake is a SaaS uptime monitoring platform with HTTP checks, page speed
monitoring, and SSL certificate tracking.

**Recommended endpoint:** `/watchman/bare/` for basic uptime checks, or
`/watchman/` with string matching for content-based verification.

**Authentication:** Include the token as a query parameter in the check URL.
StatusCake supports custom headers in JSON format for header-based
authentication.

**Response interpretation:** StatusCake HTTP checks validate the HTTP status
code. The "string match" option can verify that a specific string appears (or
does not appear) in the response body or headers.

**Vendor documentation:** [Create a Basic Website Test](https://www.statuscake.com/kb/knowledge-base/create-a-basic-website-test/)

---

### [updown.io](https://updown.io)

updown.io is a lightweight SaaS monitoring service with per-request pricing
and a simple HTTP check model.

**Recommended endpoint:** `/watchman/bare/` for status-code checks, or
`/watchman/` with string matching for content verification.

**Authentication:** Include the token as a query parameter in the check URL.
updown.io supports custom HTTP headers for header-based authentication.

**Response interpretation:** updown.io checks the HTTP status code (expects
2xx by default; the expected status code is
[configurable](https://updown.io/faq/is-it-possible-to-change-the-expected-http-response-code)).
String matching can verify that specific text appears in the response body.

**Vendor documentation:** [updown.io documentation](https://updown.io/doc)

---

### [Upptime](https://upptime.js.org)

Upptime is a free, open-source uptime monitor powered by GitHub Actions.
Monitoring configuration is defined in a `.upptimerc.yml` file in a GitHub
repository, and checks run on a schedule via GitHub Actions workflows.

**Recommended endpoint:** `/watchman/` for response body validation, or
`/watchman/ping/` for a minimal liveness check that avoids running backing
service checks on every poll.

**Authentication:** Include the token as a query parameter in the site URL.
For private tokens, use a GitHub repository secret (prefixed with `$` in the
configuration) to avoid exposing the token in the public configuration file.

**Response interpretation:** Upptime checks the HTTP status code (expects
2xx). The configuration supports custom headers and request bodies for more
advanced checks.

**Example `.upptimerc.yml` configuration:**

```yaml
sites:
  - name: My Django App
    url: https://example.com/watchman/?watchman-token=$WATCHMAN_TOKEN
    method: GET
    expectedStatusCodes:
      - 200
```

**Vendor documentation:** [Configuration](https://upptime.js.org/docs/configuration/)

---

### [UptimeRobot](https://uptimerobot.com)

UptimeRobot is a SaaS monitoring service offering HTTP and keyword monitoring
with a free tier.

**Recommended endpoint:** `/watchman/bare/` for HTTP monitoring, or
`/watchman/` with keyword monitoring to match against the JSON response body.

**Authentication:** Include the token as a query parameter in the check URL.
UptimeRobot supports custom HTTP headers on paid plans.

**Response interpretation:** HTTP monitors check for a 200 status code.
Keyword monitors search the response body for a specified string and trigger
an alert based on whether the keyword exists or is absent. Matching
`"ok": true` in the response body confirms healthy checks.

**Vendor documentation:** [UptimeRobot Monitor Types](https://help.uptimerobot.com/en/articles/11358441-uptimerobot-monitor-types-explained-http-ping-port-keyword-monitoring)
