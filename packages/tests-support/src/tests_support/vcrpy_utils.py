# (C) 2022 GoodData Corporation
from __future__ import annotations

import json
import os
import typing
from json import JSONDecodeError
from typing import Any
from urllib.parse import urlparse

import vcr
import yaml
from vcr.record_mode import RecordMode

VCR_MATCH_ON = ("method", "path", "query", "body")
NON_STATIC_HEADERS = ["DATE", "X-GDC-CANCEL-TOKEN", "X-GDC-TRACE-ID"]
HEADERS_STR = "headers"
PLACEHOLDER = ["PLACEHOLDER"]

# Fields stripped from request bodies before VCR body matching.
# These differ between local and staging environments but don't affect
# the logical identity of a request.
_ENV_SPECIFIC_BODY_FIELDS = {"password", "token", "url", "username", "privateKey"}

# Canonical (local) values — cassettes always use these.
_CANONICAL_HOST = "http://localhost:3000"
_CANONICAL_HOSTNAME = "localhost"
_CANONICAL_ORG_ID = "default"
_CANONICAL_ORG_NAME = "Default Organization"

# Module-level normalization state.
# Populated by configure_normalization() before tests run.
# Each entry is (source_string, replacement_string).
# Ordered longest-first so more specific patterns match before substrings.
_normalization_replacements: list[tuple[str, str]] = []


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
    global _normalization_replacements
    replacements: list[tuple[str, str]] = []

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

    # Sort by length descending so longer patterns are replaced first,
    # preventing partial matches from corrupting longer strings.
    replacements.sort(key=lambda pair: len(pair[0]), reverse=True)

    _normalization_replacements = replacements


def _apply_replacements(text: str) -> str:
    """Apply all configured normalization replacements to a string."""
    for source, target in _normalization_replacements:
        text = text.replace(source, target)
    return text


def _normalize_body(body: str | None) -> str:
    """Strip environment-specific fields from a JSON request body for matching."""
    if not body:
        return body or ""
    try:
        data = json.loads(body)
    except (JSONDecodeError, TypeError):
        return body

    def _strip(obj: Any) -> Any:
        if isinstance(obj, dict):
            return {k: _strip(v) for k, v in obj.items() if k not in _ENV_SPECIFIC_BODY_FIELDS}
        if isinstance(obj, list):
            return [_strip(item) for item in obj]
        return obj

    return json.dumps(_strip(data), sort_keys=True)


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
                    interaction["request"]["body"] = json.dumps(request_body)
            if response_body is not None and response_body["string"] != "":
                try:
                    if isinstance(response_body["string"], str) and response_body["string"].startswith("<?xml"):
                        interaction["response"]["body"]["string"] = response_body["string"]
                    else:
                        interaction["response"]["body"]["string"] = json.dumps(response_body["string"])
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
                    interaction["request"]["body"] = json.loads(request_body)
                except (JSONDecodeError, UnicodeDecodeError):
                    # The response can be in XML
                    interaction["request"]["body"] = request_body
            if response_body is not None and response_body["string"] != "":
                try:
                    interaction["response"]["body"]["string"] = json.loads(response_body["string"])
                except (JSONDecodeError, UnicodeDecodeError):
                    # these exceptions are expected while getting file content
                    continue
        return yaml.dump(cassette_dict, Dumper=IndentDumper, sort_keys=True)


def _normalize_uri(uri: str) -> str:
    """Rewrite a request URI to use the canonical host."""
    if not _normalization_replacements:
        return uri
    return _apply_replacements(uri)


def custom_before_request(request, headers_str: str = HEADERS_STR):
    # Normalize URI to canonical host
    request.uri = _normalize_uri(request.uri)

    # Normalize environment-specific values in request body
    if _normalization_replacements and request.body:
        if isinstance(request.body, bytes):
            request.body = _apply_replacements(request.body.decode("utf-8", errors="replace")).encode("utf-8")
        elif isinstance(request.body, str):
            request.body = _apply_replacements(request.body)

    if hasattr(request, headers_str):
        request.headers = {header: request.headers[header] for header in sorted(request.headers)}
    return request


def custom_before_response(
    response: dict[str, Any],
    headers_str: str = HEADERS_STR,
    non_static_headers: list[str] | None = None,
    placeholder: list[str] | None = None,
):
    if non_static_headers is None:
        non_static_headers = NON_STATIC_HEADERS

    if placeholder is None:
        placeholder = PLACEHOLDER

    if response.get(headers_str) is not None:
        unified_headers = {}
        for header in sorted(response[headers_str]):
            (header, value) = resolve_header(header, non_static_headers, placeholder, response[headers_str])
            # Normalize environment-specific values in header values (e.g. Location)
            if _normalization_replacements and value != placeholder:
                if isinstance(value, list):
                    value = [_apply_replacements(v) if isinstance(v, str) else v for v in value]
                elif isinstance(value, str):
                    value = _apply_replacements(value)
            unified_headers[header] = value
        response[headers_str] = unified_headers

    # Normalize environment-specific values in response body
    if _normalization_replacements:
        body = response.get("body")
        if body is not None:
            body_string = body.get("string")
            if body_string:
                if isinstance(body_string, bytes):
                    body["string"] = _apply_replacements(body_string.decode("utf-8", errors="replace")).encode("utf-8")
                elif isinstance(body_string, str):
                    body["string"] = _apply_replacements(body_string)

    return response


def resolve_header(header: str, non_static_headers: list[str], placeholder: str, response_headers: dict[str, Any]):
    return (header.upper(), placeholder) if header.upper() in non_static_headers else (header, response_headers[header])
