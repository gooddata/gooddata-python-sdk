# (C) 2022 GoodData Corporation
from __future__ import annotations

import base64
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Optional, Type, TypeVar

import attr

from gooddata_sdk.catalog.base import Base, JsonApiEntityBase
from gooddata_sdk.compute.model.base import ObjId
from gooddata_sdk.utils import AllPagedEntities

T = TypeVar("T", bound="AttrCatalogEntity")


@attr.s(auto_attribs=True)
class AttrCatalogEntity:
    json_api_entity: JsonApiEntityBase
    id: str
    type: str
    obj_id: ObjId
    title: Optional[str]
    description: Optional[str]
    tags: Optional[List[str]]

    @classmethod
    def from_api(
        cls: Type[T],
        entity: Dict[str, Any],
        side_loads: Optional[List[Any]] = None,
        related_entities: Optional[AllPagedEntities] = None,
    ) -> T:
        """
        Creates GoodData object from AttrCatalogEntityJsonApi.
        """
        json_api_entity = JsonApiEntityBase.from_api(entity, side_loads, related_entities)
        return cls(
            json_api_entity=json_api_entity,
            id=json_api_entity.id,
            type=json_api_entity.type,
            obj_id=ObjId(json_api_entity.id, type=json_api_entity.type),
            title=json_api_entity.attributes.get("title"),
            description=json_api_entity.attributes.get("description"),
            tags=json_api_entity.attributes.get("tags", []),
        )


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


@attr.s(auto_attribs=True, kw_only=True)
class Credentials(Base):
    TOKEN_KEY: ClassVar[str] = "token"
    USER_KEY: ClassVar[str] = "username"
    PASSWORD_KEY: ClassVar[str] = "password"

    def to_api_args(self) -> dict[str, Any]:
        return attr.asdict(self)

    @classmethod
    def is_part_of_api(cls, entity: dict[str, Any]) -> bool:
        return NotImplemented

    @classmethod
    def create(cls, creds_classes: list[Type[Credentials]], entity: dict[str, Any]) -> Credentials:
        for creds_class in creds_classes:
            if creds_class.is_part_of_api(entity):
                return creds_class.from_api(entity)

        raise ValueError("No supported credentials found")

    @classmethod
    def validate_instance(cls, creds_classes: list[Type[Credentials]], instance: Credentials) -> None:
        passed = isinstance(instance, tuple(creds_classes))
        if not passed:
            classes_as_str = ",".join([str(creds_class) for creds_class in creds_classes])
            raise ValueError(f"Unsupported credentials type. Pick one of {classes_as_str}")


@attr.s(auto_attribs=True, kw_only=True)
class TokenCredentials(Credentials):
    token: str = attr.field(repr=lambda value: "***")

    @classmethod
    def is_part_of_api(cls, entity: dict[str, Any]) -> bool:
        return cls.USER_KEY not in entity

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> TokenCredentials:
        # Credentials are not returned for security reasons
        return cls(token="")


@attr.s(auto_attribs=True, kw_only=True)
class TokenCredentialsFromFile(Credentials):
    file_path: Path
    token: str = attr.field(init=False, repr=lambda value: "***")

    def __attrs_post_init__(self) -> None:
        self.token = self.token_from_file(self.file_path)

    def to_api_args(self) -> dict[str, Any]:
        return {self.TOKEN_KEY: self.token}

    @classmethod
    def is_part_of_api(cls, entity: dict[str, Any]) -> bool:
        return cls.USER_KEY not in entity

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> TokenCredentialsFromFile:
        # Credentials are not returned for security reasons
        raise NotImplementedError

    @staticmethod
    def token_from_file(file_path: Path) -> str:
        with open(file_path, "rb") as fp:
            return base64.b64encode(fp.read()).decode("utf-8")


@attr.s(auto_attribs=True, kw_only=True)
class BasicCredentials(Credentials):
    username: str
    password: str = attr.field(repr=lambda value: "***")

    @classmethod
    def is_part_of_api(cls, entity: dict[str, Any]) -> bool:
        return cls.USER_KEY in entity

    @classmethod
    def from_api(cls, attributes: dict[str, Any]) -> BasicCredentials:
        # Credentials are not returned from security reasons
        return cls(
            username=attributes[cls.USER_KEY],
            # Password is not returned from API (security)
            # You have to fill it to keep it or update it
            password="",
        )
