# (C) 2022 GoodData Corporation
from __future__ import annotations

import functools
from typing import Any, Optional

from gooddata_api_client.exceptions import NotFoundException
from gooddata_api_client.model.declarative_export_templates import DeclarativeExportTemplates
from gooddata_api_client.model.declarative_notification_channels import DeclarativeNotificationChannels
from gooddata_api_client.model.json_api_csp_directive_in_document import JsonApiCspDirectiveInDocument
from gooddata_api_client.model.json_api_export_template_in_document import JsonApiExportTemplateInDocument
from gooddata_api_client.model.json_api_export_template_post_optional_id_document import (
    JsonApiExportTemplatePostOptionalIdDocument,
)
from gooddata_api_client.model.json_api_identity_provider_in_document import JsonApiIdentityProviderInDocument
from gooddata_api_client.model.json_api_organization_setting_in_document import JsonApiOrganizationSettingInDocument

from gooddata_sdk import CatalogDeclarativeExportTemplate, CatalogExportTemplate
from gooddata_sdk.catalog.catalog_service_base import CatalogServiceBase
from gooddata_sdk.catalog.organization.entity_model.directive import CatalogCspDirective
from gooddata_sdk.catalog.organization.entity_model.identity_provider import CatalogIdentityProvider
from gooddata_sdk.catalog.organization.entity_model.jwk import CatalogJwk, CatalogJwkDocument
from gooddata_sdk.catalog.organization.entity_model.llm_endpoint import (
    CatalogLlmEndpoint,
    CatalogLlmEndpointDocument,
    CatalogLlmEndpointPatch,
    CatalogLlmEndpointPatchDocument,
)
from gooddata_sdk.catalog.organization.entity_model.organization import CatalogOrganizationDocument
from gooddata_sdk.catalog.organization.entity_model.setting import CatalogOrganizationSetting
from gooddata_sdk.catalog.organization.layout.identity_provider import CatalogDeclarativeIdentityProvider
from gooddata_sdk.catalog.organization.layout.notification_channel import CatalogDeclarativeNotificationChannel
from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.utils import load_all_entities, load_all_entities_dict


class CatalogOrganizationService(CatalogServiceBase):
    def __init__(self, api_client: GoodDataApiClient) -> None:
        super().__init__(api_client)

    # Entities API

    def update_oidc_parameters(
        self,
        oauth_issuer_location: Optional[str] = None,
        oauth_client_id: Optional[str] = None,
        oauth_client_secret: Optional[str] = None,
    ) -> None:
        """Updates OIDC parameters of organization.

        Args:
            oauth_issuer_location (Optional[str], optional):
                Issuer location. Defaults to None.
            oauth_client_id (Optional[str], optional):
                Public client identifier. Defaults to None.
            oauth_client_secret (Optional[str], optional):
                Client secret. Defaults to None.

        Returns:
            None

        Raises:
            ValueError:
                Parameters were not strictly all none or all string.
        """
        parameters = [oauth_issuer_location, oauth_client_id, oauth_client_secret]
        if not all(p is not None for p in parameters) and any(p is not None for p in parameters):
            raise ValueError("All parameters have to be set to None or all parameters has to be string.")
        organization = self.get_organization()
        organization.attributes.oauth_issuer_location = oauth_issuer_location
        organization.attributes.oauth_client_id = oauth_client_id
        organization_document = CatalogOrganizationDocument(data=organization)
        self._entities_api.update_entity_organizations(
            organization.id, organization_document.to_api(oauth_client_secret=oauth_client_secret)
        )

    def update_name(self, name: str) -> None:
        """Updates the name of the organization.

        Args:
            name (str):
                New name of the organization

        Returns:
            None
        """
        organization = self.get_organization()
        organization.attributes.name = name
        organization_document = CatalogOrganizationDocument(data=organization)
        self._entities_api.update_entity_organizations(organization.id, organization_document.to_api())

    def update_allowed_origins(self, allowed_origins: list[str]) -> None:
        """Updates the allowed origins of the organization.

        Args:
            allowed_origins (list[str]):
                New allowed origins of the organization

        Returns:
            None
        """
        organization = self.get_organization()
        organization.attributes.allowed_origins = allowed_origins
        organization_document = CatalogOrganizationDocument(data=organization)
        self._entities_api.update_entity_organizations(organization.id, organization_document.to_api())

    def create_or_update_jwk(self, jwk: CatalogJwk) -> None:
        """Create a new jwk or overwrite an existing jwk with the same id.

        Args:
            jwk (CatalogJwk):
                Catalog Jwk object to be created or updated.

        Returns:
            None

        Raises:
            ValueError: Jwk can not be updated.
        """
        jwk_document = CatalogJwkDocument(data=jwk)
        try:
            self.get_jwk(jwk.id)
            self._entities_api.update_entity_jwks(id=jwk.id, json_api_jwk_in_document=jwk_document.to_api())
        except NotFoundException:
            self._entities_api.create_entity_jwks(json_api_jwk_in_document=jwk_document.to_api())

    def get_jwk(self, jwk_id: str) -> CatalogJwk:
        """Get an individual jwk.

        Args:
            jwk_id (str):
                Jwk identification string e.g. "demo"

        Returns:
            CatalogJwk:
                Catalog jwk object containing structure of the jwk.
        """
        jwk_api = self._entities_api.get_entity_jwks(id=jwk_id).data
        return CatalogJwk.from_api(jwk_api)

    def delete_jwk(self, jwk_id: str) -> None:
        """Delete a jwk.

        Args:
            jwk_id (str):
                Jwk identification string e.g. "demo"

        Returns:
            None

        Raises:
            ValueError:
                Jwk does not exist.
        """
        try:
            self._entities_api.delete_entity_jwks(jwk_id)
        except NotFoundException:
            raise ValueError(f"Can not delete {jwk_id} jwk. This jwk does not exist.")

    def list_jwks(self) -> list[CatalogJwk]:
        """Returns a list of all jwks in the current organization.

        Returns:
            list[CatalogJwk]:
                List of jwks in the current organization.
        """
        get_jwks = functools.partial(self._entities_api.get_all_entities_jwks, _check_return_type=False)
        jwks = load_all_entities(get_jwks)
        return [CatalogJwk.from_api(jwk) for jwk in jwks.data]

    def list_organization_settings(self) -> list[CatalogOrganizationSetting]:
        """Returns a list of all organization settings in the current organization.

        Returns:
            list[CatalogOrganizationSettings]:
                List of organization settings in the current organization.
        """
        get_organization_settings = functools.partial(
            self._entities_api.get_all_entities_organization_settings, _check_return_type=False
        )
        organization_settings = load_all_entities(get_organization_settings)
        return [
            CatalogOrganizationSetting.from_api(organization_settings)
            for organization_settings in organization_settings.data
        ]

    def get_organization_setting(self, organization_setting_id: str) -> CatalogOrganizationSetting:
        """Get an individual organization setting.

        Args:
            organization_setting_id (str):
                Organization setting identification string e.g. "demo"

        Returns:
            CatalogOrganizationSettings:
                Catalog organization setting object containing structure of the organization setting.
        """
        organization_setting_api = self._entities_api.get_entity_organization_settings(id=organization_setting_id).data
        return CatalogOrganizationSetting.from_api(organization_setting_api)

    def create_organization_setting(self, organization_setting: CatalogOrganizationSetting) -> None:
        """Create a new organization setting.

        Args:
            organization_setting (CatalogOrganizationSettings):
                A catalog organization setting object to be created.

        Returns:
            None
        """
        organization_setting_document = JsonApiOrganizationSettingInDocument(data=organization_setting.to_api())
        self._entities_api.create_entity_organization_settings(
            json_api_organization_setting_in_document=organization_setting_document
        )

    def delete_organization_setting(self, organization_setting_id: str) -> None:
        """Delete an organization setting.

        Args:
            organization_setting_id (str):
                Organization setting identification string e.g. "demo"

        Returns:
            None

        Raises:
            ValueError:
                Organization setting does not exist.
        """
        try:
            self._entities_api.delete_entity_organization_settings(organization_setting_id)
        except NotFoundException:
            raise ValueError(
                f"Can not delete {organization_setting_id} organization setting. "
                f"This organization setting does not exist."
            )

    def update_organization_setting(self, organization_setting: CatalogOrganizationSetting) -> None:
        """Update an organization setting.

        Args:
            organization_setting (CatalogOrganizationSettings):
                A catalog organization setting object to be updated.

        Returns:
            None

        Raises:
            ValueError:
                Organization setting does not exist.
        """
        try:
            organization_setting_document = JsonApiOrganizationSettingInDocument(data=organization_setting.to_api())
            self._entities_api.update_entity_organization_settings(
                organization_setting.id, organization_setting_document
            )
        except NotFoundException:
            raise ValueError(
                f"Can not update {organization_setting.id} organization setting. "
                f"This organization setting does not exist."
            )

    def list_csp_directives(self) -> list[CatalogCspDirective]:
        """Returns a list of all csp directives in the current organization.

        Returns:
            list[CatalogCspDirective]:
                List of csp directives in the current organization.
        """
        get_csp_directives = functools.partial(
            self._entities_api.get_all_entities_csp_directives, _check_return_type=False
        )
        csp_directives = load_all_entities(get_csp_directives)
        return [CatalogCspDirective.from_api(csp_directive) for csp_directive in csp_directives.data]

    def get_csp_directive(self, directive_id: str) -> CatalogCspDirective:
        """Get an individual csp directive.

        Args:
            directive_id (str):
                Csp directive identification string e.g. "demo"

        Returns:
            CatalogCspDirective:
                Catalog csp directive object containing structure of the csp directive.
        """
        csp_directive_api = self._entities_api.get_entity_csp_directives(id=directive_id).data
        return CatalogCspDirective.from_api(csp_directive_api)

    def create_csp_directive(self, csp_directive: CatalogCspDirective) -> None:
        """Create a new csp directive.

        Args:
            csp_directive (CatalogCspDirective):
                A catalog csp directive object to be created.

        Returns:
            None
        """
        csp_directive_document = JsonApiCspDirectiveInDocument(data=csp_directive.to_api())
        self._entities_api.create_entity_csp_directives(json_api_csp_directive_in_document=csp_directive_document)

    def delete_csp_directive(self, csp_directive_id: str) -> None:
        """Delete a csp directive.

        Args:
            csp_directive_id (str):
                Csp directive identification string e.g. "demo"

        Returns:
            None

        Raises:
            ValueError:
                Csp directive does not exist.
        """
        try:
            self._entities_api.delete_entity_csp_directives(csp_directive_id)
        except NotFoundException:
            raise ValueError(f"Can not delete {csp_directive_id} csp directive. This csp directive does not exist.")

    def update_csp_directive(self, csp_directive: CatalogCspDirective) -> None:
        """Update a csp directive.

        Args:
            csp_directive (CatalogCspDirective):
                A catalog csp directive object to be updated.

        Returns:
            None

        Raises:
            ValueError:
                Csp directive does not exist.
        """
        try:
            csp_directive_document = JsonApiCspDirectiveInDocument(data=csp_directive.to_api())
            self._entities_api.update_entity_csp_directives(csp_directive.id, csp_directive_document)
        except NotFoundException:
            raise ValueError(f"Can not update {csp_directive.id} csp directive. This csp directive does not exist.")

    def list_identity_providers(self) -> list[CatalogIdentityProvider]:
        """Returns a list of all identity providers in the current organization.

        Returns:
            list[CatalogIdentityProvider]:
                List of identity providers in the current organization.
        """
        get_identity_providers = functools.partial(
            self._entities_api.get_all_entities_identity_providers,
            _check_return_type=False,
        )
        identity_providers = load_all_entities_dict(get_identity_providers, camel_case=False)
        return [
            CatalogIdentityProvider.from_dict(identity_provider, camel_case=False)
            for identity_provider in identity_providers["data"]
        ]

    def get_identity_provider(self, identity_provider_id: str) -> CatalogIdentityProvider:
        """Get an individual identity provider.

        Args:
            identity_provider_id (str):
                Identity provider identification string e.g. "demo"

        Returns:
            CatalogIdentityProvider:
                Catalog identity provider object containing structure of the identity provider.
        """
        identity_provider_api = self._entities_api.get_entity_identity_providers(id=identity_provider_id).data
        return CatalogIdentityProvider.from_api(identity_provider_api)

    def create_identity_provider(self, identity_provider: CatalogIdentityProvider) -> None:
        """Create a new identity provider.

        Args:
            identity_provider (CatalogIdentityProvider):
                A catalog identity provider object to be created.

        Returns:
            None
        """
        identity_provider_document = JsonApiIdentityProviderInDocument(data=identity_provider.to_api())
        self._entities_api.create_entity_identity_providers(
            json_api_identity_provider_in_document=identity_provider_document
        )

    def delete_identity_provider(self, identity_provider_id: str) -> None:
        """Delete an identity provider.

        Args:
            identity_provider_id (str):
                Identity provider identification string e.g. "demo"

        Returns:
            None
        """
        self._entities_api.delete_entity_identity_providers(identity_provider_id)

    def update_identity_provider(self, identity_provider: CatalogIdentityProvider) -> None:
        """Update an identity provider.

        Args:
            identity_provider (CatalogIdentityProvider):
                A catalog identity provider object to be updated.

        Returns:
            None

        Raises:
            ValueError:
                Identity provider does not exist.
        """
        try:
            identity_provider_document = JsonApiIdentityProviderInDocument(data=identity_provider.to_api())
            self._entities_api.update_entity_identity_providers(identity_provider.id, identity_provider_document)
        except NotFoundException:
            raise ValueError(
                f"Can not update {identity_provider.id} identity provider. This identity provider does not exist."
            )

    def patch_identity_provider_attributes(self, identity_provider_id: str, attributes: dict) -> None:
        """Applies changes to the specified identity provider.

        Args:
            identity_provider_id (str):
                Identity Provider identification string. e.g. "auth0"
            attributes (dict):
                A dictionary containing attributes of the identity provider to be changed.

        Returns:
            None
        """

        self._entities_api.patch_entity_identity_providers(
            identity_provider_id, CatalogIdentityProvider.to_api_patch(identity_provider_id, attributes)
        )

    def create_or_update_export_template(self, export_template: CatalogExportTemplate) -> None:
        """Create a new export template or overwrite an existing export template with the same id.

        Args:
            export_template (CatalogExportTemplate):
                Catalog export template object to be created or updated.

        Returns:
            None

        Raises:
            ValueError: Export template cannot be updated.
        """
        try:
            self.get_export_template(export_template.id)
            self._entities_api.update_entity_export_templates(
                id=export_template.id,
                json_api_export_template_in_document=JsonApiExportTemplateInDocument.from_dict(
                    {"data": export_template.to_dict()}
                ),
            )
        except NotFoundException:
            self._entities_api.create_entity_export_templates(
                json_api_export_template_post_optional_id_document=JsonApiExportTemplatePostOptionalIdDocument(
                    data=export_template.to_api()
                )
            )

    def get_export_template(self, export_template_id: str) -> CatalogExportTemplate:
        """Get an individual export template.

        Args:
            export_template_id (str):
                Export template identification string e.g. "demo"

        Returns:
            CatalogJwk:
                Catalog export template object containing the structure of the export template.
        """
        export_template_api = self._entities_api.get_entity_export_templates(id=export_template_id).data
        return CatalogExportTemplate.from_api(export_template_api)

    def delete_export_template(self, export_template_id: str) -> None:
        """Delete an export template.

        Args:
            export_template_id (str):
                Export template identification string e.g. "demo"

        Returns:
            None

        Raises:
            ValueError:
                Export template does not exist.
        """
        try:
            self._entities_api.delete_entity_export_templates(export_template_id)
        except NotFoundException:
            raise ValueError(
                f"Can not delete {export_template_id} export template. This export template does not exist."
            )

    def list_export_templates(self) -> list[CatalogExportTemplate]:
        """Returns a list of all export templates in the current organization.

        Returns:
            list[CatalogExportTemplate]:
                List of export templates in the current organization.
        """
        get_export_templates = functools.partial(
            self._entities_api.get_all_entities_export_templates,
            _check_return_type=False,
        )
        export_templates = load_all_entities_dict(get_export_templates, camel_case=False)
        return [
            CatalogExportTemplate.from_dict(export_template, camel_case=False)
            for export_template in export_templates["data"]
        ]

    def get_llm_endpoint(self, id: str) -> CatalogLlmEndpoint:
        """
        Get LLM endpoint by ID.

        Args:
            id: LLM endpoint identifier

        Returns:
            CatalogLlmEndpoint: Retrieved LLM endpoint
        """
        response = self._entities_api.get_entity_llm_endpoints(id, _check_return_type=False)
        return CatalogLlmEndpoint.from_api(response.data)

    def list_llm_endpoints(
        self,
        filter: Optional[str] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
        sort: Optional[list[str]] = None,
        meta_include: Optional[list[str]] = None,
    ) -> list[CatalogLlmEndpoint]:
        """
        List all LLM endpoints.

        Args:
            filter: Optional filter string
            page: Zero-based page index (0..N)
            size: The size of the page to be returned
            sort: Sorting criteria in the format: property,(asc|desc). Multiple sort criteria are supported.
            meta_include: Include Meta objects

        Returns:
            list[CatalogLlmEndpoint]: List of LLM endpoints

        Note:
            Default values for optional parameters are documented in the LLM endpoints of the GoodData API.
        """
        kwargs: dict[str, Any] = {}
        if filter is not None:
            kwargs["filter"] = filter
        if page is not None:
            kwargs["page"] = page
        if size is not None:
            kwargs["size"] = size
        if sort is not None:
            kwargs["sort"] = sort
        if meta_include is not None:
            kwargs["meta_include"] = meta_include
        kwargs["_check_return_type"] = False

        response = self._entities_api.get_all_entities_llm_endpoints(**kwargs)
        return [CatalogLlmEndpoint.from_api(endpoint) for endpoint in response.data]

    def create_llm_endpoint(
        self,
        id: str,
        title: str,
        token: str,
        description: Optional[str] = None,
        provider: Optional[str] = None,
        base_url: Optional[str] = None,
        llm_organization: Optional[str] = None,
        llm_model: Optional[str] = None,
    ) -> CatalogLlmEndpoint:
        """
        Create a new LLM endpoint.

        Args:
            id: Identifier of the LLM endpoint
            title: User-facing title of the LLM Provider
            token: The token to use to connect to the LLM provider
            description: Optional user-facing description of the LLM endpoint
            provider: Optional LLM provider name (e.g., "openai")
            base_url: Optional base URL for custom LLM endpoint
            llm_organization: Optional LLM organization identifier
            llm_model: Optional LLM default model override

        Returns:
            CatalogLlmEndpoint: Created LLM endpoint
        """
        llm_endpoint = CatalogLlmEndpoint.init(
            id=id,
            title=title,
            token=token,
            description=description,
            provider=provider,
            base_url=base_url,
            llm_organization=llm_organization,
            llm_model=llm_model,
        )
        llm_endpoint_document = CatalogLlmEndpointDocument(data=llm_endpoint)
        response = self._entities_api.create_entity_llm_endpoints(
            json_api_llm_endpoint_in_document=llm_endpoint_document.to_api(), _check_return_type=False
        )
        return CatalogLlmEndpoint.from_api(response.data)

    def update_llm_endpoint(
        self,
        id: str,
        title: Optional[str] = None,
        token: Optional[str] = None,
        description: Optional[str] = None,
        provider: Optional[str] = None,
        base_url: Optional[str] = None,
        llm_organization: Optional[str] = None,
        llm_model: Optional[str] = None,
    ) -> CatalogLlmEndpoint:
        """
        Update an existing LLM endpoint.

        Args:
            id: Identifier of the LLM endpoint
            title: User-facing title of the LLM Provider
            token: The token to use to connect to the LLM provider. If not provided, the existing token will be preserved.
            description: User-facing description of the LLM endpoint
            provider: LLM provider name (e.g., "openai")
            base_url: Base URL for custom LLM endpoint
            llm_organization: LLM organization identifier
            llm_model: LLM default model override

        Returns:
            CatalogLlmEndpoint: Updated LLM endpoint
        """
        llm_endpoint_patch = CatalogLlmEndpointPatch.init(
            id=id,
            title=title,
            token=token,
            description=description,
            provider=provider,
            base_url=base_url,
            llm_organization=llm_organization,
            llm_model=llm_model,
        )
        llm_endpoint_patch_document = CatalogLlmEndpointPatchDocument(data=llm_endpoint_patch)
        response = self._entities_api.patch_entity_llm_endpoints(
            id, llm_endpoint_patch_document.to_api(), _check_return_type=False
        )
        return CatalogLlmEndpoint.from_api(response.data)

    def delete_llm_endpoint(self, id: str) -> None:
        """
        Delete an LLM endpoint.

        Args:
            id: LLM endpoint identifier
        """
        self._entities_api.delete_entity_llm_endpoints(id, _check_return_type=False)

    # Layout APIs

    def get_declarative_notification_channels(self) -> list[CatalogDeclarativeNotificationChannel]:
        """
        Get all declarative notification channels in the current organization.

        Returns:
            list[CatalogDeclarativeNotificationChannel]:
                List of declarative notification channels.
        """
        return [
            CatalogDeclarativeNotificationChannel.from_api(nc)
            for nc in self._layout_api.get_notification_channels_layout().notification_channels
        ]

    def put_declarative_notification_channels(
        self, notification_channels: list[CatalogDeclarativeNotificationChannel]
    ) -> None:
        """
        Put declarative notification channels in the current organization.

        Args:
            notification_channels (list[CatalogDeclarativeNotificationChannel]):
                List of declarative notification channels.

        Returns:
            None
        """
        api_ncs = [nc.to_api() for nc in notification_channels]
        self._layout_api.set_notification_channels(DeclarativeNotificationChannels(notification_channels=api_ncs))

    def get_declarative_identity_providers(self) -> list[CatalogDeclarativeIdentityProvider]:
        """
        Get all declarative identity providers in the current organization.

        Returns:
            list[CatalogDeclarativeIdentityProvider]:
                List of declarative identity providers.
        """
        return [
            CatalogDeclarativeIdentityProvider.from_api(idp) for idp in self._layout_api.get_identity_providers_layout()
        ]

    def put_declarative_identity_providers(self, identity_providers: list[CatalogDeclarativeIdentityProvider]) -> None:
        """
        Put declarative identity providers in the current organization.

        Args:
            identity_providers (list[CatalogDeclarativeIdentityProvider]):
                List of declarative identity providers.

        Returns:
            None
        """
        api_idps = [idp.to_api() for idp in identity_providers]
        self._layout_api.set_identity_providers(declarative_identity_provider=api_idps)

    def get_declarative_export_templates(self) -> list[CatalogDeclarativeExportTemplate]:
        """
        Get all declarative export templates in the current organization.

        Returns:
            list[CatalogDeclarativeExportTemplate]:
                List of declarative export templates.
        """
        export_templates_api = self._layout_api.get_export_templates_layout()
        if hasattr(export_templates_api, "export_templates"):
            return [
                CatalogDeclarativeExportTemplate.from_api(template)
                for template in export_templates_api.export_templates
            ]
        else:
            return []

    def put_declarative_export_templates(self, export_templates: list[CatalogDeclarativeExportTemplate]) -> None:
        """
        Put declarative export templates in the current organization.

        Args:
            export_templates (list[CatalogDeclarativeExportTemplate]):
                List of declarative export templates.

        Returns:
            None
        """
        api_export_templates = [export_template.to_api() for export_template in export_templates]
        self._layout_api.set_export_templates(
            declarative_export_templates=DeclarativeExportTemplates(export_templates=api_export_templates)
        )
