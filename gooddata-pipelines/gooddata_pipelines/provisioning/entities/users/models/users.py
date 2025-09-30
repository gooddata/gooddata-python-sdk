# (C) 2025 GoodData Corporation

from typing import Any

from gooddata_sdk.catalog.user.entity_model.user import CatalogUser
from pydantic import BaseModel, ConfigDict, Field


class UserProfile(BaseModel):
    """Minimal model of api/v1/profile response.

    Does not contain all fields from the response.
    """

    user_id: str = Field(alias="userId")


class BaseUser(BaseModel):
    """Base class containing shared user fields and functionality."""

    model_config = ConfigDict(extra="forbid")

    user_id: str
    firstname: str | None
    lastname: str | None
    email: str | None
    auth_id: str | None
    user_groups: list[str]

    @classmethod
    def _create_from_sdk_data(cls, obj: CatalogUser) -> dict[str, Any]:
        """Helper method to extract common data from SDK object."""
        if obj.attributes:
            firstname = obj.attributes.firstname
            lastname = obj.attributes.lastname
            email = obj.attributes.email
            auth_id = obj.attributes.authentication_id
        else:
            firstname = None
            lastname = None
            email = None
            auth_id = None

        return {
            "user_id": obj.id,
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "auth_id": auth_id,
            "user_groups": [ug.id for ug in obj.user_groups],
        }

    def to_sdk_obj(self) -> CatalogUser:
        """Converts to CatalogUser SDK object."""
        return CatalogUser.init(
            user_id=self.user_id,
            firstname=self.firstname,
            lastname=self.lastname,
            email=self.email,
            authentication_id=self.auth_id,
            user_group_ids=self.user_groups,
        )


class UserFullLoad(BaseUser):
    """Input validator for full load of user provisioning."""

    @classmethod
    def from_sdk_obj(cls, obj: CatalogUser) -> "UserFullLoad":
        """Creates GDUserTarget from CatalogUser SDK object."""
        base_data = cls._create_from_sdk_data(obj)
        return cls(**base_data)


class UserIncrementalLoad(BaseUser):
    """Input validator for incremental load of user provisioning."""

    is_active: bool

    @classmethod
    def from_sdk_obj(cls, obj: CatalogUser) -> "UserIncrementalLoad":
        """Creates GDUserTarget from CatalogUser SDK object."""
        base_data = cls._create_from_sdk_data(obj)
        base_data["is_active"] = True
        return cls(**base_data)
