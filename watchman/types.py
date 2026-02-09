from typing import TypedDict


class _CheckStatusRequired(TypedDict):
    ok: bool


class CheckStatus(_CheckStatusRequired, total=False):
    """Result of a single health check -- success or error.

    The ``ok`` field is always present. The ``error`` and ``stacktrace``
    fields are only present when the check failed.
    """

    error: str
    stacktrace: str


# A check result: either a direct status (email, storage) or a mapping of
# named statuses keyed by resource name (caches, databases).
CheckResult = CheckStatus | dict[str, CheckStatus]
