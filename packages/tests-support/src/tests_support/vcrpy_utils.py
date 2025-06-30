# (C) 2022 GoodData Corporation
from __future__ import annotations

import json
import typing
from json import JSONDecodeError
from typing import Any, Optional

import vcr
import yaml

VCR_MATCH_ON = ("method", "scheme", "host", "port", "path", "query", "body")
NON_STATIC_HEADERS = ["DATE", "X-GDC-TRACE-ID"]
HEADERS_STR = "headers"
PLACEHOLDER = ["PLACEHOLDER"]


def get_vcr() -> vcr.VCR:
    gd_vcr = vcr.VCR(
        filter_headers=["authorization", "user-agent"],
        match_on=VCR_MATCH_ON,
        before_record_request=custom_before_request,
        before_record_response=custom_before_response,
        decode_compressed_response=True,
    )

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
        return yaml.dump(cassette_dict, Dumper=IndentDumper, sort_keys=False)


def custom_before_request(request, headers_str: str = HEADERS_STR):
    if hasattr(request, headers_str):
        request.headers = {header: request.headers[header] for header in sorted(request.headers)}
    return request


def custom_before_response(
    response: dict[str, Any],
    headers_str: str = HEADERS_STR,
    non_static_headers: Optional[list[str]] = None,
    placeholder: Optional[list[str]] = None,
):
    if non_static_headers is None:
        non_static_headers = NON_STATIC_HEADERS

    if placeholder is None:
        placeholder = PLACEHOLDER

    if response.get(headers_str) is not None:
        unified_headers = {}
        for header in sorted(response[headers_str]):
            (header, value) = resolve_header(header, non_static_headers, placeholder, response[headers_str])
            unified_headers[header] = value
        response[headers_str] = unified_headers
    return response


def resolve_header(header: str, non_static_headers: list[str], placeholder: str, response_headers: dict[str, Any]):
    return (header.upper(), placeholder) if header.upper() in non_static_headers else (header, response_headers[header])
