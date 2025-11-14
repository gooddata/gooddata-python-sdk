# (C) 2025 GoodData Corporation

from gooddata_sdk.catalog.workspace.entity_model.workspace import (
    CatalogWorkspace,
)


def test_get_panther_children_workspaces_empty_response(
    workspace_provisioner, mocker
) -> None:
    parent_ids: set[str] = {"parent_id_1", "parent_id_2"}

    mocker.patch.object(
        workspace_provisioner._api._sdk.catalog_workspace,
        "list_workspaces",
        return_value=[],
    )

    panther_children = workspace_provisioner._get_panther_children_workspaces(
        parent_ids
    )

    assert panther_children == []


def test_get_panther_children_full_match(workspace_provisioner, mocker) -> None:
    parent_ids: set[str] = {"parent_id_1", "parent_id_2"}

    mocker.patch.object(
        workspace_provisioner._api._sdk.catalog_workspace,
        "list_workspaces",
        return_value=[
            CatalogWorkspace(
                workspace_id="workspace_id1",
                name="workspace_title1",
                parent_id="parent_id_1",
            ),
            CatalogWorkspace(
                workspace_id="workspace_id2",
                name="workspace_title2",
                parent_id="parent_id_2",
            ),
        ],
    )

    panther_children = workspace_provisioner._get_panther_children_workspaces(
        parent_ids
    )

    assert len(panther_children) == 2
    assert panther_children[0].workspace_id == "workspace_id1"
    assert panther_children[1].workspace_id == "workspace_id2"


def test_get_panther_children_no_match(workspace_provisioner, mocker) -> None:
    parent_ids: set[str] = {"parent_id_3", "parent_id_4"}

    mocker.patch.object(
        workspace_provisioner._api._sdk.catalog_workspace,
        "list_workspaces",
        return_value=[
            CatalogWorkspace(
                workspace_id="workspace_id1",
                name="workspace_title1",
                parent_id="parent_id_1",
            ),
            CatalogWorkspace(
                workspace_id="workspace_id2",
                name="workspace_title2",
                parent_id="parent_id_2",
            ),
        ],
    )

    panther_children = workspace_provisioner._get_panther_children_workspaces(
        parent_ids
    )

    assert len(panther_children) == 0
