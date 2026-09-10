# (C) 2026 GoodData Corporation
from __future__ import annotations

import json
import re
from datetime import datetime, timezone

import httpx
import pytest
from gooddata_eval.core.langfuse.otlp import (
    Span,
    encode_export_request,
    flatten_metadata,
    new_span_id,
    new_trace_id,
    otlp_attribute,
    parse_export_response,
    unix_nano,
)


def test_new_trace_id_is_32_hex_chars():
    trace_id = new_trace_id()
    assert re.fullmatch(r"[0-9a-f]{32}", trace_id)


def test_new_trace_id_is_unique():
    assert new_trace_id() != new_trace_id()


def test_new_span_id_is_16_hex_chars():
    span_id = new_span_id()
    assert re.fullmatch(r"[0-9a-f]{16}", span_id)


def test_new_span_id_is_unique():
    assert new_span_id() != new_span_id()


def test_unix_nano_exact_value_for_known_utc_datetime():
    dt = datetime(2025, 9, 8, 10, 0, 0, tzinfo=timezone.utc)
    assert unix_nano(dt) == "1757325600000000000"


def test_unix_nano_naive_datetime_treated_as_utc():
    naive = datetime(2025, 9, 8, 10, 0, 0)
    aware = datetime(2025, 9, 8, 10, 0, 0, tzinfo=timezone.utc)
    assert unix_nano(naive) == unix_nano(aware)


def test_unix_nano_includes_microsecond_precision():
    dt = datetime(2025, 9, 8, 10, 0, 0, 400000, tzinfo=timezone.utc)
    assert unix_nano(dt) == "1757325600400000000"


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (True, {"boolValue": True}),
        (False, {"boolValue": False}),
        (42, {"intValue": "42"}),
        (0, {"intValue": "0"}),
        (0.5, {"doubleValue": 0.5}),
        ("hello", {"stringValue": "hello"}),
    ],
)
def test_otlp_attribute_typing_table(value, expected):
    attr = otlp_attribute("k", value)
    assert attr == {"key": "k", "value": expected}


def test_otlp_attribute_bool_checked_before_int():
    # bool is an int subclass; must map to boolValue, not intValue
    attr = otlp_attribute("k", True)
    assert attr["value"] == {"boolValue": True}


def test_otlp_attribute_list_of_str_is_array_value():
    attr = otlp_attribute("k", ["a", "b"])
    assert attr == {"key": "k", "value": {"arrayValue": {"values": [{"stringValue": "a"}, {"stringValue": "b"}]}}}


def test_otlp_attribute_dict_is_json_string():
    attr = otlp_attribute("k", {"a": 1})
    assert attr["value"]["stringValue"] == json.dumps({"a": 1}, default=str)


def test_flatten_metadata_skips_none_values():
    attrs = flatten_metadata("prefix", {"a": None, "b": "x"})
    assert attrs == [{"key": "prefix.b", "value": {"stringValue": "x"}}]


def test_flatten_metadata_types_scalars():
    attrs = flatten_metadata("prefix", {"n": 3, "f": 1.5, "flag": True})
    assert {"key": "prefix.n", "value": {"intValue": "3"}} in attrs
    assert {"key": "prefix.f", "value": {"doubleValue": 1.5}} in attrs
    assert {"key": "prefix.flag", "value": {"boolValue": True}} in attrs


def test_flatten_metadata_nested_dict_is_json_string():
    attrs = flatten_metadata("prefix", {"nested": {"x": 1}})
    assert attrs == [{"key": "prefix.nested", "value": {"stringValue": json.dumps({"x": 1}, default=str)}}]


def test_flatten_metadata_nested_list_is_json_string():
    attrs = flatten_metadata("prefix", {"items": ["a", "b"]})
    assert attrs == [{"key": "prefix.items", "value": {"stringValue": json.dumps(["a", "b"], default=str)}}]


def test_flatten_metadata_empty_mapping():
    assert flatten_metadata("prefix", {}) == []
    assert flatten_metadata("prefix", None) == []


def test_encode_export_request_shape():
    span = Span(
        trace_id="3f2a9c1e8b7d4e6f9a0b1c2d3e4f5a6b",
        span_id="9a0b1c2d3e4f5a6b",
        name="gd-eval: Show revenue by month",
        start=datetime(2025, 9, 8, 10, 0, 0, tzinfo=timezone.utc),
        end=datetime(2025, 9, 8, 10, 0, 18, 400000, tzinfo=timezone.utc),
        attributes=[{"key": "langfuse.observation.type", "value": {"stringValue": "span"}}],
    )
    request = encode_export_request([span])

    resource_spans = request["resourceSpans"]
    assert len(resource_spans) == 1
    resource = resource_spans[0]["resource"]
    assert resource["attributes"] == [{"key": "service.name", "value": {"stringValue": "gooddata-eval"}}]

    scope_spans = resource_spans[0]["scopeSpans"]
    assert len(scope_spans) == 1
    assert scope_spans[0]["scope"]["name"] == "gooddata-eval"
    assert re.fullmatch(r"\d+\.\d+\.\d+", scope_spans[0]["scope"]["version"])

    (otlp_span,) = scope_spans[0]["spans"]
    assert otlp_span["traceId"] == span.trace_id
    assert otlp_span["spanId"] == span.span_id
    assert otlp_span["kind"] == 1
    assert otlp_span["status"] == {"code": 1}
    assert otlp_span["startTimeUnixNano"].isdigit()
    assert otlp_span["endTimeUnixNano"].isdigit()
    assert int(otlp_span["startTimeUnixNano"]) <= int(otlp_span["endTimeUnixNano"])
    assert otlp_span["attributes"] == span.attributes


def test_encode_export_request_custom_scope():
    span = Span(
        trace_id="a" * 32,
        span_id="b" * 16,
        name="s",
        start=datetime(2025, 1, 1, tzinfo=timezone.utc),
        end=datetime(2025, 1, 1, tzinfo=timezone.utc),
        attributes=[],
    )
    request = encode_export_request([span], scope_name="custom-scope", scope_version="9.9.9")
    scope = request["resourceSpans"][0]["scopeSpans"][0]["scope"]
    assert scope == {"name": "custom-scope", "version": "9.9.9"}


def test_parse_export_response_ok_empty_body():
    resp = httpx.Response(200, json={})
    assert parse_export_response(resp) is None


def test_parse_export_response_ok_no_content():
    resp = httpx.Response(200)
    assert parse_export_response(resp) is None


def test_parse_export_response_partial_success_raises():
    resp = httpx.Response(200, json={"partialSuccess": {"rejectedSpans": 1, "errorMessage": "bad span"}})
    with pytest.raises(RuntimeError, match="bad span"):
        parse_export_response(resp)


def test_parse_export_response_partial_success_string_count_raises():
    # OTLP/JSON encodes int64 fields as decimal strings.
    resp = httpx.Response(200, json={"partialSuccess": {"rejectedSpans": "1", "errorMessage": "bad span"}})
    with pytest.raises(RuntimeError, match="bad span"):
        parse_export_response(resp)


def test_parse_export_response_partial_success_zero_rejected_ok():
    resp = httpx.Response(200, json={"partialSuccess": {"rejectedSpans": 0}})
    assert parse_export_response(resp) is None


def test_parse_export_response_ok_non_json_body():
    resp = httpx.Response(200, text="not json")
    assert parse_export_response(resp) is None


def test_parse_export_response_non_2xx_raises():
    resp = httpx.Response(400, text="bad request")
    with pytest.raises(RuntimeError, match="400"):
        parse_export_response(resp)
