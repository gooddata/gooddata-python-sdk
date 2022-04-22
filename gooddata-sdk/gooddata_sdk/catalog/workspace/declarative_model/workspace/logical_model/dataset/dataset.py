# (C) 2022 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from typing import Any

from gooddata_metadata_client.model.data_source_table_identifier import DataSourceTableIdentifier
from gooddata_metadata_client.model.declarative_attribute import DeclarativeAttribute
from gooddata_metadata_client.model.declarative_dataset import DeclarativeDataset
from gooddata_metadata_client.model.declarative_fact import DeclarativeFact
from gooddata_metadata_client.model.declarative_label import DeclarativeLabel
from gooddata_metadata_client.model.declarative_reference import DeclarativeReference
from gooddata_sdk.catalog.entity import CatalogTitleEntity
from gooddata_sdk.catalog.identifier import CatalogGrainIdentifier, CatalogReferenceIdentifier
from gooddata_sdk.utils import read_layout_from_file, write_layout_to_file

LAYOUT_DATASETS_DIR = "datasets"


class CatalogDeclarativeDataset(CatalogTitleEntity):
    def __init__(
        self,
        id: str,
        title: str,
        grain: list[CatalogGrainIdentifier],
        references: list[CatalogDeclarativeReference],
        description: str = None,
        attributes: list[CatalogDeclarativeAttribute] = None,
        facts: list[CatalogDeclarativeFact] = None,
        data_source_table_id: CatalogDataSourceTableIdentifier = None,
        tags: list[str] = None,
    ):
        super(CatalogDeclarativeDataset, self).__init__(id, title)
        self.grain = grain
        self.references = references
        self.description = description
        self.attributes = attributes if attributes else []
        self.facts = facts if facts else []
        self.data_source_table_id = data_source_table_id
        self.tags = tags

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDeclarativeDataset:
        attributes = (
            [CatalogDeclarativeAttribute.from_api(v) for v in entity["attributes"]] if entity.get("attributes") else []
        )
        facts = [CatalogDeclarativeFact.from_api(v) for v in entity["facts"]] if entity.get("facts") else []
        data_source_table_id = (
            CatalogDataSourceTableIdentifier.from_api(entity["data_source_table_id"])
            if entity.get("data_source_table_id")
            else None
        )
        return cls(
            entity["id"],
            entity["title"],
            [CatalogGrainIdentifier.from_api(v) for v in entity["grain"]],
            [CatalogDeclarativeReference.from_api(v) for v in entity["references"]],
            entity.get("description"),
            attributes,
            facts,
            data_source_table_id,
            entity.get("tags"),
        )

    def to_api(self) -> DeclarativeDataset:
        kwargs: dict[str, Any] = {
            "facts": [v.to_api() for v in self.facts],
            "attributes": [v.to_api() for v in self.attributes],
        }
        if self.description:
            kwargs["description"] = self.description
        if self.data_source_table_id:
            kwargs["data_source_table_id"] = self.data_source_table_id.to_api()
        if self.tags:
            kwargs["tags"] = self.tags
        return DeclarativeDataset(
            self.id, self.title, [v.to_api() for v in self.grain], [v.to_api() for v in self.references], **kwargs
        )

    def store_to_disk(self, datasets_folder: Path) -> None:
        dataset_file = datasets_folder / f"{self.id}.yaml"
        write_layout_to_file(dataset_file, self.to_api().to_dict(camel_case=True))

    @classmethod
    def load_from_disk(cls, dataset_file: Path) -> CatalogDeclarativeDataset:
        dataset_layout = read_layout_from_file(dataset_file)
        return cls.from_dict(dataset_layout, camel_case=True)

    @classmethod
    def from_dict(cls, data: dict[str, Any], camel_case: bool = True) -> CatalogDeclarativeDataset:
        """
        :param data:    Data loaded for example from the file.
        :param camel_case:  True if the variable names in the input
                        data are serialized names as specified in the OpenAPI document.
                        False if the variables names in the input data are python
                        variable names in PEP-8 snake case.
        :return:    CatalogDeclarativeDataset object.
        """
        declarative_dataset = DeclarativeDataset.from_dict(data, camel_case)
        return cls.from_api(declarative_dataset)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogDeclarativeDataset):
            return False
        return (
            self.id == other.id
            and self.title == other.title
            and self.grain == other.grain
            and self.references == other.references
            and self.description == other.description
            and self.tags == other.tags
            and self.attributes == other.attributes
            and self.facts == other.facts
            and self.data_source_table_id == other.data_source_table_id
        )


class CatalogDeclarativeAttribute(CatalogTitleEntity):
    def __init__(
        self,
        id: str,
        title: str,
        labels: list[CatalogDeclarativeLabel],
        description: str = None,
        tags: list[str] = None,
    ):
        super(CatalogDeclarativeAttribute, self).__init__(id, title)
        self.labels = labels
        self.description = description
        self.tags = tags

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDeclarativeAttribute:
        return cls(
            entity["id"],
            entity["title"],
            [CatalogDeclarativeLabel.from_api(v) for v in entity["labels"]],
            entity.get("description"),
            entity.get("tags"),
        )

    def to_api(self) -> DeclarativeAttribute:
        kwargs: dict[str, Any] = dict()
        if self.description:
            kwargs["description"] = self.description
        if self.tags:
            kwargs["tags"] = self.tags
        return DeclarativeAttribute(self.id, self.title, [v.to_api() for v in self.labels], **kwargs)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogDeclarativeAttribute):
            return False
        return (
            self.id == other.id
            and self.title == other.title
            and self.labels == other.labels
            and self.description == other.description
            and self.tags == other.tags
        )


class CatalogDeclarativeFact(CatalogTitleEntity):
    def __init__(self, id: str, title: str, source_column: str, description: str = None, tags: list[str] = None):
        super(CatalogDeclarativeFact, self).__init__(id, title)
        self.source_column = source_column
        self.description = description
        self.tags = tags

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDeclarativeFact:
        return cls(
            entity["id"], entity["title"], entity["source_column"], entity.get("description"), entity.get("tags")
        )

    def to_api(self) -> DeclarativeFact:
        kwargs: dict[str, Any] = dict()
        if self.description:
            kwargs["description"] = self.description
        if self.tags:
            kwargs["tags"] = self.tags
        return DeclarativeFact(self.id, self.title, self.source_column, **kwargs)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogDeclarativeFact):
            return False
        return (
            self.id == other.id
            and self.title == other.title
            and self.source_column == other.source_column
            and self.description == other.description
            and self.tags == other.tags
        )


class CatalogDataSourceTableIdentifier:
    def __init__(self, id: str, data_source_id: str):
        self.id = id
        self.data_source_id = data_source_id

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDataSourceTableIdentifier:
        return cls(entity["id"], entity["data_source_id"])

    def to_api(self) -> DataSourceTableIdentifier:
        return DataSourceTableIdentifier(self.id, self.data_source_id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogDataSourceTableIdentifier):
            return False
        return self.id == other.id and self.data_source_id == other.data_source_id


class CatalogDeclarativeLabel(CatalogTitleEntity):
    def __init__(
        self,
        id: str,
        title: str,
        primary: bool,
        source_column: str,
        description: str = None,
        tags: list[str] = None,
        value_type: str = None,
    ):
        super(CatalogDeclarativeLabel, self).__init__(id, title)
        self.id = id
        self.title = title
        self.primary = primary
        self.source_column = source_column
        self.description = description
        self.tags = tags
        self.value_type = value_type

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDeclarativeLabel:
        return cls(
            entity["id"],
            entity["title"],
            entity["primary"],
            entity["source_column"],
            entity.get("description"),
            entity.get("tags"),
            entity.get("value_type"),
        )

    def to_api(self) -> DeclarativeLabel:
        kwargs: dict[str, Any] = dict()
        if self.description:
            kwargs["description"] = self.description
        if self.tags:
            kwargs["tags"] = self.tags
        if self.value_type:
            kwargs["value_type"] = self.value_type
        return DeclarativeLabel(self.id, self.title, self.primary, self.source_column, **kwargs)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogDeclarativeLabel):
            return False
        return (
            self.id == other.id
            and self.title == other.title
            and self.primary == other.primary
            and self.source_column == other.source_column
            and self.description == other.description
            and self.tags == other.tags
            and self.value_type == other.value_type
        )


class CatalogDeclarativeReference:
    def __init__(self, identifier: CatalogReferenceIdentifier, multi_value: bool, source_columns: list[str]):
        self.identifier = identifier
        self.multi_value = multi_value
        self.source_columns = source_columns

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDeclarativeReference:
        return cls(
            CatalogReferenceIdentifier.from_api(entity["identifier"]), entity["multivalue"], entity["source_columns"]
        )

    def to_api(self) -> DeclarativeReference:
        return DeclarativeReference(self.identifier.to_api(), self.multi_value, self.source_columns)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogDeclarativeReference):
            return False
        return (
            self.identifier == other.identifier
            and self.multi_value == other.multi_value
            and self.source_columns == other.source_columns
        )
