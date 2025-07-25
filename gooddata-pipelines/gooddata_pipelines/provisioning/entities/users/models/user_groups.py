# (C) 2025 GoodData Corporation

from typing import Any

from pydantic import BaseModel

from gooddata_pipelines.provisioning.utils.utils import SplitMixin


class BaseUserGroup(BaseModel, SplitMixin):
    user_group_id: str
    user_group_name: str
    parent_user_groups: list[str]

    @classmethod
    def _create_from_dict_data(
        cls, user_group_data: dict[str, Any], delimiter: str = ","
    ) -> dict[str, Any]:
        """Helper method to extract common data from dict."""
        parent_user_groups = cls.split(
            user_group_data["parent_user_groups"], delimiter=delimiter
        )
        user_group_name = user_group_data["user_group_name"]
        if not user_group_name:
            user_group_name = user_group_data["user_group_id"]

        return {
            "user_group_id": user_group_data["user_group_id"],
            "user_group_name": user_group_name,
            "parent_user_groups": parent_user_groups,
        }


class UserGroupIncrementalLoad(BaseUserGroup):
    is_active: bool

    @classmethod
    def from_list_of_dicts(
        cls, data: list[dict[str, Any]], delimiter: str = ","
    ) -> list["UserGroupIncrementalLoad"]:
        """Creates a list of User objects from list of dicts."""
        user_groups = []
        for user_group in data:
            base_data = cls._create_from_dict_data(user_group, delimiter)
            base_data["is_active"] = user_group["is_active"]

            user_groups.append(UserGroupIncrementalLoad(**base_data))

        return user_groups


class UserGroupFullLoad(BaseUserGroup):
    @classmethod
    def from_list_of_dicts(
        cls, data: list[dict[str, Any]], delimiter: str = ","
    ) -> list["UserGroupFullLoad"]:
        """Creates a list of User objects from list of dicts."""
        user_groups = []
        for user_group in data:
            base_data = cls._create_from_dict_data(user_group, delimiter)

            user_groups.append(UserGroupFullLoad(**base_data))

        return user_groups
