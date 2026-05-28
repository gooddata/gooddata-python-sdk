# (C) 2026 GoodData Corporation
"""Unit tests for LLM provider SDK-side deserialization logic.

These tests cover the branching logic in _provider_config_from_api and
the from_api path for CatalogLlmProvider. They run without a live stack
or VCR cassettes and exercise only the SDK layer.
"""

from __future__ import annotations

from gooddata_api_client.model.anthropic_provider_auth import AnthropicProviderAuth
from gooddata_api_client.model.anthropic_provider_config import AnthropicProviderConfig
from gooddata_sdk.catalog.organization.entity_model.llm_provider import (
    CatalogAnthropicApiKeyAuth,
    CatalogAnthropicProviderConfig,
    CatalogAwsBedrockProviderConfig,
    CatalogAzureFoundryProviderConfig,
    CatalogBedrockAccessKeyAuth,
    CatalogLlmProvider,
    CatalogOpenAiApiKeyAuth,
    CatalogOpenAiProviderConfig,
    _provider_config_from_api,
)


class TestProviderConfigFromApi:
    """Tests for _provider_config_from_api branching logic."""

    def test_anthropic_api_key_auth(self) -> None:
        data = {"type": "ANTHROPIC", "auth": {"type": "API_KEY"}}
        config = _provider_config_from_api(data)
        assert isinstance(config, CatalogAnthropicProviderConfig)
        assert config.type == "ANTHROPIC"
        assert isinstance(config.auth, CatalogAnthropicApiKeyAuth)
        assert config.auth.type == "API_KEY"
        # API key is redacted by the server and filled with empty string
        assert config.auth.api_key == ""

    def test_anthropic_with_custom_base_url(self) -> None:
        data = {
            "type": "ANTHROPIC",
            "auth": {"type": "API_KEY"},
            "baseUrl": "https://custom.anthropic.example.com",
        }
        config = _provider_config_from_api(data)
        assert isinstance(config, CatalogAnthropicProviderConfig)
        assert config.base_url == "https://custom.anthropic.example.com"

    def test_anthropic_without_base_url(self) -> None:
        data = {"type": "ANTHROPIC", "auth": {"type": "API_KEY"}}
        config = _provider_config_from_api(data)
        assert isinstance(config, CatalogAnthropicProviderConfig)
        assert config.base_url is None

    def test_openai_falls_through_as_default(self) -> None:
        data = {"type": "OPENAI", "auth": {"type": "API_KEY"}}
        config = _provider_config_from_api(data)
        assert isinstance(config, CatalogOpenAiProviderConfig)
        assert isinstance(config.auth, CatalogOpenAiApiKeyAuth)

    def test_aws_bedrock(self) -> None:
        data = {"type": "AWS_BEDROCK", "auth": {"type": "ACCESS_KEY"}, "region": "us-east-1"}
        config = _provider_config_from_api(data)
        assert isinstance(config, CatalogAwsBedrockProviderConfig)
        assert isinstance(config.auth, CatalogBedrockAccessKeyAuth)
        assert config.region == "us-east-1"

    def test_azure_foundry(self) -> None:
        data = {
            "type": "AZURE_FOUNDRY",
            "auth": {"type": "API_KEY"},
            "endpoint": "https://mymodel.openai.azure.com",
        }
        config = _provider_config_from_api(data)
        assert isinstance(config, CatalogAzureFoundryProviderConfig)

    def test_unknown_type_falls_through_to_openai(self) -> None:
        # Unknown provider types default to OpenAI (existing behaviour).
        data = {"type": "UNKNOWN_FUTURE_PROVIDER", "auth": {"type": "API_KEY"}}
        config = _provider_config_from_api(data)
        assert isinstance(config, CatalogOpenAiProviderConfig)


class TestCatalogLlmProviderFromApi:
    """Tests for CatalogLlmProvider.from_api deserialization."""

    def _anthropic_entity(self) -> dict:
        return {
            "id": "test-anthropic-provider",
            "attributes": {
                "providerConfig": {
                    "type": "ANTHROPIC",
                    "auth": {"type": "API_KEY"},
                    "baseUrl": "https://api.anthropic.com",
                },
                "models": [
                    {"id": "claude-3-5-sonnet-20241022", "family": "ANTHROPIC"},
                ],
                "name": "Test Anthropic Provider",
                "defaultModelId": "claude-3-5-sonnet-20241022",
            },
        }

    def test_from_api_returns_correct_type(self) -> None:
        provider = CatalogLlmProvider.from_api(self._anthropic_entity())
        assert provider.id == "test-anthropic-provider"
        assert isinstance(provider.attributes.provider_config, CatalogAnthropicProviderConfig)

    def test_from_api_provider_config_fields(self) -> None:
        provider = CatalogLlmProvider.from_api(self._anthropic_entity())
        config = provider.attributes.provider_config
        assert config.type == "ANTHROPIC"
        assert config.base_url == "https://api.anthropic.com"

    def test_from_api_auth_fields(self) -> None:
        provider = CatalogLlmProvider.from_api(self._anthropic_entity())
        auth = provider.attributes.provider_config.auth
        assert isinstance(auth, CatalogAnthropicApiKeyAuth)
        assert auth.type == "API_KEY"

    def test_from_api_models(self) -> None:
        provider = CatalogLlmProvider.from_api(self._anthropic_entity())
        assert len(provider.attributes.models) == 1
        model = provider.attributes.models[0]
        assert model.id == "claude-3-5-sonnet-20241022"
        assert model.family == "ANTHROPIC"

    def test_from_api_name_and_default_model(self) -> None:
        provider = CatalogLlmProvider.from_api(self._anthropic_entity())
        assert provider.attributes.name == "Test Anthropic Provider"
        assert provider.attributes.default_model_id == "claude-3-5-sonnet-20241022"


class TestCatalogAnthropicApiKeyAuth:
    """Tests for CatalogAnthropicApiKeyAuth model class."""

    def test_default_type(self) -> None:
        auth = CatalogAnthropicApiKeyAuth()
        assert auth.type == "API_KEY"
        assert auth.api_key is None

    def test_with_api_key(self) -> None:
        auth = CatalogAnthropicApiKeyAuth(api_key="sk-ant-test-key")
        assert auth.api_key == "sk-ant-test-key"

    def test_client_class_is_anthropic_provider_auth(self) -> None:
        assert CatalogAnthropicApiKeyAuth.client_class() is AnthropicProviderAuth


class TestCatalogAnthropicProviderConfig:
    """Tests for CatalogAnthropicProviderConfig model class."""

    def test_default_type(self) -> None:
        config = CatalogAnthropicProviderConfig()
        assert config.type == "ANTHROPIC"
        assert config.base_url is None
        assert config.auth is None

    def test_with_auth(self) -> None:
        auth = CatalogAnthropicApiKeyAuth(api_key="sk-ant-test-key")
        config = CatalogAnthropicProviderConfig(auth=auth)
        assert isinstance(config.auth, CatalogAnthropicApiKeyAuth)

    def test_client_class_is_anthropic_provider_config(self) -> None:
        assert CatalogAnthropicProviderConfig.client_class() is AnthropicProviderConfig
