# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any, Dict, Optional, Type, TypeVar

import attr
from cattrs import structure

T = TypeVar("T", bound="Base")


def value_in_allowed(
    instance: Type[Base], attribute: attr.Attribute, value: str, client_class: Optional[Any] = None
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
    def from_api(cls: Type[T], entity: Dict[str, Any]) -> T:
        """
        Creates object from entity passed by client class, which represents it as dictionary.
        """
        return structure(entity, cls)

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any], camel_case: bool = True) -> T:
        """
        Creates object from dictionary. It needs to be specified if the dictionary is in camelCase or snake_case.
        """
        # This branch does not have to exist, but in case of camel_case=False it can perform fewer calls
        if not camel_case:
            return structure(data, cls)
        client_object = cls.client_class().from_dict(data, camel_case)
        return cls.from_api(client_object)

    def to_dict(self, camel_case: bool = True) -> Dict[str, Any]:
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

    def _get_snake_dict(self) -> Dict[str, Any]:
        return attr.asdict(
            self, filter=lambda attribute, value: value is not None and not self._is_attribute_private(attribute)
        )

    @staticmethod
    def client_class() -> Any:
        return NotImplemented

    def to_api(self) -> Any:
        dictionary = self._get_snake_dict()
        return self.client_class().from_dict(dictionary, camel_case=False)
