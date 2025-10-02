# (C) 2025 GoodData Corporation

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationInfo,
    field_validator,
)


class UserGroupBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_group_id: str
    user_group_name: str
    parent_user_groups: list[str] = Field(default_factory=list)

    @field_validator("user_group_name", mode="before")
    @classmethod
    def validate_user_group_name(
        cls, v: str | None, info: ValidationInfo
    ) -> str:
        """If user_group_name is None or empty, default to user_group_id."""
        if not v:  # handles None and empty string
            return info.data.get("user_group_id", "")
        return v

    @field_validator("parent_user_groups", mode="before")
    @classmethod
    def validate_parent_user_groups(cls, v: list[str] | None) -> list[str]:
        """If parent_user_groups is None or empty, default to empty list."""
        if not v:
            return []
        return v


class UserGroupFullLoad(UserGroupBase):
    """Input validator for full load of user group provisioning."""


class UserGroupIncrementalLoad(UserGroupBase):
    """Input validator for incremental load of user group provisioning."""

    is_active: bool
