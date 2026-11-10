# (C) 2022 GoodData Corporation
from __future__ import annotations

import builtins
import keyword
from typing import Any, TypeVar

from attrs import Attribute, define, field, fields, has
from cattrs import structure

from gooddata_sdk.utils import AllPagedEntities

T = TypeVar("T", bound="Base")
U = TypeVar("U", bound="JsonApiEntityBase")


def value_in_allowed(instance: type[Base], attribute: Attribute, value: str, client_class: Any | None = None) -> None:
    if client_class is None:
        client_class = instance.client_class()
    allowed_values = client_class.allowed_values.get((attribute.name,))
    if allowed_values is not None and value not in list(allowed_values.values()):
        raise ValueError(
            f"Allowed values for attribute {attribute.name} are: {', '.join(list(allowed_values.values()))}. "
            f"But value {value} was passed."
        )


def _client_attribute_name(name: str) -> str:
    """
    Returns the generated client's attribute name for an attrs attribute name.

    The client prefixes a keyword-named attribute with an underscore (``_from``); attrs code suffixes it (``from_``).
    """
    if name.endswith("_") and keyword.iskeyword(name[:-1]):
        return f"_{name[:-1]}"
    return name


@define
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
    def _is_attribute_private(attribute: Attribute) -> bool:
        return attribute.name.startswith("_")

    def _get_snake_dict(self) -> dict[str, Any]:
        """
        Converts object into a snake_case dictionary keyed by the generated client's attribute names.

        Attributes that are None or private are left out at every depth. An attribute named after a Python keyword
        plus a trailing underscore (``from_``) is written under the client's name for it (``_from``); keys inside a
        ``dict`` value are user data and are never renamed.
        """
        return self._snake_value(self)

    @classmethod
    def _snake_value(cls, value: Any) -> Any:
        if has(type(value)):
            dictionary: dict[str, Any] = {}
            for attribute in fields(type(value)):
                attribute_value = getattr(value, attribute.name)
                if attribute_value is None or cls._is_attribute_private(attribute):
                    continue
                dictionary[_client_attribute_name(attribute.name)] = cls._snake_value(attribute_value)
            return dictionary
        if isinstance(value, dict):
            return {key: cls._snake_value(item) for key, item in value.items()}
        if isinstance(value, (list, tuple, set, frozenset)):
            return [cls._snake_value(item) for item in value]
        return value

    @staticmethod
    def client_class() -> Any:
        return NotImplemented

    def to_api(self) -> Any:
        dictionary = self._get_snake_dict()
        return self.client_class().from_dict(dictionary, camel_case=False)


@define
class JsonApiEntityBase:
    id: str
    type: str
    attributes: dict[str, Any] = field(repr=False)
    relationships: dict[str, Any] | None = field(repr=False, default=None)
    meta: dict[str, Any] | None = field(repr=False, default=None)
    links: dict[str, Any] | None = field(repr=False, default=None)
    related_entities_data: list[dict[str, Any]] = field(repr=False, factory=list)
    related_entities_side_loads: list[dict[str, Any]] = field(repr=False, factory=list)
    side_loads: list[dict[str, Any]] = field(repr=False, factory=list)

    @classmethod
    def from_api(
        cls,
        entity: dict[str, Any],
        side_loads: list[Any] | None = None,
        related_entities: AllPagedEntities | None = None,
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
