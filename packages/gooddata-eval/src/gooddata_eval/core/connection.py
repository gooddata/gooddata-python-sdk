# (C) 2026 GoodData Corporation
"""Resolve (host, token) from explicit flags, environment, or a gooddata.yaml profile."""

import os

from gooddata_sdk.utils import profile_content


class ConnectionError_(Exception):
    """Raised when host/token cannot be resolved."""


def resolve_connection(host: str | None, token: str | None, profile: str | None) -> tuple[str, str]:
    """Resolve connection parameters.

    Precedence: explicit flags > GOODDATA_TOKEN env (token only) > profile file.

    Raises:
        ConnectionError_: host or token could not be determined.
    """
    resolved_host = host
    resolved_token = token or os.environ.get("GOODDATA_TOKEN")

    if profile is not None and (resolved_host is None or resolved_token is None):
        content = profile_content(profile)
        resolved_host = resolved_host or content.get("host")
        resolved_token = resolved_token or content.get("token")

    if not resolved_host:
        raise ConnectionError_("Missing host. Pass --host or use a --profile that defines it.")
    if not resolved_token:
        raise ConnectionError_("Missing token. Pass --token, set GOODDATA_TOKEN, or use a --profile that defines it.")
    return resolved_host, resolved_token
