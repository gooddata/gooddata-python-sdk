# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Optional

import attr
from gooddata_api_client.model.json_api_organization_in import JsonApiOrganizationIn
from gooddata_api_client.model.json_api_organization_in_attributes import JsonApiOrganizationInAttributes
from gooddata_api_client.model.json_api_organization_in_document import JsonApiOrganizationInDocument

from gooddata_sdk.catalog.base import Base


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

    @staticmethod
    def client_class() -> type[JsonApiOrganizationIn]:
        return JsonApiOrganizationIn


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
