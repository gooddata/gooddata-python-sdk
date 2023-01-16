# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any, Optional, Union, cast

from gooddata_sdk.catalog.entity import CatalogEntity
from gooddata_sdk.catalog.types import ValidObjects
from gooddata_sdk.compute.model.attribute import Attribute
from gooddata_sdk.compute.model.base import ObjId
from gooddata_sdk.compute.model.metric import Metric, SimpleMetric
from gooddata_sdk.utils import IdObjType, id_obj_to_key


class CatalogAttribute(CatalogEntity):
    def __init__(self, entity: dict[str, Any], labels: list[CatalogLabel]) -> None:
        super(CatalogAttribute, self).__init__(entity)

        self._labels = labels
        self._labels_idx = dict([(str(label.obj_id), label) for label in labels])
        self._dataset: Optional[CatalogDataset] = None

    @property
    def labels(self) -> list[CatalogLabel]:
        return self._labels

    @property
    def dataset(self) -> CatalogDataset:
        if self._dataset is None:
            # Attribute needs link to dataset but dataset is created after all CatalogAttribute instances
            # it is responsibility of CatalogDataset instance to set link to itself
            raise ValueError("Uninitialized dataset value")
        else:
            return self._dataset

    @dataset.setter
    def dataset(self, value: CatalogDataset) -> None:
        self._dataset = value

    @property
    def granularity(self) -> Union[str, None]:
        return self._e["granularity"] if "granularity" in self._e else None

    def primary_label(self) -> Union[CatalogLabel, None]:
        # use cast as mypy is not applying next, it claims, type is filter[CatalogLabel]
        return cast(Union[CatalogLabel, None], next(filter(lambda x: x.primary, self.labels), None))

    def find_label(self, id_obj: IdObjType) -> Union[CatalogLabel, None]:
        obj_key = id_obj_to_key(id_obj)

        return self._labels_idx[obj_key] if obj_key in self._labels_idx else None

    def as_computable(self) -> Attribute:
        primary_label = self.primary_label()

        if primary_label is not None:
            return primary_label.as_computable()

        # cannot even write meaningful error here. cannot create attribute from attribute? :D
        raise ValueError()

    def __repr__(self) -> str:
        return f"CatalogAttribute(id={self.id}, title={self.title}, labels={self.labels})"


class CatalogLabel(CatalogEntity):
    @property
    def primary(self) -> bool:
        return "primary" in self._e and self._e["primary"]

    def as_computable(self) -> Attribute:
        return Attribute(local_id=self.id, label=self.id)


class CatalogFact(CatalogEntity):
    def as_computable(self) -> Metric:
        return SimpleMetric(local_id=self.id, item=ObjId(self.id, "fact"))


class CatalogDataset(CatalogEntity):
    def __init__(self, entity: dict[str, Any], attributes: list[CatalogAttribute], facts: list[CatalogFact]) -> None:
        super(CatalogDataset, self).__init__(entity)
        self._attributes = attributes
        self._facts = facts

        for attr in self.attributes:
            attr.dataset = self

    @property
    def data_type(self) -> str:
        return self._e["type"]

    @property
    def attributes(self) -> list[CatalogAttribute]:
        return self._attributes

    @property
    def facts(self) -> list[CatalogFact]:
        return self._facts

    def find_label_attribute(self, id_obj: IdObjType) -> Union[CatalogAttribute, None]:
        for attr in self._attributes:
            if attr.find_label(id_obj) is not None:
                return attr

        return None

    def filter_dataset(self, valid_objects: ValidObjects) -> Union[CatalogDataset, None]:
        """
        Filters dataset so that it contains only attributes and facts that are part of the provided valid objects
        structure.

        :param valid_objects: mapping of object type to a set of valid object ids
        :return: CatalogDataset containing only valid attributes and facts; None if all of the attributes and facts
                 were filtered out
        """
        new_attributes = [a for a in self.attributes if a.id in valid_objects[a.type]]
        new_facts = [f for f in self.facts if f.id in valid_objects[f.type]]

        if not len(new_attributes) and not len(new_facts):
            return None

        return CatalogDataset(self._entity, new_attributes, new_facts)

    def __repr__(self) -> str:
        return f"CatalogDataset(id={self.id}, title={self.title}, facts={self.facts}, attributes={self.attributes})"
