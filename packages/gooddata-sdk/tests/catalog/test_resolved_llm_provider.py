# (C) 2026 GoodData Corporation
from __future__ import annotations

import pytest
from gooddata_sdk.catalog.workspace.entity_model.resolved_llm_provider import (
    CatalogResolvedLlmModel,
    CatalogResolvedLlmProvider,
)


@pytest.mark.parametrize(
    "scenario, input_data, expected_id, expected_title, expected_model_count",
    [
        (
            "provider_with_models",
            {
                "id": "openai-provider",
                "title": "OpenAI Provider",
                "models": [{"id": "gpt-4o", "family": "OPENAI"}],
            },
            "openai-provider",
            "OpenAI Provider",
            1,
        ),
        (
            "provider_without_models",
            {
                "id": "bedrock-provider",
                "title": "AWS Bedrock Provider",
                "models": [],
            },
            "bedrock-provider",
            "AWS Bedrock Provider",
            0,
        ),
    ],
)
def test_resolved_llm_provider_from_dict(scenario, input_data, expected_id, expected_title, expected_model_count):
    provider = CatalogResolvedLlmProvider.from_dict(input_data)
    assert provider.id == expected_id
    assert provider.title == expected_title
    assert len(provider.models) == expected_model_count


def test_resolved_llm_model_fields():
    model = CatalogResolvedLlmModel(id="gpt-4o", family="OPENAI")
    assert model.id == "gpt-4o"
    assert model.family == "OPENAI"


def test_resolved_llm_provider_models_populated():
    data = {
        "id": "openai-provider",
        "title": "OpenAI Provider",
        "models": [
            {"id": "gpt-4o", "family": "OPENAI"},
            {"id": "gpt-3.5-turbo", "family": "OPENAI"},
        ],
    }
    provider = CatalogResolvedLlmProvider.from_dict(data)
    assert len(provider.models) == 2
    assert provider.models[0].id == "gpt-4o"
    assert provider.models[0].family == "OPENAI"
    assert provider.models[1].id == "gpt-3.5-turbo"
