# (C) 2026 GoodData Corporation
from __future__ import annotations

import pytest
from gooddata_sdk import (
    CatalogResolvedLlmEndpoint,
    CatalogResolvedLlmModelItem,
    CatalogResolvedLlmProvider,
    CatalogResolvedLlms,
)


class TestCatalogResolvedLlms:
    """Unit tests for ResolvedLlm model classes — no network I/O required."""

    def test_from_api_no_data(self):
        """data=None means no LLM is configured."""
        result = CatalogResolvedLlms.from_api({"data": None})
        assert result.data is None

    def test_from_api_missing_data_key(self):
        """Absent 'data' key is treated the same as None."""
        result = CatalogResolvedLlms.from_api({})
        assert result.data is None

    def test_from_api_endpoint(self):
        """When data has no 'models' key it is parsed as a CatalogResolvedLlmEndpoint."""
        payload = {
            "data": {
                "id": "my-endpoint",
                "title": "My Endpoint",
            }
        }
        result = CatalogResolvedLlms.from_api(payload)
        assert isinstance(result.data, CatalogResolvedLlmEndpoint)
        assert result.data.id == "my-endpoint"
        assert result.data.title == "My Endpoint"

    def test_from_api_provider(self):
        """When data contains a 'models' key it is parsed as a CatalogResolvedLlmProvider."""
        payload = {
            "data": {
                "id": "my-provider",
                "title": "My Provider",
                "models": [{"id": "gpt-4", "family": "OPENAI"}],
            }
        }
        result = CatalogResolvedLlms.from_api(payload)
        assert isinstance(result.data, CatalogResolvedLlmProvider)
        assert result.data.id == "my-provider"
        assert result.data.title == "My Provider"
        assert len(result.data.models) == 1
        model = result.data.models[0]
        assert isinstance(model, CatalogResolvedLlmModelItem)
        assert model.id == "gpt-4"
        assert model.family == "OPENAI"

    def test_from_api_provider_empty_models(self):
        """Provider with an empty models list is still parsed as CatalogResolvedLlmProvider."""
        payload = {
            "data": {
                "id": "provider-no-models",
                "title": "Provider",
                "models": [],
            }
        }
        result = CatalogResolvedLlms.from_api(payload)
        assert isinstance(result.data, CatalogResolvedLlmProvider)
        assert result.data.models == []

    @pytest.mark.parametrize(
        "scenario, payload, expected_type",
        [
            (
                "endpoint",
                {"data": {"id": "ep", "title": "EP"}},
                CatalogResolvedLlmEndpoint,
            ),
            (
                "provider",
                {"data": {"id": "prov", "title": "Prov", "models": []}},
                CatalogResolvedLlmProvider,
            ),
        ],
    )
    def test_from_api_type_dispatch(self, scenario, payload, expected_type):
        result = CatalogResolvedLlms.from_api(payload)
        assert isinstance(result.data, expected_type), f"scenario={scenario}"
