# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any, Union

from attr import define
from gooddata_api_client.model.aws_bedrock_provider_config import AwsBedrockProviderConfig
from gooddata_api_client.model.azure_foundry_provider_auth import AzureFoundryProviderAuth
from gooddata_api_client.model.azure_foundry_provider_config import AzureFoundryProviderConfig
from gooddata_api_client.model.bedrock_provider_auth import BedrockProviderAuth
from gooddata_api_client.model.json_api_llm_provider_in import JsonApiLlmProviderIn
from gooddata_api_client.model.json_api_llm_provider_in_attributes import JsonApiLlmProviderInAttributes
from gooddata_api_client.model.json_api_llm_provider_in_attributes_models_inner import (
    JsonApiLlmProviderInAttributesModelsInner,
)
from gooddata_api_client.model.json_api_llm_provider_in_document import JsonApiLlmProviderInDocument
from gooddata_api_client.model.json_api_llm_provider_patch import JsonApiLlmProviderPatch
from gooddata_api_client.model.json_api_llm_provider_patch_document import JsonApiLlmProviderPatchDocument
from gooddata_api_client.model.list_llm_provider_models_request import ListLlmProviderModelsRequest
from gooddata_api_client.model.list_llm_provider_models_response import ListLlmProviderModelsResponse
from gooddata_api_client.model.open_ai_provider_auth import OpenAiProviderAuth
from gooddata_api_client.model.open_ai_provider_config import OpenAIProviderConfig
from gooddata_api_client.model.test_llm_provider_by_id_request import TestLlmProviderByIdRequest
from gooddata_api_client.model.test_llm_provider_definition_request import TestLlmProviderDefinitionRequest
from gooddata_api_client.model.test_llm_provider_response import TestLlmProviderResponse

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.utils import safeget

# --- OpenAI auth ---


@define(kw_only=True)
class CatalogOpenAiApiKeyAuth(Base):
    """API key authentication for the OpenAI provider."""

    api_key: str | None = None
    type: str = "API_KEY"

    @staticmethod
    def client_class() -> type[OpenAiProviderAuth]:
        return OpenAiProviderAuth


CatalogOpenAiAuth = Union[CatalogOpenAiApiKeyAuth]

# --- AWS Bedrock auth ---


@define(kw_only=True)
class CatalogBedrockAccessKeyAuth(Base):
    """AWS access key authentication for the Bedrock provider."""

    access_key_id: str | None = None
    secret_access_key: str | None = None
    session_token: str | None = None
    type: str = "ACCESS_KEY"

    @staticmethod
    def client_class() -> type[BedrockProviderAuth]:
        return BedrockProviderAuth


CatalogBedrockAuth = Union[CatalogBedrockAccessKeyAuth]

# --- Azure Foundry auth ---


@define(kw_only=True)
class CatalogAzureFoundryApiKeyAuth(Base):
    """API key authentication for the Azure Foundry provider."""

    api_key: str | None = None
    type: str = "API_KEY"

    @staticmethod
    def client_class() -> type[AzureFoundryProviderAuth]:
        return AzureFoundryProviderAuth


CatalogAzureFoundryAuth = Union[CatalogAzureFoundryApiKeyAuth]

# --- Provider config types ---


@define(kw_only=True)
class CatalogOpenAiProviderConfig(Base):
    """OpenAI provider configuration."""

    auth: CatalogOpenAiAuth | None = None
    base_url: str | None = None
    organization: str | None = None
    type: str = "OPENAI"

    @staticmethod
    def client_class() -> type[OpenAIProviderConfig]:
        return OpenAIProviderConfig


@define(kw_only=True)
class CatalogAwsBedrockProviderConfig(Base):
    """AWS Bedrock provider configuration."""

    auth: CatalogBedrockAuth | None = None
    region: str | None = None
    type: str = "AWS_BEDROCK"

    @staticmethod
    def client_class() -> type[AwsBedrockProviderConfig]:
        return AwsBedrockProviderConfig


@define(kw_only=True)
class CatalogAzureFoundryProviderConfig(Base):
    """Azure Foundry provider configuration."""

    auth: CatalogAzureFoundryAuth | None = None
    endpoint: str | None = None
    type: str = "AZURE_FOUNDRY"

    @staticmethod
    def client_class() -> type[AzureFoundryProviderConfig]:
        return AzureFoundryProviderConfig


CatalogLlmProviderConfig = Union[
    CatalogOpenAiProviderConfig,
    CatalogAwsBedrockProviderConfig,
    CatalogAzureFoundryProviderConfig,
]


def _openai_auth_from_api(data: dict[str, Any]) -> CatalogOpenAiAuth:
    auth_type = safeget(data, ["type"]) or "API_KEY"
    if auth_type == "API_KEY":
        return CatalogOpenAiApiKeyAuth(
            api_key="",  # Credentials are not returned for security reasons
            type=auth_type,
        )
    raise ValueError(f"Unknown OpenAI auth type: {auth_type}")


def _bedrock_auth_from_api(data: dict[str, Any]) -> CatalogBedrockAuth:
    auth_type = safeget(data, ["type"]) or "ACCESS_KEY"
    if auth_type == "ACCESS_KEY":
        return CatalogBedrockAccessKeyAuth(
            access_key_id="",  # Credentials are not returned for security reasons
            secret_access_key="",
            session_token=safeget(data, ["sessionToken"]),
            type=auth_type,
        )
    raise ValueError(f"Unknown Bedrock auth type: {auth_type}")


def _azure_foundry_auth_from_api(data: dict[str, Any]) -> CatalogAzureFoundryAuth:
    auth_type = safeget(data, ["type"]) or "API_KEY"
    if auth_type == "API_KEY":
        return CatalogAzureFoundryApiKeyAuth(
            api_key="",  # Credentials are not returned for security reasons
            type=auth_type,
        )
    raise ValueError(f"Unknown Azure Foundry auth type: {auth_type}")


def _provider_config_from_api(data: dict[str, Any]) -> CatalogLlmProviderConfig:
    provider_type = safeget(data, ["type"]) or "OPENAI"
    auth_data = safeget(data, ["auth"])

    if provider_type == "AWS_BEDROCK":
        return CatalogAwsBedrockProviderConfig(
            auth=_bedrock_auth_from_api(auth_data) if auth_data is not None else None,
            region=safeget(data, ["region"]),
        )

    if provider_type == "AZURE_FOUNDRY":
        return CatalogAzureFoundryProviderConfig(
            auth=_azure_foundry_auth_from_api(auth_data) if auth_data is not None else None,
            endpoint=safeget(data, ["endpoint"]),
        )

    # Default: OpenAI
    return CatalogOpenAiProviderConfig(
        auth=_openai_auth_from_api(auth_data) if auth_data is not None else None,
        base_url=safeget(data, ["baseUrl"]),
        organization=safeget(data, ["organization"]),
    )


# --- Document wrappers ---


@define(kw_only=True)
class CatalogLlmProviderDocument(Base):
    data: CatalogLlmProvider

    @staticmethod
    def client_class() -> type[JsonApiLlmProviderInDocument]:
        return JsonApiLlmProviderInDocument


@define(kw_only=True)
class CatalogLlmProviderPatchDocument(Base):
    data: CatalogLlmProviderPatch

    @staticmethod
    def client_class() -> type[JsonApiLlmProviderPatchDocument]:
        return JsonApiLlmProviderPatchDocument


# --- Model type ---


@define(kw_only=True)
class CatalogLlmProviderModel(Base):
    """Represents a single LLM model available for a provider."""

    id: str
    family: str

    @staticmethod
    def client_class() -> type[JsonApiLlmProviderInAttributesModelsInner]:
        return JsonApiLlmProviderInAttributesModelsInner


# --- Main entity types ---


@define(kw_only=True)
class CatalogLlmProvider(Base):
    id: str
    attributes: CatalogLlmProviderAttributes | None = None

    @staticmethod
    def client_class() -> type[JsonApiLlmProviderIn]:
        return JsonApiLlmProviderIn

    @classmethod
    def init(
        cls,
        id: str,
        models: list[CatalogLlmProviderModel],
        provider_config: CatalogLlmProviderConfig,
        name: str | None = None,
        description: str | None = None,
        default_model_id: str | None = None,
    ) -> CatalogLlmProvider:
        return cls(
            id=id,
            attributes=CatalogLlmProviderAttributes(
                models=models,
                provider_config=provider_config,
                name=name,
                description=description,
                default_model_id=default_model_id,
            ),
        )

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogLlmProvider:
        ea = entity["attributes"]
        raw_models = safeget(ea, ["models"]) or []
        models = [
            CatalogLlmProviderModel(
                id=safeget(m, ["id"]),
                family=safeget(m, ["family"]),
            )
            for m in raw_models
        ]
        raw_config = safeget(ea, ["providerConfig"]) or {}
        provider_config = _provider_config_from_api(raw_config)
        return cls(
            id=entity["id"],
            attributes=CatalogLlmProviderAttributes(
                models=models,
                provider_config=provider_config,
                name=safeget(ea, ["name"]),
                description=safeget(ea, ["description"]),
                default_model_id=safeget(ea, ["defaultModelId"]),
            ),
        )


@define(kw_only=True)
class CatalogLlmProviderPatch(Base):
    id: str
    attributes: CatalogLlmProviderPatchAttributes | None = None

    @staticmethod
    def client_class() -> type[JsonApiLlmProviderPatch]:
        return JsonApiLlmProviderPatch

    @classmethod
    def init(
        cls,
        id: str,
        models: list[CatalogLlmProviderModel] | None = None,
        provider_config: CatalogLlmProviderConfig | None = None,
        name: str | None = None,
        description: str | None = None,
        default_model_id: str | None = None,
    ) -> CatalogLlmProviderPatch:
        return cls(
            id=id,
            attributes=CatalogLlmProviderPatchAttributes(
                models=models,
                provider_config=provider_config,
                name=name,
                description=description,
                default_model_id=default_model_id,
            ),
        )


# --- Attributes ---


@define(kw_only=True)
class CatalogLlmProviderAttributes(Base):
    models: list[CatalogLlmProviderModel]
    provider_config: CatalogLlmProviderConfig
    name: str | None = None
    description: str | None = None
    default_model_id: str | None = None

    @staticmethod
    def client_class() -> type[JsonApiLlmProviderInAttributes]:
        return JsonApiLlmProviderInAttributes


@define(kw_only=True)
class CatalogLlmProviderPatchAttributes(Base):
    models: list[CatalogLlmProviderModel] | None = None
    provider_config: CatalogLlmProviderConfig | None = None
    name: str | None = None
    description: str | None = None
    default_model_id: str | None = None

    @staticmethod
    def client_class() -> type[JsonApiLlmProviderInAttributes]:
        return JsonApiLlmProviderInAttributes


# --- Action request/response model types ---


@define(kw_only=True)
class CatalogModelTestResult(Base):
    """Result for a single model connectivity test."""

    model_id: str
    success: bool
    message: str | None = None

    @staticmethod
    def client_class() -> type:
        raise NotImplementedError()

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> CatalogModelTestResult:
        return cls(
            model_id=safeget(data, ["modelId"]) or "",
            success=safeget(data, ["success"]) or False,
            message=safeget(data, ["message"]),
        )


@define(kw_only=True)
class CatalogTestLlmProviderResponse(Base):
    """Response from test LLM provider endpoint."""

    success: bool
    message: str | None = None
    model_results: list[CatalogModelTestResult] | None = None

    @staticmethod
    def client_class() -> type[TestLlmProviderResponse]:
        return TestLlmProviderResponse

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> CatalogTestLlmProviderResponse:
        raw_model_results = safeget(data, ["modelResults"]) or []
        model_results = [CatalogModelTestResult.from_api(r) for r in raw_model_results]
        return cls(
            success=safeget(data, ["success"]) or False,
            message=safeget(data, ["message"]),
            model_results=model_results if model_results else None,
        )


@define(kw_only=True)
class CatalogTestLlmProviderDefinitionRequest(Base):
    """Request for testing LLM provider connectivity with a full definition."""

    provider_config: CatalogLlmProviderConfig
    models: list[CatalogLlmProviderModel] | None = None

    @staticmethod
    def client_class() -> type[TestLlmProviderDefinitionRequest]:
        return TestLlmProviderDefinitionRequest

    def to_api(self) -> TestLlmProviderDefinitionRequest:
        kwargs: dict[str, Any] = {}
        if self.models is not None:
            kwargs["models"] = [m.to_api() for m in self.models]
        return TestLlmProviderDefinitionRequest(
            provider_config=self.provider_config.to_api(),
            **kwargs,
        )


@define(kw_only=True)
class CatalogTestLlmProviderByIdRequest(Base):
    """Request for testing an existing LLM provider by ID with optional overrides."""

    provider_config: CatalogLlmProviderConfig | None = None
    models: list[CatalogLlmProviderModel] | None = None

    @staticmethod
    def client_class() -> type[TestLlmProviderByIdRequest]:
        return TestLlmProviderByIdRequest

    def to_api(self) -> TestLlmProviderByIdRequest:
        kwargs: dict[str, Any] = {}
        if self.provider_config is not None:
            kwargs["provider_config"] = self.provider_config.to_api()
        if self.models is not None:
            kwargs["models"] = [m.to_api() for m in self.models]
        return TestLlmProviderByIdRequest(**kwargs)


@define(kw_only=True)
class CatalogListLlmProviderModelsRequest(Base):
    """Request for listing models available on an LLM provider."""

    provider_config: CatalogLlmProviderConfig

    @staticmethod
    def client_class() -> type[ListLlmProviderModelsRequest]:
        return ListLlmProviderModelsRequest

    def to_api(self) -> ListLlmProviderModelsRequest:
        return ListLlmProviderModelsRequest(
            provider_config=self.provider_config.to_api(),
        )


@define(kw_only=True)
class CatalogListLlmProviderModelsResponse(Base):
    """Response from list LLM provider models endpoint."""

    success: bool
    models: list[CatalogLlmProviderModel] | None = None
    message: str | None = None

    @staticmethod
    def client_class() -> type[ListLlmProviderModelsResponse]:
        return ListLlmProviderModelsResponse

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> CatalogListLlmProviderModelsResponse:
        raw_models = safeget(data, ["models"]) or []
        models = [
            CatalogLlmProviderModel(
                id=safeget(m, ["id"]) or "",
                family=safeget(m, ["family"]) or "",
            )
            for m in raw_models
        ]
        return cls(
            success=safeget(data, ["success"]) or False,
            models=models if models else None,
            message=safeget(data, ["message"]),
        )
