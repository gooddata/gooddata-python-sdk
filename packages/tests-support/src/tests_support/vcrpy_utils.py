# (C) 2022 GoodData Corporation
from __future__ import annotations

import os
import re
import typing
from typing import Any
from urllib.parse import urlparse

import orjson
import vcr
import yaml
from vcr.record_mode import RecordMode

VCR_MATCH_ON = ("method", "path", "query", "body")
NON_STATIC_HEADERS = ["DATE", "X-GDC-CANCEL-TOKEN", "X-GDC-TRACE-ID"]

# Infrastructure headers injected by reverse proxies / load balancers.
# These differ between local and staging and are irrelevant to API behavior.
_STRIPPED_RESPONSE_HEADERS = {
    "X-Xss-Protection",
    "Strict-Transport-Security",
    "Vary",
    "Content-Encoding",
    "Content-Length",
    "Transfer-Encoding",
    "Referrer-Policy",
    "Cache-Control",
}
HEADERS_STR = "headers"
PLACEHOLDER = ["PLACEHOLDER"]

# Fields stripped from request bodies before VCR body matching.
# These differ between local and staging environments but don't affect
# the logical identity of a request.
_ENV_SPECIFIC_BODY_FIELDS = {
    "password",
    "token",
    "url",
    "username",
    "privateKey",
    "client_secret",
    "private_key_passphrase",
}

# Canonical (local) values — cassettes always use these.
_CANONICAL_HOST = "http://localhost:3000"
_CANONICAL_HOSTNAME = "localhost"
_CANONICAL_ORG_ID = "default"
_CANONICAL_ORG_NAME = "Default Organization"
_CANONICAL_DS_URL = "jdbc:postgresql://postgres:5432/tiger?sslmode=prefer"
_CANONICAL_DS_PASSWORD = "passw0rd"

# Module-level normalization state.
# Populated by configure_normalization() before tests run.
# Each entry is (source_string, replacement_string).
# Ordered longest-first so more specific patterns match before substrings.
_normalization_replacements: list[tuple[str, str]] = []
_password_replacements: list[tuple[re.Pattern, str]] = []
_normalization_configured: bool = False

# --- Timestamp normalization ---
_CREATED_AT_RE = re.compile(
    r'(?<=createdAt": ")\d{4}-\d{2}-\d{2} \d{2}:\d{2}'  # JSON (stdlib): "createdAt": "..."
    r"|"
    r'(?<=createdAt":")\d{4}-\d{2}-\d{2} \d{2}:\d{2}'  # JSON (orjson):  "createdAt":"..."
    r"|"
    r"(?<=createdAt: )\d{4}-\d{2}-\d{2} \d{2}:\d{2}"  # YAML: createdAt: ...
)
_CANONICAL_CREATED_AT = "2000-01-01 00:00"

# --- Dynamic hash normalization ---
# executionResult: 40-hex ":" 64-hex (body uses ":", URI uses "%3A")
_EXEC_HASH_BODY_RE = re.compile(r"[0-9a-f]{40}:[0-9a-f]{64}")
_EXEC_HASH_URI_RE = re.compile(r"[0-9a-f]{40}%3[Aa][0-9a-f]{64}")

# exportResult: 40-hex, anchored to /export/tabular/ in URIs
# or preceded by "exportResult" context in bodies
_EXPORT_HASH_URI_RE = re.compile(r"(?<=/export/tabular/)[0-9a-f]{40}(?![0-9a-f])")
_EXPORT_HASH_BODY_RE = re.compile(
    r'(?<=exportResult": ")[0-9a-f]{40}(?![0-9a-f])'  # JSON: "exportResult": "hash"
    r"|"
    r'(?<=exportResult":")[0-9a-f]{40}(?![0-9a-f])'  # JSON (orjson)
    r"|"
    r"(?<=exportResult: )[0-9a-f]{40}(?![0-9a-f])"  # YAML
)


_CANONICAL_EXECUTION_RESULT = "EXECUTION_NORMALIZED"
_CANONICAL_EXPORT_RESULT = "EXPORT_NORMALIZED"


def configure_normalization(test_config: dict[str, Any]) -> None:
    """Build normalization replacements from the active test environment config.

    Compares the active config values against canonical (local) values and
    creates replacement pairs for any that differ. This must be called once
    at session start, before any cassettes are recorded.

    IMPORTANT: This module is installed as the ``tests-support`` package.
    When modifying normalization logic, you must clear the tox and uv caches
    so the updated code is picked up by test environments::

        rm -rf packages/gooddata-sdk/.tox
        uv cache clean tests-support --force
    """
    global _normalization_replacements, _password_replacements, _normalization_configured
    replacements: list[tuple[str, str]] = []
    _password_replacements = []

    parsed = urlparse(test_config.get("host", _CANONICAL_HOST))
    active_scheme = parsed.scheme or "http"
    active_hostname = parsed.hostname or _CANONICAL_HOSTNAME
    active_port = parsed.port
    active_org_id = test_config.get("org_id", _CANONICAL_ORG_ID)
    active_org_name = test_config.get("org_name", _CANONICAL_ORG_NAME)
    active_org_hostname = test_config.get("org_hostname", _CANONICAL_HOSTNAME)

    # Build the active host string for URI replacement (e.g. "https://foo.example.com")
    active_host_with_port = f"{active_hostname}:{active_port}" if active_port else active_hostname

    active_origin = f"{active_scheme}://{active_host_with_port}"
    canonical_origin = _CANONICAL_HOST

    # Only add replacements for values that actually differ from canonical.
    # Order matters: add longer/more-specific strings first.

    # Full origin URL: "https://staging.example.com" → "http://localhost:3000"
    if active_origin != canonical_origin:
        replacements.append((active_origin, canonical_origin))

    # Hostname:port (only when the source actually has a port, so it differs
    # from the bare hostname): "staging.example.com:8443" → "localhost:3000"
    if active_port and active_host_with_port != "localhost:3000":
        replacements.append((active_host_with_port, "localhost:3000"))

    # org_hostname (may differ from hostname, e.g. in multi-tenant setups)
    if active_org_hostname != _CANONICAL_HOSTNAME and active_org_hostname != active_hostname:
        replacements.append((active_org_hostname, _CANONICAL_HOSTNAME))

    # Bare hostname: "staging.example.com" → "localhost"
    if active_hostname != _CANONICAL_HOSTNAME:
        replacements.append((active_hostname, _CANONICAL_HOSTNAME))

    # Organization name: "Python SDK Dex" → "Default Organization"
    if active_org_name != _CANONICAL_ORG_NAME:
        replacements.append((active_org_name, _CANONICAL_ORG_NAME))

    # Organization ID: "python-sdk-dex" → "default"
    if active_org_id != _CANONICAL_ORG_ID:
        replacements.append((active_org_id, _CANONICAL_ORG_ID))

    # Data source JDBC URL: staging DB host/name → local DB host/name
    # The server may normalize by appending the default port (:5432), so
    # we add both the with-port and without-port variants.
    active_ds_url = test_config.get("ds_url", _CANONICAL_DS_URL)
    if active_ds_url != _CANONICAL_DS_URL:
        port_variant = re.sub(r"(jdbc:postgresql://[^/?]+)", r"\1:5432", active_ds_url, count=1)
        if port_variant != active_ds_url:
            replacements.append((port_variant, _CANONICAL_DS_URL))
        replacements.append((active_ds_url, _CANONICAL_DS_URL))

    # Data source password: staging password → local password
    # Uses regex (not plain string replacement) to avoid corrupting values
    # that contain the password as a substring (e.g. "client-secret").
    active_ds_password = test_config.get("ds_password", _CANONICAL_DS_PASSWORD)
    if active_ds_password and active_ds_password != _CANONICAL_DS_PASSWORD:
        _ds_password_re = re.compile(
            r'(?<="password": ")' + re.escape(active_ds_password) + r'(?=")'  # JSON
            r"|"
            r"(?<=password: )" + re.escape(active_ds_password) + r"(?=\s|$)"  # YAML
        )
        _password_replacements.append((_ds_password_re, _CANONICAL_DS_PASSWORD))

    # Sort by length descending so longer patterns are replaced first,
    # preventing partial matches from corrupting longer strings.
    replacements.sort(key=lambda pair: len(pair[0]), reverse=True)

    _normalization_replacements = replacements
    _normalization_configured = True


def _apply_replacements(text: str) -> str:
    """Apply all configured normalization replacements to a string."""
    for source, target in _normalization_replacements:
        text = text.replace(source, target)
    for pattern, target in _password_replacements:
        text = pattern.sub(target, text)
    return text


def _normalize_hashes_in_text(text: str) -> str:
    """Replace transient server values with deterministic placeholders."""
    text = _EXEC_HASH_BODY_RE.sub(_CANONICAL_EXECUTION_RESULT, text)
    text = _EXPORT_HASH_BODY_RE.sub(_CANONICAL_EXPORT_RESULT, text)
    text = _CREATED_AT_RE.sub(_CANONICAL_CREATED_AT, text)
    return text


def _normalize_hashes_in_uri(uri: str) -> str:
    """Replace executionResult/exportResult hashes in a request URI."""
    uri = _EXEC_HASH_URI_RE.sub(_CANONICAL_EXECUTION_RESULT, uri)
    uri = _EXPORT_HASH_URI_RE.sub(_CANONICAL_EXPORT_RESULT, uri)
    return uri


def _normalize_body(body: str | None) -> str:
    """Strip environment-specific fields from a JSON request body for matching."""
    if not body:
        return body or ""
    try:
        data = orjson.loads(body)
    except (orjson.JSONDecodeError, TypeError):
        return body

    def _strip(obj: Any) -> Any:
        if isinstance(obj, dict):
            return {k: _strip(v) for k, v in obj.items() if k not in _ENV_SPECIFIC_BODY_FIELDS}
        if isinstance(obj, list):
            return [_strip(item) for item in obj]
        return obj

    return orjson.dumps(_strip(data), option=orjson.OPT_SORT_KEYS).decode("utf-8")


def _body_matcher(r1: Any, r2: Any) -> None:
    """Custom VCR body matcher that ignores environment-specific fields."""
    b1 = _normalize_body(r1.body)
    b2 = _normalize_body(r2.body)
    assert b1 == b2, f"Request bodies differ after normalization:\n{b1}\n!=\n{b2}"


def _noop_matcher(r1: Any, r2: Any) -> None:
    """Always matches — used to disable scheme/host/port matching across environments."""


def get_vcr() -> vcr.VCR:
    gd_vcr = vcr.VCR(
        filter_headers=["authorization", "user-agent"],
        match_on=VCR_MATCH_ON,
        before_record_request=custom_before_request,
        before_record_response=custom_before_response,
        decode_compressed_response=True,
        record_mode=RecordMode.ALL if "OVERWRITE" in os.environ else RecordMode.ONCE,
    )
    gd_vcr.register_matcher("body", _body_matcher)
    # Cassettes recorded against staging must replay in CI (localhost).
    # Disable scheme/host/port matching — path is sufficient.
    for matcher in ("scheme", "host", "port"):
        gd_vcr.register_matcher(matcher, _noop_matcher)

    gd_vcr.register_serializer("custom", CustomSerializerYaml())
    gd_vcr.serializer = "custom"
    return gd_vcr


class IndentDumper(yaml.SafeDumper):
    @typing.no_type_check
    def increase_indent(self, flow: bool = False, indentless: bool = False):
        return super().increase_indent(flow, False)


class CustomSerializerYaml:
    def deserialize(self, cassette_string: str) -> dict[str, Any]:
        cassette_dict = yaml.safe_load(cassette_string)
        for interaction in cassette_dict.get("interactions", []):
            request_body = interaction["request"]["body"]
            response_body = interaction["response"]["body"]
            if request_body is not None:
                if isinstance(request_body, str) and request_body.startswith("<?xml"):
                    interaction["request"]["body"] = request_body
                else:
                    interaction["request"]["body"] = orjson.dumps(request_body).decode("utf-8")
            if response_body is not None and response_body["string"] != "":
                try:
                    if isinstance(response_body["string"], str) and response_body["string"].startswith("<?xml"):
                        interaction["response"]["body"]["string"] = response_body["string"]
                    else:
                        interaction["response"]["body"]["string"] = orjson.dumps(response_body["string"]).decode(
                            "utf-8"
                        )
                except TypeError:
                    # this exception is expected while getting XLSX file content
                    continue
        return cassette_dict

    def serialize(self, cassette_dict: dict[str, Any]) -> str:
        for interaction in cassette_dict.get("interactions", []):
            request_body = interaction["request"]["body"]
            response_body = interaction["response"]["body"]
            if request_body is not None:
                try:
                    interaction["request"]["body"] = orjson.loads(request_body)
                except (orjson.JSONDecodeError, UnicodeDecodeError):
                    # The response can be in XML
                    interaction["request"]["body"] = request_body
            if response_body is not None and response_body["string"] != "":
                try:
                    interaction["response"]["body"]["string"] = orjson.loads(response_body["string"])
                except (orjson.JSONDecodeError, UnicodeDecodeError):
                    # these exceptions are expected while getting file content
                    continue
        return yaml.dump(cassette_dict, Dumper=IndentDumper, sort_keys=True)


def _normalize_uri(uri: str) -> str:
    """Rewrite a request URI to use the canonical host and normalize dynamic hashes."""
    uri = _apply_replacements(uri) if _normalization_replacements else uri
    return _normalize_hashes_in_uri(uri)


def custom_before_request(request, headers_str: str = HEADERS_STR):
    if not _normalization_configured and "OVERWRITE" in os.environ:
        raise RuntimeError(
            "VCR normalization not configured. "
            "Ensure your test fixture depends on 'test_config' (directly or transitively) "
            "so that configure_normalization() runs before cassette recording starts."
        )
    # Normalize URI to canonical host
    request.uri = _normalize_uri(request.uri)

    # Normalize environment-specific values and dynamic hashes in request body
    if request.body:
        if isinstance(request.body, bytes):
            decoded = request.body.decode("utf-8", errors="replace")
            if _normalization_replacements:
                decoded = _apply_replacements(decoded)
            decoded = _normalize_hashes_in_text(decoded)
            request.body = decoded.encode("utf-8")
        elif isinstance(request.body, str):
            if _normalization_replacements:
                request.body = _apply_replacements(request.body)
            request.body = _normalize_hashes_in_text(request.body)

    if hasattr(request, headers_str):
        request.headers = {header: request.headers[header] for header in sorted(request.headers)}
    return request


def custom_before_response(
    response: dict[str, Any],
    headers_str: str = HEADERS_STR,
    non_static_headers: list[str] | None = None,
    placeholder: list[str] | None = None,
):
    if not _normalization_configured and "OVERWRITE" in os.environ:
        raise RuntimeError(
            "VCR normalization not configured. "
            "Ensure your test fixture depends on 'test_config' (directly or transitively) "
            "so that configure_normalization() runs before cassette recording starts."
        )

    if non_static_headers is None:
        non_static_headers = NON_STATIC_HEADERS

    if placeholder is None:
        placeholder = PLACEHOLDER

    if response.get(headers_str) is not None:
        unified_headers = {}
        for header in sorted(response[headers_str]):
            if header in _STRIPPED_RESPONSE_HEADERS:
                continue
            (header, value) = resolve_header(header, non_static_headers, placeholder, response[headers_str])
            # Normalize environment-specific values in header values (e.g. Location)
            if _normalization_replacements and value != placeholder:
                if isinstance(value, list):
                    value = [_apply_replacements(v) if isinstance(v, str) else v for v in value]
                elif isinstance(value, str):
                    value = _apply_replacements(value)
            unified_headers[header] = value
        response[headers_str] = unified_headers

    # Normalize response body: environment-specific values and dynamic hashes
    body = response.get("body")
    if body is not None:
        body_string = body.get("string")
        if body_string:
            if isinstance(body_string, bytes):
                decoded = body_string.decode("utf-8", errors="replace")
                if _normalization_replacements:
                    decoded = _apply_replacements(decoded)
                decoded = _normalize_hashes_in_text(decoded)
                body["string"] = decoded.encode("utf-8")
            elif isinstance(body_string, str):
                if _normalization_replacements:
                    body_string = _apply_replacements(body_string)
                body["string"] = _normalize_hashes_in_text(body_string)

    return response


def resolve_header(header: str, non_static_headers: list[str], placeholder: str, response_headers: dict[str, Any]):
    return (header.upper(), placeholder) if header.upper() in non_static_headers else (header, response_headers[header])
