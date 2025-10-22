# (C) 2025 GoodData Corporation

"""This module defines data models for user data filters in a GoodData workspace."""

import attrs
from pydantic import BaseModel, ConfigDict


@attrs.define
class UserDataFilterGroup:
    udf_id: str
    udf_values: list[str]


@attrs.define
class WorkspaceUserDataFilters:
    workspace_id: str
    user_data_filters: list["UserDataFilterGroup"] = attrs.field(factory=list)


class UserDataFilterFullLoad(BaseModel):
    model_config = ConfigDict(extra="forbid")

    workspace_id: str
    udf_id: str
    udf_value: str


class UserDataFilterIncrementalLoad(UserDataFilterFullLoad):
    is_active: bool
