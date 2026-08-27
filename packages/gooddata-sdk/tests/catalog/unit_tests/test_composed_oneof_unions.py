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
"""

from __future__ import annotations

import pytest
from gooddata_api_client.model.json_api_llm_provider_in_attributes_provider_config import (
    JsonApiLlmProviderInAttributesProviderConfig,
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
