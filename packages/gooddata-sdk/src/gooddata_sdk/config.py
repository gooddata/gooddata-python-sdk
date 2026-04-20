# (C) 2024 GoodData Corporation
import os
import warnings
from typing import Any, TypeVar

from attrs import asdict, define
from cattrs import structure
from cattrs.errors import ClassValidationError
from dotenv import load_dotenv

T = TypeVar("T", bound="ConfigBase")


@define
class ConfigBase:
    def to_dict(self) -> dict[str, str]:
        return asdict(self)

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
    workspace_id: str | None = None
    data_source: str | None = None
    custom_headers: dict[str, str] | None = None
    extra_user_agent: str | None = None
    ssl_ca_cert: str | None = None

    # Fields used only by CLI/config, not passed to GoodDataApiClient
    _NON_API_FIELDS = frozenset({"workspace_id", "data_source"})

    def to_dict(self, use_env: bool = False) -> dict[str, str]:
        load_dotenv()
        base = {k: v for k, v in asdict(self).items() if k not in self._NON_API_FIELDS}
        if not use_env:
            return base
        env_var = self.token[1:]
        if env_var not in os.environ:
            raise ValueError(f"Environment variable {env_var} not found")
        return {**base, "token": os.environ[env_var]}


_AAC_CONFIG_DEPRECATION_MSG = (
    "AacConfig is deprecated and will be removed in a future version. "
    "The AAC analytics model API endpoints have been removed from the GoodData platform."
)


@define
class AacConfig(ConfigBase):
    """Configuration for AAC deployments.

    .. deprecated::
        AacConfig is deprecated. The AAC analytics model API endpoints have been removed
        from the GoodData platform.
    """

    profiles: dict[str, Profile]
    default_profile: str
    access: dict[str, str] | None = None
    source_dir: str | None = None

    def __attrs_post_init__(self) -> None:
        warnings.warn(_AAC_CONFIG_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)

    def ds_credentials(self) -> dict[str, str]:
        load_dotenv()
        if self.access is None:
            return {}
        return {k: os.environ.get(v[1:], v) for k, v in self.access.items()}
