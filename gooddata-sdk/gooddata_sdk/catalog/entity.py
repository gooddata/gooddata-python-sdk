# (C) 2022 GoodData Corporation
from __future__ import annotations

import base64
from pathlib import Path
from typing import Any, ClassVar, Optional, Type, TypeVar

import attr

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.compute.model.base import ObjId

T = TypeVar("T", bound="CatalogTypeEntity")
U = TypeVar("U", bound="CatalogTitleEntity")


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

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"


class CatalogTypeEntity:
    def __init__(self, id: str, type: str):
        self.id = id
        self.type = type

    @classmethod
    def from_api(cls: Type[T], entity: dict[str, Any]) -> T:
        return cls(
            entity["id"],
            entity["type"],
        )

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, type={self.type})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id and self.type == other.type


class CatalogTitleEntity:
    def __init__(self, id: str, title: str):
        self.id = id
        self.title = title

    @classmethod
    def from_api(cls: Type[U], entity: dict[str, Any]) -> U:
        return cls(
            entity["id"],
            entity["title"],
        )

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, title={self.title})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id and self.title == other.title


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
