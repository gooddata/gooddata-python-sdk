# (C) 2026 GoodData Corporation
from __future__ import annotations

from attrs import define
from gooddata_api_client.model.json_api_computed_attribute_in import JsonApiComputedAttributeIn
from gooddata_api_client.model.json_api_computed_attribute_in_attributes import JsonApiComputedAttributeInAttributes
from gooddata_api_client.model.json_api_computed_attribute_in_attributes_content import (
    JsonApiComputedAttributeInAttributesContent,
)
from gooddata_api_client.model.json_api_computed_attribute_in_document import JsonApiComputedAttributeInDocument
from gooddata_api_client.model.json_api_computed_attribute_post_optional_id import (
    JsonApiComputedAttributePostOptionalId,
)
from gooddata_api_client.model.json_api_computed_attribute_post_optional_id_document import (
    JsonApiComputedAttributePostOptionalIdDocument,
)

from gooddata_sdk.catalog.base import Base


@define(kw_only=True)
class CatalogComputedAttributeDocument(Base):
    data: CatalogComputedAttribute

    @staticmethod
    def client_class() -> type[JsonApiComputedAttributeInDocument]:
        return JsonApiComputedAttributeInDocument

    def to_api(self) -> JsonApiComputedAttributeInDocument:
        return JsonApiComputedAttributeInDocument(data=self.data.to_api())


@define(kw_only=True)
class CatalogComputedAttributePostDocument(Base):
    """Request body of the create (POST) endpoint, where the id is optional.

    Unlike filter views, computed attributes have a dedicated POST schema: the backend
    generates the id when it is omitted, so the create endpoint takes this document and
    only the update (PUT) endpoint takes CatalogComputedAttributeDocument.
    """

    data: CatalogComputedAttribute

    @staticmethod
    def client_class() -> type[JsonApiComputedAttributePostOptionalIdDocument]:
        return JsonApiComputedAttributePostOptionalIdDocument

    def to_api(self) -> JsonApiComputedAttributePostOptionalIdDocument:
        return JsonApiComputedAttributePostOptionalIdDocument(data=self.data.to_post_api())


@define(kw_only=True)
class CatalogComputedAttribute(Base):
    # None only when creating a computed attribute whose id the backend generates.
    id: str | None = None
    attributes: CatalogComputedAttributeAttributes

    @staticmethod
    def client_class() -> type[JsonApiComputedAttributeIn]:
        return JsonApiComputedAttributeIn

    @classmethod
    def init(
        cls,
        maql: str,
        computed_attribute_id: str | None = None,
        title: str | None = None,
        description: str | None = None,
        format: str | None = None,
        metric_type: str | None = None,
        data_type: str | None = None,
        locale: str | None = None,
        value_type: str | None = None,
        is_hidden: bool | None = None,
        is_nullable: bool | None = None,
        null_value: str | None = None,
        tags: list[str] | None = None,
        are_relations_valid: bool | None = None,
    ) -> CatalogComputedAttribute:
        attributes = CatalogComputedAttributeAttributes(
            content=CatalogComputedAttributeContent(maql=maql, format=format, metric_type=metric_type),
            title=title,
            description=description,
            data_type=data_type,
            locale=locale,
            value_type=value_type,
            is_hidden=is_hidden,
            is_nullable=is_nullable,
            null_value=null_value,
            tags=tags,
            are_relations_valid=are_relations_valid,
        )
        return cls(id=computed_attribute_id, attributes=attributes)

    def to_api(self) -> JsonApiComputedAttributeIn:
        if self.id is None:
            raise ValueError("Computed attribute id is required for an update, use to_post_api() to create one.")
        return JsonApiComputedAttributeIn(id=self.id, attributes=self.attributes.to_api())

    def to_post_api(self) -> JsonApiComputedAttributePostOptionalId:
        optional_id = {} if self.id is None else {"id": self.id}
        return JsonApiComputedAttributePostOptionalId(attributes=self.attributes.to_api(), **optional_id)


@define(kw_only=True)
class CatalogComputedAttributeAttributes(Base):
    content: CatalogComputedAttributeContent
    title: str | None = None
    description: str | None = None
    data_type: str | None = None
    locale: str | None = None
    value_type: str | None = None
    is_hidden: bool | None = None
    is_nullable: bool | None = None
    null_value: str | None = None
    tags: list[str] | None = None
    are_relations_valid: bool | None = None

    @staticmethod
    def client_class() -> type[JsonApiComputedAttributeInAttributes]:
        return JsonApiComputedAttributeInAttributes


@define(kw_only=True)
class CatalogComputedAttributeContent(Base):
    maql: str
    format: str | None = None
    metric_type: str | None = None

    @staticmethod
    def client_class() -> type[JsonApiComputedAttributeInAttributesContent]:
        return JsonApiComputedAttributeInAttributesContent
