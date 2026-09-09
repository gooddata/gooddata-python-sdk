# (C) 2026 GoodData Corporation
"""Langfuse environment resolution: base URL and credentials, shared by all Langfuse call sites."""

from __future__ import annotations

import base64
import os

import httpx

_DEFAULT_BASE_URL = "https://us.cloud.langfuse.com"


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


def make_http_client(*, timeout: float, transport: httpx.BaseTransport | None = None) -> httpx.Client:
    return httpx.Client(
        base_url=resolve_base_url(),
        headers={"Authorization": basic_auth_header()},
        timeout=timeout,
        transport=transport,
    )
