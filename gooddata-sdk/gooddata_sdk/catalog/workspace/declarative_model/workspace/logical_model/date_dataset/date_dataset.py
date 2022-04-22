# (C) 2022 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from typing import Any

from gooddata_metadata_client.model.declarative_date_dataset import DeclarativeDateDataset
from gooddata_metadata_client.model.granularities_formatting import GranularitiesFormatting
from gooddata_sdk.catalog.entity import CatalogTitleEntity
from gooddata_sdk.utils import read_layout_from_file, write_layout_to_file

LAYOUT_DATE_INSTANCES_DIR = "date_instances"


class CatalogDeclarativeDateDataset(CatalogTitleEntity):
    def __init__(
        self,
        id: str,
        title: str,
        granularities_formatting: CatalogGranularitiesFormatting,
        granularities: list[str],
        description: str = None,
        tags: list[str] = None,
    ):
        super(CatalogDeclarativeDateDataset, self).__init__(id, title)
        self.granularities_formatting = granularities_formatting
        self.granularities = granularities
        self.description = description
        self.tags = tags

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDeclarativeDateDataset:
        return cls(
            entity["id"],
            entity["title"],
            CatalogGranularitiesFormatting.from_api(entity["granularities_formatting"]),
            entity["granularities"],
            entity.get("description"),
            entity.get("tags"),
        )

    def to_api(self) -> DeclarativeDateDataset:
        kwargs: dict[str, Any] = dict()
        if self.description is not None:
            kwargs["description"] = self.description
        if self.tags is not None:
            kwargs["tags"] = self.tags
        return DeclarativeDateDataset(
            self.id, self.title, self.granularities_formatting.to_api(), self.granularities, **kwargs
        )

    def store_to_disk(self, date_instances_folder: Path) -> None:
        date_instance_file = date_instances_folder / f"{self.id}.yaml"
        write_layout_to_file(date_instance_file, self.to_api().to_dict(camel_case=True))

    @classmethod
    def load_from_disk(cls, date_instance_file: Path) -> CatalogDeclarativeDateDataset:
        date_instance_layout = read_layout_from_file(date_instance_file)
        return cls.from_dict(date_instance_layout, camel_case=True)

    @classmethod
    def from_dict(cls, data: dict[str, Any], camel_case: bool = True) -> CatalogDeclarativeDateDataset:
        """
        :param data:    Data loaded for example from the file.
        :param camel_case:  True if the variable names in the input
                        data are serialized names as specified in the OpenAPI document.
                        False if the variables names in the input data are python
                        variable names in PEP-8 snake case.
        :return:    CatalogDeclarativeDateDataset object.
        """
        declarative_date_dataset = DeclarativeDateDataset.from_dict(data, camel_case)
        return cls.from_api(declarative_date_dataset)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogDeclarativeDateDataset):
            return False
        return (
            self.id == other.id
            and self.title == other.title
            and self.granularities_formatting == other.granularities_formatting
            and self.granularities == other.granularities
            and self.description == other.description
            and self.tags == other.tags
        )


class CatalogGranularitiesFormatting:
    def __init__(self, title_base: str, title_pattern: str):
        self.title_base = title_base
        self.title_pattern = title_pattern

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogGranularitiesFormatting:
        return cls(entity["title_base"], entity["title_pattern"])

    def to_api(self) -> GranularitiesFormatting:
        return GranularitiesFormatting(self.title_base, self.title_pattern)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogGranularitiesFormatting):
            return False
        return self.title_base == other.title_base and self.title_pattern == other.title_pattern
