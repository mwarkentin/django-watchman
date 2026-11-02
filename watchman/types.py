from typing import TypedDict


class _CheckStatusRequired(TypedDict):
    ok: bool


class CheckStatus(_CheckStatusRequired, total=False):
    """Result of a single health check -- success or error.

    The ``ok`` field is always present. The ``error`` field is only present
    when the check failed. The ``stacktrace`` field is only present when the
    check failed and
    [`WATCHMAN_EXPOSE_ERROR_DETAILS`][watchman.settings.WATCHMAN_EXPOSE_ERROR_DETAILS]
    is ``True``.
    """

    error: str
    stacktrace: str


# A check result: either a direct status (email, storage) or a mapping of
# named statuses keyed by resource name (caches, databases).
CheckResult = CheckStatus | dict[str, CheckStatus]
