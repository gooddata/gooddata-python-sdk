# (C) 2022 GoodData Corporation
from __future__ import annotations

import builtins
from typing import Any, Optional, TypeVar

import attr
from cattrs import structure

from gooddata_sdk.utils import AllPagedEntities

T = TypeVar("T", bound="Base")
U = TypeVar("U", bound="JsonApiEntityBase")


def value_in_allowed(
    instance: type[Base], attribute: attr.Attribute, value: str, client_class: Optional[Any] = None
) -> None:
    if client_class is None:
        client_class = instance.client_class()
    allowed_values = client_class.allowed_values.get((attribute.name,))
    if allowed_values is not None and value not in list(allowed_values.values()):
        raise ValueError(
            f"Allowed values for attribute {attribute.name} are: {', '.join(list(allowed_values.values()))}. "
            f"But value {value} was passed."
        )


@attr.s
class Base:
    @classmethod
    def from_api(cls: type[T], entity: dict[str, Any]) -> T:
        """
        Creates object from entity passed by client class, which represents it as dictionary.
        """
        return structure(entity, cls)

    @classmethod
    def from_dict(cls: type[T], data: dict[str, Any], camel_case: bool = True) -> T:
        """
        Creates object from dictionary. It needs to be specified if the dictionary is in camelCase or snake_case.
        """
        if camel_case:
            data = cls.client_class().from_dict(data, camel_case).to_dict()
        return structure(data, cls)

    def to_dict(self, camel_case: bool = True) -> dict[str, Any]:
        """
        Converts object into dictionary. Optional argument if the dictionary should be camelCase or snake_case can be
        specified.
        """
        # This branch does not have to exist, but in case of camel_case=False it can perform fewer calls
        if not camel_case:
            return self._get_snake_dict()
        return self.to_api().to_dict(camel_case)

    @staticmethod
    def _is_attribute_private(attribute: attr.Attribute) -> bool:
        return attribute.name.startswith("_")

    def _get_snake_dict(self) -> dict[str, Any]:
        return attr.asdict(
            self, filter=lambda attribute, value: value is not None and not self._is_attribute_private(attribute)
        )

    @staticmethod
    def client_class() -> Any:
        return NotImplemented

    def to_api(self) -> Any:
        dictionary = self._get_snake_dict()
        return self.client_class().from_dict(dictionary, camel_case=False)


@attr.s(auto_attribs=True)
class JsonApiEntityBase:
    id: str
    type: str
    attributes: dict[str, Any] = attr.field(repr=False)
    relationships: Optional[dict[str, Any]] = attr.field(repr=False, default=None)
    meta: Optional[dict[str, Any]] = attr.field(repr=False, default=None)
    links: Optional[dict[str, Any]] = attr.field(repr=False, default=None)
    related_entities_data: list[dict[str, Any]] = attr.field(repr=False, default=list)
    related_entities_side_loads: list[dict[str, Any]] = attr.field(repr=False, default=list)
    side_loads: list[dict[str, Any]] = attr.field(repr=False, default=list)

    @classmethod
    def from_api(
        cls,
        entity: dict[str, Any],
        side_loads: Optional[list[Any]] = None,
        related_entities: Optional[AllPagedEntities] = None,
    ) -> JsonApiEntityBase:
        """
        Creates object from entity passed by client class, which represents it as dictionary.
        """
        entity["side_loads"] = side_loads or []
        entity["related_entities_data"] = related_entities.data if related_entities else []
        entity["related_entities_side_loads"] = related_entities.included if related_entities else []
        return structure(entity, cls)

    @classmethod
    def from_dict(cls: builtins.type[U], data: dict[str, Any]) -> U:
        return NotImplemented

    @staticmethod
    def to_dict() -> dict[str, Any]:
        return NotImplemented

    @staticmethod
    def to_api() -> Any:
        return NotImplemented

    @staticmethod
    def client_class() -> Any:
        return NotImplemented
