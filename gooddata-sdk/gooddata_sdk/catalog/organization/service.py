# (C) 2022 GoodData Corporation
from __future__ import annotations

import functools
from typing import List, Optional

from gooddata_api_client.exceptions import NotFoundException
from gooddata_sdk.catalog.catalog_service_base import CatalogServiceBase
from gooddata_sdk.catalog.organization.entity_model.jwk import CatalogJwk, CatalogJwkDocument
from gooddata_sdk.catalog.organization.entity_model.organization import CatalogOrganizationDocument
from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.utils import load_all_entities


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

    def list_jwks(self) -> List[CatalogJwk]:
        """Returns a list of all jwks in current organization.

        Returns:
            List[CatalogJwk]:
                List of jwks in the current organization.
        """
        get_jwks = functools.partial(self._entities_api.get_all_entities_jwks, _check_return_type=False)
        jwks = load_all_entities(get_jwks)
        return [CatalogJwk.from_api(jwk) for jwk in jwks.data]
