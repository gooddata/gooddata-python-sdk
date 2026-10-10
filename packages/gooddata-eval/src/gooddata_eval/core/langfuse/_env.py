# (C) 2026 GoodData Corporation
"""Langfuse environment resolution: base URL and credentials, shared by all Langfuse call sites."""

from __future__ import annotations

import base64
import os
import re

import httpx

from gooddata_eval._version import __version__

_DEFAULT_BASE_URL = "https://us.cloud.langfuse.com"
SERVICE_NAME = "gooddata-eval"

_LOCAL = "local"
_HEADER_SAFE = re.compile(r"[A-Za-z0-9._-]+")
_SHORT_SHA_LENGTH = 12
# Resource attribute -> the GitHub Actions variable it is read from.
_GITHUB_RESOURCE = {
    "github.run_id": "GITHUB_RUN_ID",
    "github.workflow": "GITHUB_WORKFLOW",
    "github.ref_name": "GITHUB_REF_NAME",
    "github.event_name": "GITHUB_EVENT_NAME",
}


def resolve_base_url() -> str:
    """Resolve the Langfuse base URL: `LANGFUSE_BASE_URL` > `LANGFUSE_HOST` > the US cloud region GoodData uses."""
    base = os.environ.get("LANGFUSE_BASE_URL") or os.environ.get("LANGFUSE_HOST") or _DEFAULT_BASE_URL
    return base.rstrip("/")


def credentials_present() -> bool:
    return bool(os.environ.get("LANGFUSE_PUBLIC_KEY")) and bool(os.environ.get("LANGFUSE_SECRET_KEY"))


def basic_auth_header() -> str:
    if not credentials_present():
        raise RuntimeError("Langfuse credentials not set. Export LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY.")
    pub = os.environ["LANGFUSE_PUBLIC_KEY"]
    sec = os.environ["LANGFUSE_SECRET_KEY"]
    creds = base64.b64encode(f"{pub}:{sec}".encode()).decode()
    return f"Basic {creds}"


def _header_value(name: str) -> str:
    """The variable's value, or "local" when it is unset, blank or unsafe in a header."""
    value = os.environ.get(name, "").strip()
    return value if _HEADER_SAFE.fullmatch(value) else _LOCAL


def user_agent() -> str:
    """``gooddata-eval/<version> (<ci|local>; run=<GITHUB_RUN_ID>; sha=<short GITHUB_SHA>)``."""
    env = "ci" if os.environ.get("GITHUB_ACTIONS") == "true" else _LOCAL
    sha = _header_value("GITHUB_SHA")
    short_sha = sha[:_SHORT_SHA_LENGTH] if sha != _LOCAL else _LOCAL
    return f"{SERVICE_NAME}/{__version__} ({env}; run={_header_value('GITHUB_RUN_ID')}; sha={short_sha})"


def resource_attributes() -> dict[str, str]:
    """OTLP resource attributes of gooddata-eval's spans, with the GitHub run context when set."""
    attributes = {"service.name": SERVICE_NAME, "service.version": __version__}
    for key, variable in _GITHUB_RESOURCE.items():
        value = os.environ.get(variable, "").strip()
        if value:
            attributes[key] = value
    return attributes


def make_http_client(*, timeout: float, transport: httpx.BaseTransport | None = None) -> httpx.Client:
    return httpx.Client(
        base_url=resolve_base_url(),
        headers={"Authorization": basic_auth_header(), "User-Agent": user_agent()},
        timeout=timeout,
        transport=transport,
    )
