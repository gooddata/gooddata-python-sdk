# (C) 2026 GoodData Corporation
from gooddata_api_client.model.json_api_workspace_out import JsonApiWorkspaceOut
from gooddata_api_client.model.json_api_workspace_out_attributes import JsonApiWorkspaceOutAttributes
from gooddata_sdk import CatalogWorkspace


def test_workspace_early_access_values_to_api():
    ws = CatalogWorkspace(workspace_id="w", name="W", early_access_values=["flag_a", "flag_b"])
    assert ws.to_api().data.attributes.early_access_values == ["flag_a", "flag_b"]


def test_workspace_without_early_access_values_to_api():
    ws = CatalogWorkspace(workspace_id="w", name="W")
    assert "early_access_values" not in ws.to_api().data.attributes


def test_workspace_early_access_values_from_api():
    entity = JsonApiWorkspaceOut(
        id="w", type="workspace", attributes=JsonApiWorkspaceOutAttributes(name="W", early_access_values=["flag_a"])
    )
    assert CatalogWorkspace.from_api(entity).early_access_values == ["flag_a"]
