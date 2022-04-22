# (C) 2021 GoodData Corporation
from __future__ import annotations

import json
from pathlib import Path

import vcr

import gooddata_metadata_client.apis as metadata_apis
from gooddata_sdk import GoodDataApiClient, GoodDataSdk
from gooddata_sdk.catalog.workspace.declarative_model.workspace.workspace import CatalogDeclarativeWorkspaces
from gooddata_sdk.catalog.workspace.entity_model.workspace import CatalogWorkspace
from gooddata_sdk.utils import create_directory
from tests import VCR_MATCH_ON

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures" / "workspaces"

gd_vcr = vcr.VCR(filter_headers=["authorization", "user-agent"], serializer="json", match_on=VCR_MATCH_ON)


def _empty_workspaces(sdk: GoodDataSdk) -> None:
    empty_workspaces_e = CatalogDeclarativeWorkspaces.from_api({"workspaces": [], "workspace_data_filters": []})
    sdk.catalog_workspace.put_declarative_workspaces(empty_workspaces_e)
    empty_workspaces_o = sdk.catalog_workspace.get_declarative_workspaces()
    assert empty_workspaces_e == empty_workspaces_o
    assert empty_workspaces_e.to_api().to_dict() == empty_workspaces_o.to_api().to_dict()


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_load_and_put_declarative_workspaces.json"))
def test_load_and_put_declarative_workspaces(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "load"
    expected_json_path = _current_dir / "expected" / "declarative_workspaces.json"
    workspaces_e = sdk.catalog_workspace.get_declarative_workspaces()

    try:
        _empty_workspaces(sdk)

        sdk.catalog_workspace.load_and_put_declarative_workspaces(path)
        workspaces_o = sdk.catalog_workspace.get_declarative_workspaces()
        assert workspaces_e == workspaces_o
        assert workspaces_e.to_api().to_dict() == workspaces_o.to_api().to_dict()
    finally:
        with open(expected_json_path) as f:
            data = json.load(f)
        workspaces_o = CatalogDeclarativeWorkspaces.from_dict(data)
        sdk.catalog_workspace.put_declarative_workspaces(workspaces_o)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_store_declarative_workspaces.json"))
def test_store_declarative_workspaces(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "store"
    create_directory(path)

    workspaces_e = sdk.catalog_workspace.get_declarative_workspaces()
    sdk.catalog_workspace.store_declarative_workspaces(path)
    workspaces_o = sdk.catalog_workspace.load_declarative_workspaces(path)

    assert workspaces_e == workspaces_o
    assert workspaces_e.to_api().to_dict() == workspaces_o.to_api().to_dict()


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_put_declarative_workspaces.json"))
def test_put_declarative_workspaces(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "expected" / "declarative_workspaces.json"
    workspaces_e = sdk.catalog_workspace.get_declarative_workspaces()

    try:
        _empty_workspaces(sdk)

        sdk.catalog_workspace.put_declarative_workspaces(workspaces_e)
        workspaces_o = sdk.catalog_workspace.get_declarative_workspaces()
        assert workspaces_e == workspaces_o
        assert workspaces_e.to_api().to_dict() == workspaces_o.to_api().to_dict()
    finally:
        with open(path) as f:
            data = json.load(f)
        workspaces_o = CatalogDeclarativeWorkspaces.from_dict(data)
        sdk.catalog_workspace.put_declarative_workspaces(workspaces_o)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_get_declarative_workspaces_snake_case.json"))
def test_get_declarative_workspaces_snake_case(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "expected" / "declarative_workspaces_snake_case.json"
    workspaces_o = sdk.catalog_workspace.get_declarative_workspaces()

    with open(path) as f:
        data = json.load(f)

    expected_o = CatalogDeclarativeWorkspaces.from_dict(data, camel_case=False)

    assert workspaces_o == expected_o
    assert workspaces_o.to_api().to_dict() == data


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_get_declarative_workspaces.json"))
def test_get_declarative_workspaces(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "expected" / "declarative_workspaces.json"
    workspaces_o = sdk.catalog_workspace.get_declarative_workspaces()

    with open(path) as f:
        data = json.load(f)

    expected_o = CatalogDeclarativeWorkspaces.from_dict(data)

    assert workspaces_o == expected_o
    assert workspaces_o.to_api().to_dict(camel_case=True) == data


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_declarative_workspaces.json"))
def test_declarative_workspaces(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    client = GoodDataApiClient(host=test_config["host"], token=test_config["token"])
    layout_api = metadata_apis.LayoutApi(client.metadata_client)

    workspaces_o = sdk.catalog_workspace.get_declarative_workspaces()

    assert len(workspaces_o.workspaces) == 3
    assert len(workspaces_o.workspace_data_filters) == 2
    assert [workspace.id for workspace in workspaces_o.workspaces] == ["demo", "demo_west", "demo_west_california"]
    assert workspaces_o.to_api().to_dict() == layout_api.get_workspaces_layout().to_dict()


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_update_workspace_invalid.json"))
def test_update_workspace_invalid(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    workspace_new_name = "Test"
    workspace_new_parent = "new_parent"

    workspace = sdk.catalog_workspace.get_workspace(test_config["workspace_with_parent"])
    workspaces = sdk.catalog_workspace.list_workspaces()
    assert len(workspaces) == 3
    assert workspace.id in [w.id for w in workspaces]
    assert workspace_new_parent not in [w.id for w in workspaces]
    assert workspace.parent_id is not None

    try:
        sdk.catalog_workspace.create_or_update(CatalogWorkspace(workspace.id, workspace_new_name, workspace_new_parent))
    except ValueError:
        # Update workspace parent is not allowed.
        workspaces = sdk.catalog_workspace.list_workspaces()
        workspace_o = sdk.catalog_workspace.get_workspace(workspace.id)
        assert len(workspaces) == 3
        assert workspace == workspace_o


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_update_workspace_valid.json"))
def test_update_workspace_valid(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    workspace_new_name = "Test"

    # Original workspace
    workspace = sdk.catalog_workspace.get_workspace(test_config["workspace_with_parent"])
    # New workspace
    new_workspace = CatalogWorkspace(workspace.id, workspace_new_name, workspace.parent_id)

    workspaces = sdk.catalog_workspace.list_workspaces()
    assert len(workspaces) == 3
    assert workspace.id in [w.id for w in workspaces]
    assert workspace.parent_id is not None

    try:
        # Updating only name.
        sdk.catalog_workspace.create_or_update(new_workspace)
        workspaces = sdk.catalog_workspace.list_workspaces()
        workspace_o = sdk.catalog_workspace.get_workspace(workspace.id)
        assert len(workspaces) == 3
        assert workspace_o == new_workspace
    finally:
        # Clean up. Revert changes.
        sdk.catalog_workspace.create_or_update(workspace)
        workspaces = sdk.catalog_workspace.list_workspaces()
        workspace_o = sdk.catalog_workspace.get_workspace(workspace.id)
        assert len(workspaces) == 3
        assert workspace_o == workspace


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_delete_workspace.json"))
def test_delete_workspace(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    workspace_id = "demo_west_california"

    workspace = sdk.catalog_workspace.get_workspace(workspace_id)
    workspaces = sdk.catalog_workspace.list_workspaces()
    assert len(workspaces) == 3
    assert workspace_id in [w.id for w in workspaces]

    try:
        sdk.catalog_workspace.delete_workspace(workspace_id)
        workspaces = sdk.catalog_workspace.list_workspaces()
        assert len(workspaces) == 2
        assert workspace_id not in [w.id for w in workspaces]
    finally:
        # Clean up. Create deleted workspace.
        sdk.catalog_workspace.create_or_update(workspace)
        workspaces = sdk.catalog_workspace.list_workspaces()
        assert len(workspaces) == 3
        assert workspace_id in [w.id for w in workspaces]


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_delete_non_existing_workspace.json"))
def test_delete_non_existing_workspace(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    workspace_id = "non_existing_workspace"

    workspaces = sdk.catalog_workspace.list_workspaces()
    assert len(workspaces) == 3
    assert workspace_id not in [w.id for w in workspaces]

    try:
        sdk.catalog_workspace.delete_workspace(workspace_id)
    except ValueError:
        # Trying to delete not existing workspace should not be executed and an exception should be raised.
        workspaces = sdk.catalog_workspace.list_workspaces()
        assert len(workspaces) == 3


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_delete_parent_workspace.json"))
def test_delete_parent_workspace(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    workspaces = sdk.catalog_workspace.list_workspaces()
    assert len(workspaces) == 3

    try:
        sdk.catalog_workspace.delete_workspace(test_config["workspace"])
    except ValueError:
        # Delete of workspace, which has children should not be executed and an exception should be raised.
        workspaces = sdk.catalog_workspace.list_workspaces()
        assert len(workspaces) == 3


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_create_workspace.json"))
def test_create_workspace(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    workspace_id = "test"
    workspace_name = "Test"
    workspace_parent = "demo"

    workspace = CatalogWorkspace(workspace_id, workspace_name, workspace_parent)

    workspaces = sdk.catalog_workspace.list_workspaces()
    assert len(workspaces) == 3
    assert workspace_id not in [w.id for w in workspaces]

    try:
        sdk.catalog_workspace.create_or_update(workspace)
        workspaces = sdk.catalog_workspace.list_workspaces()
        workspace_o = sdk.catalog_workspace.get_workspace(workspace_id)
        assert len(workspaces) == 4
        assert workspace_o == workspace
    finally:
        # Clean up. Delete created workspace.
        sdk.catalog_workspace.delete_workspace(workspace_id)
        workspaces = sdk.catalog_workspace.list_workspaces()
        assert len(workspaces) == 3
        assert workspace_id not in [w.id for w in workspaces]


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_get_workspace.json"))
def test_get_workspace(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    # Check workspace without parent
    workspace_demo = sdk.catalog_workspace.get_workspace(test_config["workspace"])
    assert workspace_demo.id == test_config["workspace"]
    assert workspace_demo.name == test_config["workspace_name"]
    assert workspace_demo.parent_id is None

    # Check workspace with parent
    workspace_with_parent = sdk.catalog_workspace.get_workspace(test_config["workspace_with_parent"])
    assert workspace_with_parent.id == test_config["workspace_with_parent"]
    assert workspace_with_parent.name == test_config["workspace_with_parent_name"]
    assert workspace_with_parent.parent_id == test_config["workspace"]


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_workspace_list.json"))
def test_workspace_list(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    ids = ["demo", "demo_west", "demo_west_california"]
    names = ["Demo", "Demo West", "Demo West California"]
    parents = [None, "demo", "demo_west"]

    workspaces = sdk.catalog_workspace.list_workspaces()
    assert len(workspaces) == 3

    workspaces_id = [w.id for w in workspaces]
    workspaces_id.sort()
    assert ids == workspaces_id

    workspaces_name = [w.name for w in workspaces]
    workspaces_name.sort()
    assert names == workspaces_name

    workspaces_parent = {w.id: w.parent_id for w in workspaces}
    workspaces_parent_l = [workspaces_parent[workspace_id] for workspace_id in workspaces_id]
    assert parents == workspaces_parent_l
