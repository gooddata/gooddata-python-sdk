# (C) 2025 GoodData Corporation

from typing import Any

from gooddata_sdk.catalog.user.entity_model.user import CatalogUser
from pydantic import BaseModel

from gooddata_pipelines.provisioning.utils.utils import SplitMixin


class BaseUser(BaseModel, SplitMixin):
    """Base class containing shared user fields and functionality."""

    user_id: str
    firstname: str | None
    lastname: str | None
    email: str | None
    auth_id: str | None
    user_groups: list[str]

    @classmethod
    def _create_from_dict_data(
        cls, user_data: dict[str, Any], delimiter: str = ","
    ) -> dict[str, Any]:
        """Helper method to extract common data from dict."""
        user_groups = cls.split(user_data["user_groups"], delimiter=delimiter)
        return {
            "user_id": user_data["user_id"],
            "firstname": user_data["firstname"],
            "lastname": user_data["lastname"],
            "email": user_data["email"],
            "auth_id": user_data["auth_id"],
            "user_groups": user_groups,
        }

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


class UserIncrementalLoad(BaseUser):
    """User model for incremental load operations with active status tracking."""

    is_active: bool

    @classmethod
    def from_list_of_dicts(
        cls, data: list[dict[str, Any]], delimiter: str = ","
    ) -> list["UserIncrementalLoad"]:
        """Creates a list of User objects from list of dicts."""
        converted_users = []
        for user in data:
            base_data = cls._create_from_dict_data(user, delimiter)
            base_data["is_active"] = user["is_active"]
            converted_users.append(cls(**base_data))
        return converted_users

    @classmethod
    def from_sdk_obj(cls, obj: CatalogUser) -> "UserIncrementalLoad":
        """Creates GDUserTarget from CatalogUser SDK object."""
        base_data = cls._create_from_sdk_data(obj)
        base_data["is_active"] = True
        return cls(**base_data)


class UserFullLoad(BaseUser):
    """User model for full load operations."""

    @classmethod
    def from_list_of_dicts(
        cls, data: list[dict[str, Any]], delimiter: str = ","
    ) -> list["UserFullLoad"]:
        """Creates a list of User objects from list of dicts."""
        converted_users = []
        for user in data:
            base_data = cls._create_from_dict_data(user, delimiter)
            converted_users.append(cls(**base_data))
        return converted_users

    @classmethod
    def from_sdk_obj(cls, obj: CatalogUser) -> "UserFullLoad":
        """Creates GDUserTarget from CatalogUser SDK object."""
        base_data = cls._create_from_sdk_data(obj)
        return cls(**base_data)
