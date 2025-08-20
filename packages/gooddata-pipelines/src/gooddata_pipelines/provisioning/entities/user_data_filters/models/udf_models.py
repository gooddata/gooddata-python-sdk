# (C) 2025 GoodData Corporation

"""This module defines data models for user data filters in a GoodData workspace."""

# TODO: consider using attrs instead of dataclasses for these models. Dataclasses
# have different functionality per Python version (not package version).

from dataclasses import dataclass, field


@dataclass
class UserDataFilterGroup:
    udf_id: str
    udf_values: list[str]


@dataclass
class WorkspaceUserDataFilters:
    workspace_id: str
    user_data_filters: list["UserDataFilterGroup"] = field(default_factory=list)


@dataclass
class UserDataFilterFullLoad:
    workspace_id: str
    udf_id: str
    udf_value: str


@dataclass
class UserDataFilterIncrementalLoad(UserDataFilterFullLoad):
    is_active: bool
