# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any

from gooddata_metadata_client.model.json_api_organization_in import JsonApiOrganizationIn
from gooddata_metadata_client.model.json_api_organization_in_attributes import JsonApiOrganizationInAttributes
from gooddata_metadata_client.model.json_api_organization_in_document import JsonApiOrganizationInDocument
from gooddata_sdk.catalog.entity import CatalogNameEntity


class CatalogOrganization(CatalogNameEntity):
    def __init__(self, organization_id: str, name: str, hostname: str) -> None:
        super(CatalogOrganization, self).__init__(organization_id, name)
        self.hostname = hostname

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogOrganization:
        ea = entity["attributes"]
        return cls(organization_id=entity["id"], name=ea["name"], hostname=ea["hostname"])

    def to_api(self) -> JsonApiOrganizationInDocument:
        return JsonApiOrganizationInDocument(
            data=JsonApiOrganizationIn(
                id=self.id,
                attributes=JsonApiOrganizationInAttributes(name=self.name, hostname=self.hostname),
            )
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogOrganization):
            return False
        return self.id == other.id and self.name == other.name and self.hostname == other.hostname
