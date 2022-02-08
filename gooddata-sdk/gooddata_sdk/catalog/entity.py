# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any, Optional

from gooddata_sdk.compute.model.base import ObjId


class CatalogEntity:
    def __init__(self, entity: dict[str, Any]) -> None:
        self._e = entity["attributes"]
        self._entity = entity
        self._obj_id = ObjId(self._entity["id"], type=self._entity["type"])

    @property
    def id(self) -> str:
        return self._entity["id"]

    @property
    def type(self) -> str:
        return self._entity["type"]

    @property
    def title(self) -> Optional[str]:
        # Optional, not all metadata objects contain title
        return self._e.get("title")

    @property
    def description(self) -> Optional[str]:
        # Optional, not all metadata objects contain description
        return self._e.get("description")

    @property
    def obj_id(self) -> ObjId:
        return self._obj_id

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, title={self.title})"


# TODO - rewrite to data classes once it is possible
# 1. Inheritance does not work, if attributes with defaults are used in parents
#   https://stackoverflow.com/questions/51575931/class-inheritance-in-python-3-7-dataclasses
#   fixed in Python 3.10, but now we have to support older python versions
# 2. Generated attributes are not detected consistently in Sphinx, DOC generation fails
class CatalogNameEntity:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
