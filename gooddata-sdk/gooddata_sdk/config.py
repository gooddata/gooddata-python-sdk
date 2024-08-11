# (C) 2024 GoodData Corporation
import os
from typing import Any, Optional, TypeVar

import attrs
from attrs import define
from cattrs import structure
from cattrs.errors import ClassValidationError
from dotenv import load_dotenv

T = TypeVar("T", bound="ConfigBase")


@define
class ConfigBase:
    def to_dict(self) -> dict[str, str]:
        return attrs.asdict(self)

    @classmethod
    def from_dict(cls: type[T], data: dict[str, Any]) -> T:
        return structure(data, cls)

    @classmethod
    def can_structure(cls: type[T], data: dict[str, Any]) -> bool:
        try:
            cls.from_dict(data)
            return True
        except ClassValidationError:
            return False


@define
class Profile(ConfigBase):
    host: str
    token: str
    custom_headers: Optional[dict[str, str]] = None
    extra_user_agent: Optional[str] = None

    def to_dict(self, use_env: bool = False) -> dict[str, str]:
        load_dotenv()
        if not use_env:
            return attrs.asdict(self)
        env_var = self.token[1:]
        if env_var not in os.environ:
            raise ValueError(f"Environment variable {env_var} not found")
        return {**attrs.asdict(self), "token": os.environ[env_var]}


@define
class AacConfig(ConfigBase):
    profiles: dict[str, Profile]
    default_profile: str
    access: dict[str, str]

    def ds_credentials(self) -> dict[str, str]:
        load_dotenv()
        return {k: os.environ.get(v[1:], v) for k, v in self.access.items()}
