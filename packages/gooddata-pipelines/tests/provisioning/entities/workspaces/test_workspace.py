# (C) 2025 GoodData Corporation

import pytest
from gooddata_sdk.catalog.workspace.entity_model.workspace import (
    CatalogWorkspace,
)

from gooddata_pipelines.provisioning import WorkspaceProvisioner
from gooddata_pipelines.provisioning.entities.workspaces.models import (
    WorkspaceFullLoad,
)


@pytest.fixture
def test_find_workspaces_to_update_same_ids_and_names(
    workspace_provisioner: WorkspaceProvisioner,
) -> None:
    ids_in_both_systems = {"workspace_id1", "workspace_id2"}
    source_group: list[WorkspaceFullLoad] = [
        WorkspaceFullLoad(
            parent_id="client_id1",
            workspace_id="workspace_id1",
            workspace_name="workspace_title1",
        ),
        WorkspaceFullLoad(
            parent_id="client_id2",
            workspace_id="workspace_id2",
            workspace_name="workspace_title2",
        ),
    ]
    panther_group: list[CatalogWorkspace] = [
        CatalogWorkspace(
            workspace_id="workspace_id1",
            name="workspace_title1",
            parent_id="parent_id",
        ),
        CatalogWorkspace(
            workspace_id="workspace_id2",
            name="workspace_title2",
            parent_id="parent_id",
        ),
    ]

    workspaces_to_update = workspace_provisioner._find_workspaces_to_update(
        source_group, panther_group, ids_in_both_systems
    )

    assert workspaces_to_update == set()


def test_find_workspaces_to_update_different_ids(
    workspace_provisioner: WorkspaceProvisioner,
) -> None:
    ids_in_both_systems = {"workspace_id1", "workspace_id2"}
    source_group: list[WorkspaceFullLoad] = [
        WorkspaceFullLoad(
            parent_id="client_id1",
            workspace_id="workspace_id1",
            workspace_name="workspace_title1",
        ),
        WorkspaceFullLoad(
            parent_id="client_id2",
            workspace_id="workspace_id2",
            workspace_name="workspace_title2",
        ),
    ]
    panther_group: list[CatalogWorkspace] = [
        CatalogWorkspace(
            workspace_id="workspace_id1",
            name="workspace_title1",
            parent_id="parent_id",
        ),
        CatalogWorkspace(
            workspace_id="workspace_id2",
            name="workspace_title2",
            parent_id="parent_id",
        ),
    ]

    workspaces_to_update = workspace_provisioner._find_workspaces_to_update(
        source_group, panther_group, ids_in_both_systems
    )

    assert workspaces_to_update == set()


def test_find_workspaces_to_update_same_ids_different_names(
    workspace_provisioner: WorkspaceProvisioner,
) -> None:
    ids_in_both_systems: set[str] = {"workspace_id1", "workspace_id2"}
    source_group: list[WorkspaceFullLoad] = [
        WorkspaceFullLoad(
            parent_id="client_id1",
            workspace_id="workspace_id1",
            workspace_name="workspace_title1",
        ),
        WorkspaceFullLoad(
            parent_id="client_id2",
            workspace_id="workspace_id2",
            workspace_name="workspace_title2",
        ),
    ]
    panther_group: list[CatalogWorkspace] = [
        CatalogWorkspace(
            workspace_id="workspace_id1",
            name="old_workspace_title1",
            parent_id="parent_id",
        ),
        CatalogWorkspace(
            workspace_id="workspace_id2",
            name="old_workspace_title2",
            parent_id="parent_id",
        ),
    ]

    workspaces_to_update = workspace_provisioner._find_workspaces_to_update(
        source_group, panther_group, ids_in_both_systems
    )

    assert workspaces_to_update == {"workspace_id1", "workspace_id2"}


def test_find_workspaces_to_update_no_panther(
    workspace_provisioner: WorkspaceProvisioner,
) -> None:
    ids_in_both_systems: set[str] = set()
    source_group: list[WorkspaceFullLoad] = [
        WorkspaceFullLoad(
            parent_id="client_id1",
            workspace_id="workspace_id1",
            workspace_name="workspace_title1",
        ),
        WorkspaceFullLoad(
            parent_id="client_id2",
            workspace_id="workspace_id2",
            workspace_name="workspace_title2",
        ),
    ]
    panther_group: list[CatalogWorkspace] = []

    workspaces_to_update = workspace_provisioner._find_workspaces_to_update(
        source_group, panther_group, ids_in_both_systems
    )

    assert workspaces_to_update == set()
