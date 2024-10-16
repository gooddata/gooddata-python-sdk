# (C) 2022 GoodData Corporation
from __future__ import annotations

import functools
from typing import Optional

from gooddata_api_client.exceptions import NotFoundException
from gooddata_api_client.model.declarative_notification_channels import DeclarativeNotificationChannels
from gooddata_api_client.model.json_api_csp_directive_in_document import JsonApiCspDirectiveInDocument
from gooddata_api_client.model.json_api_organization_setting_in_document import JsonApiOrganizationSettingInDocument

from gooddata_sdk.catalog.catalog_service_base import CatalogServiceBase
from gooddata_sdk.catalog.organization.entity_model.directive import CatalogCspDirective
from gooddata_sdk.catalog.organization.entity_model.jwk import CatalogJwk, CatalogJwkDocument
from gooddata_sdk.catalog.organization.entity_model.organization import CatalogOrganizationDocument
from gooddata_sdk.catalog.organization.entity_model.setting import CatalogOrganizationSetting
from gooddata_sdk.catalog.organization.layout.notification_channel import CatalogDeclarativeNotificationChannel
from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.utils import load_all_entities


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
                A catalog organization setting an object to be created.

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
                A catalog organization setting an object to be updated.

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
            list[CatalogOrganizationSettings]:
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
                A catalog csp directive an object to be created.

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
                A catalog csp directive an object to be updated.

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
