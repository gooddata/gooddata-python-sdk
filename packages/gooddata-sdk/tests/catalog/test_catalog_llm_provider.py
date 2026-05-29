# (C) 2026 GoodData Corporation
from __future__ import annotations

from unittest.mock import MagicMock

from gooddata_api_client.model.list_llm_provider_models_response import ListLlmProviderModelsResponse
from gooddata_api_client.model.llm_model import LlmModel
from gooddata_api_client.model.model_test_result import ModelTestResult
from gooddata_api_client.model.test_llm_provider_response import TestLlmProviderResponse
from gooddata_sdk import (
    CatalogLlmProviderModel,
    CatalogLlmProviderModelsResult,
    CatalogLlmProviderTestResult,
    CatalogModelTestResult,
    CatalogOpenAiApiKeyAuth,
    CatalogOpenAiProviderConfig,
)
from gooddata_sdk.catalog.organization.service import CatalogOrganizationService


def test_provider_test_result_from_api():
    api_response = TestLlmProviderResponse(
        provider_reachable=True,
        provider_message="ok",
        model_results=[ModelTestResult(model_id="gpt-4o", successful=True, message="ok")],
    )

    result = CatalogLlmProviderTestResult.from_api(api_response)

    assert result.provider_reachable is True
    assert result.provider_message == "ok"
    assert len(result.model_results) == 1
    assert isinstance(result.model_results[0], CatalogModelTestResult)
    assert result.model_results[0].model_id == "gpt-4o"
    assert result.model_results[0].successful is True
    assert result.model_results[0].message == "ok"


def test_provider_models_result_from_api():
    api_response = ListLlmProviderModelsResponse(
        success=True,
        message="ok",
        models=[LlmModel(id="gpt-4o", family="OPENAI")],
    )

    result = CatalogLlmProviderModelsResult.from_api(api_response)

    assert result.success is True
    assert result.message == "ok"
    assert len(result.models) == 1
    assert isinstance(result.models[0], CatalogLlmProviderModel)
    assert result.models[0].id == "gpt-4o"
    assert result.models[0].family == "OPENAI"


def _openai_config():
    return CatalogOpenAiProviderConfig(
        auth=CatalogOpenAiApiKeyAuth(api_key="secret"),
        base_url="https://api.openai.com/v1",
    )


def test_test_llm_provider_maps_response():
    service = CatalogOrganizationService.__new__(CatalogOrganizationService)
    service._actions_api = MagicMock()
    service._actions_api.test_llm_provider.return_value = TestLlmProviderResponse(
        provider_reachable=False,
        provider_message="bad key",
        model_results=[],
    )

    result = service.test_llm_provider(_openai_config())

    assert result.provider_reachable is False
    assert result.provider_message == "bad key"
    # the request body passed to the client carries the provider config discriminator
    sent = service._actions_api.test_llm_provider.call_args.args[0]
    assert sent["provider_config"]["type"] == "OPENAI"


def test_test_llm_provider_by_id_calls_client_with_id():
    service = CatalogOrganizationService.__new__(CatalogOrganizationService)
    service._actions_api = MagicMock()
    service._actions_api.test_llm_provider_by_id.return_value = TestLlmProviderResponse(
        provider_reachable=True,
        provider_message="ok",
        model_results=[],
    )

    result = service.test_llm_provider_by_id("my-provider")

    assert result.provider_reachable is True
    assert service._actions_api.test_llm_provider_by_id.call_args.args[0] == "my-provider"


def test_list_llm_provider_models_maps_response():
    service = CatalogOrganizationService.__new__(CatalogOrganizationService)
    service._actions_api = MagicMock()
    service._actions_api.list_llm_provider_models.return_value = ListLlmProviderModelsResponse(
        success=True,
        message="ok",
        models=[LlmModel(id="gpt-4o", family="OPENAI")],
    )

    result = service.list_llm_provider_models(_openai_config())

    assert result.success is True
    assert result.models[0].id == "gpt-4o"
    sent = service._actions_api.list_llm_provider_models.call_args.args[0]
    assert sent["provider_config"]["type"] == "OPENAI"


def test_list_llm_provider_models_by_id_calls_client_with_id():
    service = CatalogOrganizationService.__new__(CatalogOrganizationService)
    service._actions_api = MagicMock()
    service._actions_api.list_llm_provider_models_by_id.return_value = ListLlmProviderModelsResponse(
        success=True,
        message="ok",
        models=[],
    )

    result = service.list_llm_provider_models_by_id("my-provider")

    assert result.success is True
    assert service._actions_api.list_llm_provider_models_by_id.call_args.args[0] == "my-provider"
