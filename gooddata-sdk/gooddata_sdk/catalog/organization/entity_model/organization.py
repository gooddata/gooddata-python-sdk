# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any, Optional

import attr
from gooddata_api_client.model.json_api_identity_provider_to_one_linkage import JsonApiIdentityProviderToOneLinkage
from gooddata_api_client.model.json_api_organization_in import JsonApiOrganizationIn
from gooddata_api_client.model.json_api_organization_in_attributes import JsonApiOrganizationInAttributes
from gooddata_api_client.model.json_api_organization_in_document import JsonApiOrganizationInDocument
from gooddata_api_client.model.json_api_organization_in_relationships import JsonApiOrganizationInRelationships
from gooddata_api_client.model.json_api_organization_in_relationships_identity_provider import (
    JsonApiOrganizationInRelationshipsIdentityProvider,
)

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.utils import safeget


@attr.s(auto_attribs=True, kw_only=True)
class CatalogOrganizationDocument(Base):
    data: CatalogOrganization

    @staticmethod
    def client_class() -> type[JsonApiOrganizationInDocument]:
        return JsonApiOrganizationInDocument

    def to_api(self, oauth_client_secret: Optional[str] = None) -> JsonApiOrganizationInDocument:
        dictionary = self._get_snake_dict()
        if oauth_client_secret is not None:
            dictionary["data"]["attributes"]["oauth_client_secret"] = oauth_client_secret
        return self.client_class().from_dict(dictionary, camel_case=False)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogOrganization(Base):
    id: str
    attributes: CatalogOrganizationAttributes
    identity_provider_id: Optional[str] = None

    @staticmethod
    def client_class() -> type[JsonApiOrganizationIn]:
        return JsonApiOrganizationIn

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogOrganization:
        ea = entity.get("attributes", {})
        er = entity.get("relationships", {})

        attributes = CatalogOrganizationAttributes(
            name=safeget(ea, ["name"]),
            hostname=safeget(ea, ["hostname"]),
            allowed_origins=safeget(ea, ["allowed_origins"]),
            oauth_issuer_location=safeget(ea, ["oauth_issuer_location"]),
            oauth_client_id=safeget(ea, ["oauth_client_id"]),
        )

        identity_provider_id = safeget(er, ["identityProvider", "data", "id"])

        return cls(
            id=entity["id"],
            attributes=attributes,
            identity_provider_id=identity_provider_id,
        )

    def to_api(self) -> JsonApiOrganizationIn:
        kwargs = {}
        if self.identity_provider_id:
            kwargs["relationships"] = JsonApiOrganizationInRelationships(
                identity_provider=JsonApiOrganizationInRelationshipsIdentityProvider(
                    data=JsonApiIdentityProviderToOneLinkage(id=self.identity_provider_id, type="identityProvider")
                )
            )

        return JsonApiOrganizationIn(
            id=self.id,
            type="organization",
            attributes=self.attributes.to_api(),
            **kwargs,
        )


@attr.s(auto_attribs=True, kw_only=True)
class CatalogOrganizationAttributes(Base):
    name: Optional[str] = None
    hostname: Optional[str] = None
    allowed_origins: Optional[list[str]] = None
    oauth_issuer_location: Optional[str] = None
    oauth_client_id: Optional[str] = None

    @staticmethod
    def client_class() -> type[JsonApiOrganizationInAttributes]:
        return JsonApiOrganizationInAttributes
