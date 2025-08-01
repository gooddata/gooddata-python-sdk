# (C) 2025 GoodData Corporation
"""Module containing models related to workspace provisioning in GoodData Cloud."""

from dataclasses import dataclass, field
from typing import Literal

from pydantic import BaseModel, ConfigDict


@dataclass
class WorkspaceDataMaps:
    """Dataclass to hold various mappings related to workspace data."""

    child_to_parent_id_map: dict[str, str] = field(default_factory=dict)
    workspace_id_to_wdf_map: dict[str, dict[str, list[str]]] = field(
        default_factory=dict
    )
    parent_ids: set[str] = field(default_factory=set)
    source_ids: set[str] = field(default_factory=set)
    workspace_id_to_name_map: dict[str, str] = field(default_factory=dict)
    upstream_ids: set[str] = field(default_factory=set)


class WorkspaceFullLoad(BaseModel):
    """Model representing input for provisioning of workspaces in GoodData Cloud."""

    model_config = ConfigDict(coerce_numbers_to_str=True)

    parent_id: str
    workspace_id: str
    workspace_name: str
    workspace_data_filter_id: str | None = None
    workspace_data_filter_values: list[str] | None = None


class WorkspaceIncrementalLoad(WorkspaceFullLoad):
    """Model representing input for incremental provisioning of workspaces in GoodData Cloud."""

    # TODO: double check that the model loads the data correctly, write a test
    is_active: bool


class WDFSettingAttributes(BaseModel):
    title: str
    filterValues: list[str]


class WDFSettingRelationshipsData(BaseModel):
    id: str
    type: Literal["workspaceDataFilter"]


class WDFSettingRelationships(BaseModel):
    workspaceDataFilter: dict[str, WDFSettingRelationshipsData]


class WDFSettingLinks(BaseModel):
    self: str


class WDFSettingMetaOrigin(BaseModel):
    originType: str
    originId: str


class WDFSettingMeta(BaseModel):
    origin: WDFSettingMetaOrigin


class WDFSetting(BaseModel):
    """Model representing a workspace data filter setting in GoodData Cloud."""

    id: str
    type: Literal["workspaceDataFilterSetting"]
    attributes: WDFSettingAttributes
    relationships: WDFSettingRelationships
    links: WDFSettingLinks
    meta: WDFSettingMeta
