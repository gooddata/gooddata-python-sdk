# (C) 2025 GoodData Corporation

from gooddata_sdk.catalog.workspace.entity_model.workspace import (
    CatalogWorkspace,
)

from gooddata_pipelines.provisioning.entities.workspaces.models import (
    WorkspaceFullLoad,
)
from gooddata_pipelines.provisioning.entities.workspaces.workspace_data_parser import (
    WorkspaceDataParser,
)

parser = WorkspaceDataParser()


def test_get_id_to_name_map_no_overlap() -> None:
    """No overlap between source and Panther groups."""
    source_group: list[WorkspaceFullLoad] = [
        WorkspaceFullLoad(
            parent_id="some_parent",
            workspace_id="1",
            workspace_name="Source Workspace 1",
        ),
        WorkspaceFullLoad(
            parent_id="some_parent",
            workspace_id="2",
            workspace_name="Source Workspace 2",
        ),
    ]
    panther_group: list[CatalogWorkspace] = [
        CatalogWorkspace(workspace_id="3", name="Panther Workspace 1"),
        CatalogWorkspace(workspace_id="4", name="Panther Workspace 2"),
    ]

    expected_result = {
        "3": "Panther Workspace 1",
        "4": "Panther Workspace 2",
        "1": "Source Workspace 1",
        "2": "Source Workspace 2",
    }

    result = parser._get_id_to_name_map(source_group, panther_group)
    assert result == expected_result


def test_get_id_to_name_map_with_overlap() -> None:
    """Overlaping groups -> source group name takse precedence."""
    source_group: list[WorkspaceFullLoad] = [
        WorkspaceFullLoad(
            parent_id="some_parent",
            workspace_id="1",
            workspace_name="Source Workspace 1",
        ),
        WorkspaceFullLoad(
            parent_id="some_parent",
            workspace_id="2",
            workspace_name="Source Workspace 2",
        ),
    ]
    panther_group: list[CatalogWorkspace] = [
        CatalogWorkspace(workspace_id="1", name="Panther Workspace 1"),
        CatalogWorkspace(workspace_id="4", name="Panther Workspace 2"),
    ]

    expected_result = {
        "1": "Source Workspace 1",
        "4": "Panther Workspace 2",
        "2": "Source Workspace 2",
    }

    result = parser._get_id_to_name_map(source_group, panther_group)
    assert result == expected_result


def test_get_id_to_name_map_empty() -> None:
    """Empty source and Panther groups -> will return empty dict."""
    source_group: list[WorkspaceFullLoad] = []
    panther_group: list[CatalogWorkspace] = []

    expected_result: dict[str, str] = {}

    result = parser._get_id_to_name_map(source_group, panther_group)
    assert result == expected_result


def test_get_child_to_parent_map() -> None:
    """Maps child ID to parent ID."""
    source_group: list[WorkspaceFullLoad] = [
        WorkspaceFullLoad(
            workspace_id="child_1",
            parent_id="parent_1",
            workspace_name="Child Workspace 1",
        ),
        WorkspaceFullLoad(
            workspace_id="child_2",
            parent_id="parent_2",
            workspace_name="Child Workspace 2",
        ),
        WorkspaceFullLoad(
            workspace_id="child_3",
            parent_id="parent_1",
            workspace_name="Child Workspace 3",
        ),
    ]

    expected_result = {
        "child_1": "parent_1",
        "child_2": "parent_2",
        "child_3": "parent_1",
    }

    result = parser._get_child_to_parent_map(source_group)
    assert result == expected_result


def test_get_child_to_parent_map_empty() -> None:
    """Empty source group -> will return empty dict."""
    source_group: list[WorkspaceFullLoad] = []

    expected_result: dict[str, str] = {}

    result = parser._get_child_to_parent_map(source_group)
    assert result == expected_result


def test_get_child_to_parent_map_with_duplicates() -> None:
    """Child ID will be unique in the resulting dict"""
    source_group: list[WorkspaceFullLoad] = [
        WorkspaceFullLoad(
            workspace_id="child_1",
            parent_id="parent_1",
            workspace_name="Child Workspace 1",
        ),
        WorkspaceFullLoad(
            workspace_id="child_2",
            parent_id="parent_2",
            workspace_name="Child Workspace 2",
        ),
        WorkspaceFullLoad(
            workspace_id="child_3",
            parent_id="parent_1",
            workspace_name="Child Workspace 3",
        ),
        WorkspaceFullLoad(
            workspace_id="child_1",
            parent_id="parent_1",
            workspace_name="Child Workspace 1",
        ),
        WorkspaceFullLoad(
            workspace_id="child_2",
            parent_id="parent_2",
            workspace_name="Child Workspace 2",
        ),
        WorkspaceFullLoad(
            workspace_id="child_3",
            parent_id="parent_1",
            workspace_name="Child Workspace 3",
        ),
    ]

    expected_result: dict[str, str] = {
        "child_1": "parent_1",
        "child_2": "parent_2",
        "child_3": "parent_1",
    }

    result = parser._get_child_to_parent_map(source_group)
    assert result == expected_result


def test_get_child_to_wdfs_map() -> None:
    """Mapping child ID to WDF ID and WDF values."""
    source_group: list[WorkspaceFullLoad] = [
        WorkspaceFullLoad(
            parent_id="parent_1",
            workspace_id="child_1",
            workspace_name="Child Workspace 1",
            workspace_data_filter_id="wdf_1",
            workspace_data_filter_values=["value_1", "value_2"],
        ),
        WorkspaceFullLoad(
            parent_id="parent_2",
            workspace_id="child_2",
            workspace_name="Child Workspace 2",
            workspace_data_filter_id="wdf_2",
            workspace_data_filter_values=["value_3", "value_4"],
        ),
        WorkspaceFullLoad(
            parent_id="parent_1",
            workspace_id="child_3",
            workspace_name="Child Workspace 3",
            workspace_data_filter_id=None,
            workspace_data_filter_values=None,
        ),
    ]

    expected_result = {
        "child_1": {"wdf_1": ["value_1", "value_2"]},
        "child_2": {"wdf_2": ["value_3", "value_4"]},
    }

    result = parser._get_child_to_wdfs_map(source_group)
    assert result == expected_result


def test_get_child_to_wdfs_map_integers() -> None:
    """Is capable of handling int values (in case source column is int)."""
    source_group: list[WorkspaceFullLoad] = [
        WorkspaceFullLoad(
            workspace_id="child_1",
            parent_id="parent_1",
            workspace_name="Child Workspace 1",
            workspace_data_filter_id="wdf_1",
            workspace_data_filter_values=[1],  # type: ignore
        ),
        WorkspaceFullLoad(
            workspace_id="child_2",
            parent_id="parent_2",
            workspace_name="Child Workspace 2",
            workspace_data_filter_id="wdf_2",
            workspace_data_filter_values=["value_3", "value_4"],
        ),
        WorkspaceFullLoad(
            workspace_id="child_3",
            parent_id="parent_1",
            workspace_name="Child Workspace 3",
            workspace_data_filter_id=None,
            workspace_data_filter_values=None,
        ),
    ]

    expected_result = {
        "child_1": {"wdf_1": ["1"]},
        "child_2": {"wdf_2": ["value_3", "value_4"]},
    }

    result = parser._get_child_to_wdfs_map(source_group)
    assert result == expected_result


def test_get_child_to_wdfs_map_multiple_wdfs() -> None:
    """Handles multiple WDFs on a child workspace."""
    source_group: list[WorkspaceFullLoad] = [
        WorkspaceFullLoad(
            workspace_id="child_1",
            parent_id="parent_1",
            workspace_name="Child Workspace 1",
            workspace_data_filter_id="wdf_1",
            workspace_data_filter_values=[1],  # type: ignore
        ),
        WorkspaceFullLoad(
            workspace_id="child_1",
            parent_id="parent_1",
            workspace_name="Child Workspace 1",
            workspace_data_filter_id="wdf_2",
            workspace_data_filter_values=["value_3", "value_4"],
        ),
        WorkspaceFullLoad(
            workspace_id="child_2",
            parent_id="parent_2",
            workspace_name="Child Workspace 2",
            workspace_data_filter_id="wdf_2",
            workspace_data_filter_values=["value_3", "value_4"],
        ),
        WorkspaceFullLoad(
            workspace_id="child_3",
            parent_id="parent_1",
            workspace_name="Child Workspace 3",
            workspace_data_filter_id=None,
            workspace_data_filter_values=None,
        ),
    ]

    expected_result = {
        "child_1": {"wdf_1": ["1"], "wdf_2": ["value_3", "value_4"]},
        "child_2": {"wdf_2": ["value_3", "value_4"]},
    }

    result = parser._get_child_to_wdfs_map(source_group)
    assert result == expected_result


def test_get_child_to_wdfs_map_empty() -> None:
    source_group: list[WorkspaceFullLoad] = []

    expected_result: dict[str, dict[str, list[str]]] = {}

    result = parser._get_child_to_wdfs_map(source_group)
    assert result == expected_result
