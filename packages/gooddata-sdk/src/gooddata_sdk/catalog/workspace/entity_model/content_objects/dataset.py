# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any, Optional, Union, cast

import attr
import attrs
from gooddata_api_client.model.json_api_attribute_out import JsonApiAttributeOut
from gooddata_api_client.model.json_api_dataset_out import JsonApiDatasetOut
from gooddata_api_client.model.json_api_fact_out import JsonApiFactOut
from gooddata_api_client.model.json_api_label_out import JsonApiLabelOut

from gooddata_sdk.catalog.entity import AttrCatalogEntity
from gooddata_sdk.catalog.types import ValidObjects
from gooddata_sdk.compute.model.attribute import Attribute
from gooddata_sdk.compute.model.metric import Metric, SimpleMetric
from gooddata_sdk.utils import IdObjType, id_obj_to_key, safeget, safeget_list


@attr.s(auto_attribs=True, kw_only=True)
class CatalogLabel(AttrCatalogEntity):
    @staticmethod
    def client_class() -> Any:
        return JsonApiLabelOut

    @property
    def primary(self) -> bool:
        return safeget(self.json_api_attributes, ["primary"])

    @property
    def value_type(self) -> bool:
        return safeget(self.json_api_attributes, ["valueType"])

    def as_computable(self) -> Attribute:
        return Attribute(local_id=self.id, label=self.id)

    # TODO - attribute_id? dataset?


@attr.s(auto_attribs=True, kw_only=True)
class CatalogAttribute(AttrCatalogEntity):
    @staticmethod
    def client_class() -> Any:
        return JsonApiAttributeOut

    @property
    def labels(self) -> list[CatalogLabel]:
        related_label_ids = [x.get("id") for x in (safeget_list(self.json_api_relationships, ["labels", "data"]))]
        return [
            CatalogLabel.from_api(sl)
            for sl in self.json_api_side_loads
            if sl["type"] == "label" and sl["id"] in related_label_ids
        ]

    @property
    def dataset(self) -> CatalogDataset:
        related_dataset_id = safeget(self.json_api_relationships, ["dataset", "data", "id"])
        sl_dataset = next(
            iter([d for d in self.json_api_side_loads if d["type"] == "dataset" and d["id"] == related_dataset_id])
        )
        return CatalogDataset.from_api(sl_dataset)

    @property
    def granularity(self) -> Union[str, None]:
        return self.json_api_attributes.get("granularity")

    def primary_label(self) -> Union[CatalogLabel, None]:
        # use cast as mypy is not applying next, it claims, type is filter[CatalogLabel]
        return cast(Union[CatalogLabel, None], next(filter(lambda x: x.primary, self.labels), None))

    def find_label(self, id_obj: IdObjType) -> Union[CatalogLabel, None]:
        obj_key = id_obj_to_key(id_obj)
        # use cast as mypy is not applying next, it claims, type is filter[CatalogLabel]
        return cast(
            Union[CatalogLabel, None], next(filter(lambda x: id_obj_to_key(x.obj_id) == obj_key, self.labels), None)
        )

    # TODO add missing properties

    def as_computable(self) -> Attribute:
        primary_label = self.primary_label()

        if primary_label is not None:
            return primary_label.as_computable()

        # cannot even write meaningful error here. cannot create attribute from attribute? :D
        raise ValueError()


@attr.s(auto_attribs=True, kw_only=True)
class CatalogFact(AttrCatalogEntity):
    @staticmethod
    def client_class() -> Any:
        return JsonApiFactOut

    def as_computable(self) -> Metric:
        return SimpleMetric(local_id=self.id, item=self.obj_id)

    # TODO - dataset?


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDataset(AttrCatalogEntity):
    @property
    def dataset_type(self) -> str:
        return self.json_api_attributes["type"]

    def generate_attributes_from_api(self) -> list[CatalogAttribute]:
        related_attribute_ids = [x.get("id") for x in safeget_list(self.json_api_relationships, ["attributes", "data"])]
        related_attributes = [
            CatalogAttribute.from_api(x, side_loads=self.json_api_related_entities_side_loads)
            for x in self.json_api_related_entities_data
            if x["id"] in related_attribute_ids
        ]
        return related_attributes

    attributes: list[CatalogAttribute] = attr.field(
        repr=False,
        default=attr.Factory(lambda self: self.generate_attributes_from_api(), takes_self=True),
    )

    def generate_facts_from_api(self) -> list[CatalogFact]:
        related_fact_ids = [x.get("id") for x in safeget_list(self.json_api_relationships, ["facts", "data"])]
        return [
            CatalogFact.from_api(sl)
            for sl in self.json_api_side_loads
            if sl["type"] == "fact" and sl["id"] in related_fact_ids
        ]

    facts: list[CatalogFact] = attr.field(
        repr=False,
        default=attr.Factory(lambda self: self.generate_facts_from_api(), takes_self=True),
    )

    grain: Optional[list] = attr.field(
        default=attr.Factory(lambda self: self.json_api_attributes.get("grain"), takes_self=True)
    )
    reference_properties: Optional[list] = attr.field(
        default=attr.Factory(lambda self: self.json_api_attributes.get("referenceProperties"), takes_self=True)
    )
    data_source_table_id: Optional[str] = attr.field(
        default=attr.Factory(lambda self: self.json_api_attributes.get("dataSourceTableId"), takes_self=True)
    )
    data_source_table_path: Optional[list] = attr.field(
        default=attr.Factory(lambda self: self.json_api_attributes.get("dataSourceTablePath"), takes_self=True)
    )
    sql: Optional[dict] = attr.field(
        default=attr.Factory(lambda self: self.json_api_attributes.get("sql"), takes_self=True)
    )
    are_relations_valid: Optional[bool] = attr.field(
        default=attr.Factory(lambda self: self.json_api_attributes.get("areRelationsValid"), takes_self=True)
    )
    workspace_data_filter_columns: Optional[list] = attr.field(
        default=attr.Factory(lambda self: self.json_api_attributes.get("workspaceDataFilterColumns"), takes_self=True)
    )
    workspace_data_filter_references: Optional[list] = attr.field(
        default=attr.Factory(
            lambda self: self.json_api_attributes.get("workspaceDataFilterReferences"), takes_self=True
        )
    )

    @staticmethod
    def client_class() -> Any:
        return JsonApiDatasetOut

    def find_label_attribute(self, id_obj: IdObjType) -> Union[CatalogAttribute, None]:
        for attribute in self.attributes:
            if attribute.find_label(id_obj) is not None:
                return attribute

        return None

    def filter_dataset(self, valid_objects: ValidObjects) -> Optional[CatalogDataset]:
        """
        Filters dataset so that it contains only attributes and facts that are part of the provided valid objects
        structure.

        Args:
            valid_objects (ValidObjects):
                list of valid object IDs for each object type. They are valid for existing report context.

        Returns:
            CatalogDataset:
                copy of self modified by the valid_objects context.
        """
        new_attributes = [a for a in self.attributes if a.id in valid_objects[a.type]]
        new_facts = [f for f in self.facts if f.id in valid_objects[f.type]]
        return (
            None
            if len(new_facts) == 0 and len(new_attributes) == 0
            else attrs.evolve(
                self,
                attributes=new_attributes,
                facts=new_facts,
            )
        )
