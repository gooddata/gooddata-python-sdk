# (C) 2026 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

from gooddata_sdk import (
    CatalogResolvedLlmModel,
    CatalogResolvedLlmProvider,
    CatalogResolvedLlms,
    GoodDataSdk,
)
from tests_support.vcrpy_utils import get_vcr

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures" / "workspace_content"


# --- Unit tests ---


def test_resolved_llm_model_from_dict():
    data = {"id": "gpt-4o", "family": "OPENAI"}
    model = CatalogResolvedLlmModel(id=data["id"], family=data["family"])
    assert model.id == "gpt-4o"
    assert model.family == "OPENAI"


def test_resolved_llm_provider_from_api():
    raw = {
        "id": "my_provider",
        "title": "My Provider",
        "models": [
            {"id": "gpt-4o", "family": "OPENAI"},
        ],
    }
    provider = CatalogResolvedLlmProvider.from_api(raw)
    assert provider.id == "my_provider"
    assert provider.title == "My Provider"
    assert len(provider.models) == 1
    assert provider.models[0].id == "gpt-4o"
    assert provider.models[0].family == "OPENAI"


def test_resolved_llms_from_api_with_data():
    raw_response = {
        "data": {
            "id": "my_provider",
            "title": "My Provider",
            "models": [{"id": "gpt-4o", "family": "OPENAI"}],
        }
    }
    result = CatalogResolvedLlms.from_api(raw_response)
    assert result.data is not None
    assert result.data.id == "my_provider"
    assert result.data.title == "My Provider"
    assert len(result.data.models) == 1


def test_resolved_llms_from_api_no_data():
    raw_response = {"data": None}
    result = CatalogResolvedLlms.from_api(raw_response)
    assert result.data is None


def test_resolved_llms_from_api_missing_data_key():
    raw_response = {}
    result = CatalogResolvedLlms.from_api(raw_response)
    assert result.data is None


def test_resolve_llm_providers_calls_actions_api():
    """Verify that resolve_llm_providers calls the correct actions API method."""
    mock_client = MagicMock()
    mock_actions_api = MagicMock()
    mock_client.actions_api = mock_actions_api
    mock_client.entities_api = MagicMock()
    mock_client.layout_api = MagicMock()
    mock_client.user_management_api = MagicMock()

    from gooddata_sdk.catalog.workspace.content_service import CatalogWorkspaceContentService

    service = CatalogWorkspaceContentService(mock_client)

    # Mock the API response as a dict with no data
    mock_actions_api.resolve_llm_providers.return_value = {"data": None}

    result = service.resolve_llm_providers("test_workspace")

    mock_actions_api.resolve_llm_providers.assert_called_once_with("test_workspace", _check_return_type=False)
    assert isinstance(result, CatalogResolvedLlms)
    assert result.data is None


# --- Integration tests ---


@gd_vcr.use_cassette(str(_fixtures_dir / "test_resolve_llm_providers.yaml"))
def test_resolve_llm_providers_integration(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    result = sdk.catalog_workspace_content.resolve_llm_providers(test_config["workspace"])
    assert isinstance(result, CatalogResolvedLlms)
    # data may be None if no LLM provider is configured
    if result.data is not None:
        assert isinstance(result.data, CatalogResolvedLlmProvider)
        assert result.data.id
        assert result.data.title
        for model in result.data.models:
            assert isinstance(model, CatalogResolvedLlmModel)
            assert model.id
            assert model.family
