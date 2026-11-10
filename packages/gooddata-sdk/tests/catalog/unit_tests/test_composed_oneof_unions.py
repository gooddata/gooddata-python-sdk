# (C) 2026 GoodData Corporation
"""Regression tests for oneOf/anyOf unions in the generated api client.

openapi-generator's `python-prior` generator flattens a `oneOf`'s members into
the composed parent model, but for a property that several members declare it
keeps only the **last** member's value:

- `allowed_values[('type',)]` ends up holding one member's enum, so the parent
  accepts exactly one variant - and which one depends on the order of the
  `oneOf` array in the OpenAPI document.
- `openapi_types[prop]` ends up holding one member's class, so a nested union
  such as an LLM provider's `auth` cannot carry the other members' payloads.

`model_utils` (via the `model_utils.mustache` / `method_set_attribute.mustache`
custom templates) widens both back to the union of the members. These tests pin
that behaviour for the LLM provider config - the instance this was reported
against - so a template or generator change cannot silently reintroduce it.

The defect was repo-wide (25 collapsed enums and 47 collapsed types across 161
composed models), so it is worth suspecting whenever a `oneOf` variant is
inexplicably rejected.

A `oneOf` of primitive members only (`number|string`, `boolean|string`,
`integer|string`) is a different case: the generator emits an empty model class
for it. The custom templates mark such a class with its member types, and
`model_utils` validates the property against those members and keeps the value
as it is. The tests at the end of this module pin that for every such union.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass, field
from types import SimpleNamespace
from typing import Any

import pytest
from gooddata_api_client.api_client import ApiClient
from gooddata_api_client.exceptions import ApiTypeError, ApiValueError
from gooddata_api_client.model.anomaly_detection_request import AnomalyDetectionRequest
from gooddata_api_client.model.column_location import ColumnLocation
from gooddata_api_client.model.conditional_formatting_literal_value import ConditionalFormattingLiteralValue
from gooddata_api_client.model.dashboard_date_filter_date_filter import DashboardDateFilterDateFilter
from gooddata_api_client.model.declarative_publisher_document_page_template import (
    DeclarativePublisherDocumentPageTemplate,
)
from gooddata_api_client.model.json_api_llm_provider_in_attributes_provider_config import (
    JsonApiLlmProviderInAttributesProviderConfig,
)
from gooddata_api_client.model.publisher_document_area_style import PublisherDocumentAreaStyle
from gooddata_api_client.model.publisher_document_auto_visibility import PublisherDocumentAutoVisibility
from gooddata_api_client.model.publisher_document_container_style import PublisherDocumentContainerStyle
from gooddata_api_client.model.publisher_document_date_filter_date_filter import (
    PublisherDocumentDateFilterDateFilter,
)
from gooddata_api_client.model_utils import (
    composed_union_allowed_values,
    composed_union_types,
)
from gooddata_sdk import (
    CatalogAwsBedrockProviderConfig,
    CatalogAzureFoundryApiKeyAuth,
    CatalogAzureFoundryProviderConfig,
    CatalogBedrockAccessKeyAuth,
    CatalogLlmProvider,
    CatalogLlmProviderModel,
    CatalogOpenAiApiKeyAuth,
    CatalogOpenAiProviderConfig,
)

PROVIDER_CONFIGS = {
    "OPENAI": (
        CatalogOpenAiProviderConfig(
            auth=CatalogOpenAiApiKeyAuth(api_key="dummy"),
            base_url="https://api.openai.com/v1",
            organization="org-1",
        ),
        {
            "type": "OPENAI",
            "base_url": "https://api.openai.com/v1",
            "organization": "org-1",
            "auth": {"type": "API_KEY", "api_key": "dummy"},
        },
    ),
    "AWS_BEDROCK": (
        CatalogAwsBedrockProviderConfig(
            auth=CatalogBedrockAccessKeyAuth(access_key_id="akid", secret_access_key="secret", session_token="token"),
            region="us-east-1",
        ),
        {
            "type": "AWS_BEDROCK",
            "region": "us-east-1",
            "auth": {
                "type": "ACCESS_KEY",
                "access_key_id": "akid",
                "secret_access_key": "secret",
                "session_token": "token",
            },
        },
    ),
    "AZURE_FOUNDRY": (
        CatalogAzureFoundryProviderConfig(
            auth=CatalogAzureFoundryApiKeyAuth(api_key="dummy"),
            endpoint="https://example.openai.azure.com",
        ),
        {
            "type": "AZURE_FOUNDRY",
            "endpoint": "https://example.openai.azure.com",
            "auth": {"type": "API_KEY", "api_key": "dummy"},
        },
    ),
}


@pytest.mark.parametrize("provider_type", sorted(PROVIDER_CONFIGS))
def test_llm_provider_to_api_accepts_every_provider_config(provider_type: str) -> None:
    """Every provider variant must survive `to_api()`, not just the flattened one."""
    provider_config, expected = PROVIDER_CONFIGS[provider_type]
    provider = CatalogLlmProvider.init(
        id=f"test-{provider_type.lower()}",
        models=[CatalogLlmProviderModel(id="model-1", family="OPENAI")],
        provider_config=provider_config,
        name=f"Test {provider_type}",
        default_model_id="model-1",
    )

    api_object = provider.to_api()

    assert api_object.to_dict()["attributes"]["provider_config"] == expected


@pytest.mark.parametrize("provider_type", sorted(PROVIDER_CONFIGS))
def test_llm_provider_round_trips_through_from_api(provider_type: str) -> None:
    provider_config, _ = PROVIDER_CONFIGS[provider_type]
    provider = CatalogLlmProvider.init(
        id=f"test-{provider_type.lower()}",
        models=[CatalogLlmProviderModel(id="model-1", family="OPENAI")],
        provider_config=provider_config,
        name=f"Test {provider_type}",
        default_model_id="model-1",
    )

    restored = CatalogLlmProvider.from_api(provider.to_dict())

    assert restored.attributes is not None
    assert restored.attributes.provider_config is not None
    assert restored.attributes.provider_config.type == provider_type


def _oneof_members(model):
    return model._composed_schemas["oneOf"]


def test_provider_config_type_enum_is_the_union_of_its_members() -> None:
    """The parent's effective enum covers every member, not just the flattened one.

    Asserted against the members themselves rather than a hardcoded list, so
    adding a provider to the OpenAPI document does not need a test edit.
    """
    model = JsonApiLlmProviderInAttributesProviderConfig
    per_member = {frozenset(member.allowed_values.get(("type",), {})) for member in _oneof_members(model)}
    expected = frozenset().union(*per_member)

    effective = frozenset(composed_union_allowed_values(model, "type"))

    assert effective == expected
    # Each member contributes its own single value, so a union of more than one
    # is what makes this meaningful - and the generator wrote only one of them
    # onto the parent.
    assert len(expected) > 1
    assert frozenset(model.allowed_values.get(("type",), {})) < effective


def test_provider_config_auth_accepts_every_members_auth_class() -> None:
    """`auth` is a nested union; the flattened parent kept only one auth class."""
    model = JsonApiLlmProviderInAttributesProviderConfig
    expected = {t for member in _oneof_members(model) for t in member.openapi_types.get("auth", ())}

    effective = set(composed_union_types(model, "auth"))

    assert effective == expected
    assert len(expected) > 1
    assert set(model.openapi_types.get("auth", ())) < effective


@pytest.mark.parametrize(
    "union_helper",
    [composed_union_types, composed_union_allowed_values],
    ids=["types", "allowed_values"],
)
def test_union_helpers_tolerate_a_non_model_member(union_helper, monkeypatch) -> None:
    """A composed member is not always a model, and primitives have no metadata.

    `oneOf: [$ref, {type: string}]` makes the generator emit
    `'oneOf': [Thing, str]`. Reading `openapi_types` / `allowed_values` straight
    off such a member raises AttributeError, which would break every attribute
    assignment on that model rather than just the union widening.
    """
    model = JsonApiLlmProviderInAttributesProviderConfig
    with_primitive = dict(model._composed_schemas)
    with_primitive["oneOf"] = tuple(with_primitive["oneOf"]) + (str,)
    monkeypatch.setattr(model, "_composed_schemas", with_primitive)

    # Must not raise, and must still report what the real members declare.
    assert union_helper(model, "type")


_TEXT = {"type": "text", "id": "t1", "markdown": "Hello"}
_ROW = {"type": "row", "children": [_TEXT]}
_COLUMN = {"type": "column", "children": [_TEXT, _ROW]}


def _page_template_from_python_names(layout: dict[str, Any]) -> DeclarativePublisherDocumentPageTemplate:
    """Builds a page template the way `Base.to_api()` does: python names, `camel_case=False`."""
    return DeclarativePublisherDocumentPageTemplate.from_dict(
        {"id": "pt", "title": "PT", "version": "1", "content": {"layout": layout}},
        camel_case=False,
    )


@pytest.mark.parametrize("layout", [_TEXT, _ROW, _COLUMN], ids=["text", "row", "column"])
def test_layout_node_resolves_from_python_names(layout: dict[str, Any]) -> None:
    """A discriminated composed model must dispatch on `type`, not try every member.

    `PublisherDocumentLayoutNode` is a `oneOf` with a `type` discriminator. Built
    from python names, it must resolve to the member `type` names; trying the
    members in turn fails on the first one whose required arguments are missing.
    """
    template = _page_template_from_python_names(layout)

    assert template.to_dict(camel_case=True)["content"]["layout"] == layout


def test_text_layout_node_keeps_its_fields_from_python_names() -> None:
    template = _page_template_from_python_names(_TEXT)

    assert template.content.layout.markdown == "Hello"


def test_nested_layout_nodes_resolve_from_python_names() -> None:
    template = _page_template_from_python_names(_COLUMN)

    text, row = template.content.layout.children
    assert text.markdown == "Hello"
    assert row.children[0].markdown == "Hello"


def test_image_layout_node_maps_python_names_to_json_names() -> None:
    template = _page_template_from_python_names({"type": "image", "id": "i1", "alt_text": "A chart"})

    layout = template.to_dict(camel_case=True)["content"]["layout"]
    assert layout == {"type": "image", "id": "i1", "altText": "A chart"}


@dataclass(frozen=True)
class _PrimitiveUnionSite:
    """A property typed by a primitive-only `oneOf`, on a model that hosts it."""

    model: type
    python_name: str
    json_name: str
    members: tuple[Any, ...]
    non_members: tuple[Any, ...]
    required: dict[str, Any] = field(default_factory=dict)


_NUMBER_OR_STRING = (20, 4.5, "{theme.spacing.gap.normal}", "")
_NOT_NUMBER_OR_STRING = ({"a": 1}, [1], True)

_PRIMITIVE_UNION_SITES = {
    "style-gap": _PrimitiveUnionSite(
        PublisherDocumentAreaStyle, "gap", "gap", _NUMBER_OR_STRING, _NOT_NUMBER_OR_STRING
    ),
    "style-padding": _PrimitiveUnionSite(
        PublisherDocumentContainerStyle, "padding", "padding", _NUMBER_OR_STRING, _NOT_NUMBER_OR_STRING
    ),
    "style-border-radius": _PrimitiveUnionSite(
        PublisherDocumentContainerStyle, "border_radius", "borderRadius", _NUMBER_OR_STRING, _NOT_NUMBER_OR_STRING
    ),
    "auto-visibility": _PrimitiveUnionSite(
        PublisherDocumentAutoVisibility, "visible", "visible", (True, False, "auto", ""), ({"a": 1}, [1], 20, 1.5)
    ),
    "publisher-date-filter-from": _PrimitiveUnionSite(
        PublisherDocumentDateFilterDateFilter,
        "_from",
        "from",
        (-3, 0.5, "2020-01-01"),
        _NOT_NUMBER_OR_STRING,
        {"granularity": "GDC.time.month", "type": "relative"},
    ),
    "dashboard-date-filter-from": _PrimitiveUnionSite(
        DashboardDateFilterDateFilter,
        "_from",
        "from",
        (-3, "2020-01-01"),
        ({"a": 1}, [1], True, 1.5),
        {"granularity": "GDC.time.month", "type": "relative"},
    ),
    "conditional-formatting-literal": _PrimitiveUnionSite(
        ConditionalFormattingLiteralValue,
        "value",
        "value",
        _NUMBER_OR_STRING,
        _NOT_NUMBER_OR_STRING,
        {"kind": "literal"},
    ),
}

_MEMBER_CASES = [
    pytest.param(site, value, id=f"{name}-{value!r}")
    for name, site in _PRIMITIVE_UNION_SITES.items()
    for value in site.members
]
_WRONG_CASES = [
    pytest.param(site, value, id=f"{name}-{value!r}")
    for name, site in _PRIMITIVE_UNION_SITES.items()
    for value in site.non_members
]


def _deserialize(body: dict[str, Any], model: type) -> Any:
    """Deserializes `body` the way `ApiClient` deserializes a response."""
    return ApiClient().deserialize(SimpleNamespace(data=json.dumps(body)), (model,), True)


def _assert_kept(actual: Any, expected: Any) -> None:
    assert type(actual) is type(expected)
    assert actual == expected


@pytest.mark.parametrize(("site", "value"), _MEMBER_CASES)
def test_primitive_union_member_survives_response_deserialization(site: _PrimitiveUnionSite, value: Any) -> None:
    """A member value from the wire is kept as it is: `20` stays an int, a string stays a string."""
    model = _deserialize({**site.required, site.json_name: value}, site.model)

    _assert_kept(model.to_dict()[site.python_name], value)
    _assert_kept(ApiClient.sanitize_for_serialization(model)[site.json_name], value)


@pytest.mark.parametrize(("site", "value"), _MEMBER_CASES)
def test_primitive_union_member_survives_the_constructor(site: _PrimitiveUnionSite, value: Any) -> None:
    model = site.model(**site.required, **{site.python_name: value})

    _assert_kept(model.to_dict()[site.python_name], value)
    _assert_kept(ApiClient.sanitize_for_serialization(model)[site.json_name], value)


def _assert_rejected_as_wrong_type(build: Callable[[], Any]) -> None:
    """Asserts `build` fails on an `ApiTypeError`.

    A composed host such as `ConditionalFormattingLiteralValue` wraps the type
    error of its `allOf` member in an `ApiValueError`, so the cause chain is
    searched rather than the outermost exception alone.
    """
    with pytest.raises((ApiTypeError, ApiValueError)) as info:
        build()
    error: BaseException | None = info.value
    while error is not None and not isinstance(error, ApiTypeError):
        error = error.__cause__
    assert isinstance(error, ApiTypeError)


@pytest.mark.parametrize(("site", "value"), _WRONG_CASES)
def test_primitive_union_rejects_a_wrong_type_in_a_response(site: _PrimitiveUnionSite, value: Any) -> None:
    _assert_rejected_as_wrong_type(lambda: _deserialize({**site.required, site.json_name: value}, site.model))


@pytest.mark.parametrize(("site", "value"), _WRONG_CASES)
def test_primitive_union_rejects_a_wrong_type_in_the_constructor(site: _PrimitiveUnionSite, value: Any) -> None:
    _assert_rejected_as_wrong_type(lambda: site.model(**site.required, **{site.python_name: value}))


def test_number_property_outside_a_union_still_upconverts_an_int() -> None:
    model = _deserialize({"sensitivity": 2}, AnomalyDetectionRequest)

    _assert_kept(model.sensitivity, 2.0)


def test_empty_object_model_still_accepts_a_free_form_object() -> None:
    body = {"a": {"x": 1}, "b": [1, "two"]}

    model = _deserialize(body, ColumnLocation)

    assert model.to_dict() == body
