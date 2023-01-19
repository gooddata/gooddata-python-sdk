# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Optional

from gooddata_sdk.catalog.catalog_service_base import CatalogServiceBase
from gooddata_sdk.catalog.organization.entity_model.organization import CatalogOrganizationDocument
from gooddata_sdk.client import GoodDataApiClient


class CatalogOrganizationService(CatalogServiceBase):
    def __init__(self, api_client: GoodDataApiClient) -> None:
        super(CatalogOrganizationService, self).__init__(api_client)

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
