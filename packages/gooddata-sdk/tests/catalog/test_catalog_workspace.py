# (C) 2021 GoodData Corporation
from __future__ import annotations

import json
from pathlib import Path
from xml.etree import ElementTree as ET

import yaml
from gooddata_sdk import (
    BasicCredentials,
    CatalogAutomationSchedule,
    CatalogDataSourcePostgres,
    CatalogDeclarativeAutomation,
    CatalogDeclarativeFilterView,
    CatalogDeclarativeUserDataFilter,
    CatalogDeclarativeUserDataFilters,
    CatalogDeclarativeWorkspaceDataFilters,
    CatalogDeclarativeWorkspaceModel,
    CatalogDeclarativeWorkspaces,
    CatalogUserDataFilter,
    CatalogWorkspace,
    CatalogWorkspaceSetting,
    GoodDataApiClient,
    GoodDataSdk,
    PostgresAttributes,
)
from gooddata_sdk.catalog.identifier import (
    CatalogDeclarativeAnalyticalDashboardIdentifier,
    CatalogNotificationChannelIdentifier,
    CatalogUserIdentifier,
)
from gooddata_sdk.catalog.organization.layout.notification_channel import (
    CatalogDeclarativeNotificationChannel,
    CatalogWebhook,
)
from gooddata_sdk.utils import recreate_directory
from tests_support.vcrpy_utils import get_vcr

from tests.catalog.utils import _refresh_workspaces

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures" / "workspaces"


def _empty_workspaces(sdk: GoodDataSdk) -> None:
    empty_workspaces_e = CatalogDeclarativeWorkspaces.from_api({"workspaces": [], "workspace_data_filters": []})
    sdk.catalog_workspace.put_declarative_workspaces(empty_workspaces_e)
    empty_workspaces_o = sdk.catalog_workspace.get_declarative_workspaces()
    assert empty_workspaces_e == empty_workspaces_o
    assert empty_workspaces_e.to_dict(camel_case=True) == empty_workspaces_o.to_dict(camel_case=True)


def _empty_workspace(sdk: GoodDataSdk, workspace_id: str) -> None:
    empty_workspace_e = CatalogDeclarativeWorkspaceModel()
    sdk.catalog_workspace.put_declarative_workspace(workspace_id=workspace_id, workspace=empty_workspace_e)
    empty_workspace_o = sdk.catalog_workspace.get_declarative_workspace(workspace_id=workspace_id)
    assert len(empty_workspace_o.ldm.datasets) == 0
    assert len(empty_workspace_o.ldm.date_instances) == 0
    assert len(empty_workspace_o.analytics.analytical_dashboards) == 0
    assert len(empty_workspace_o.analytics.dashboard_plugins) == 0
    assert len(empty_workspace_o.analytics.filter_contexts) == 0
    assert len(empty_workspace_o.analytics.metrics) == 0
    assert len(empty_workspace_o.analytics.visualization_objects) == 0


def _empty_workspace_data_filters(sdk: GoodDataSdk) -> None:
    empty_workspace_data_filters_e = CatalogDeclarativeWorkspaceDataFilters.from_dict(
        {"workspace_data_filters": []}, camel_case=False
    )
    sdk.catalog_workspace.put_declarative_workspace_data_filters(empty_workspace_data_filters_e)
    empty_workspace_data_filters_o = sdk.catalog_workspace.get_declarative_workspace_data_filters()
    assert empty_workspace_data_filters_e == empty_workspace_data_filters_o
    assert empty_workspace_data_filters_e.to_dict(camel_case=True) == empty_workspace_data_filters_o.to_dict(
        camel_case=True
    )


def _empty_user_data_filters(workspace_id: str, sdk: GoodDataSdk) -> None:
    empty_user_data_filters_e = CatalogDeclarativeUserDataFilters.from_dict({"user_data_filters": []}, camel_case=False)
    sdk.catalog_workspace.put_declarative_user_data_filters(workspace_id, empty_user_data_filters_e)
    empty_user_data_filters_o = sdk.catalog_workspace.get_declarative_user_data_filters(workspace_id)
    assert empty_user_data_filters_e == empty_user_data_filters_o
    assert empty_user_data_filters_e.to_dict(camel_case=True) == empty_user_data_filters_o.to_dict(camel_case=True)


def _are_user_data_filters_empty(sdk: GoodDataSdk, workspace_id: str) -> None:
    user_data_filters = sdk.catalog_workspace.list_user_data_filters(workspace_id)
    assert len(user_data_filters) == 0


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_load_and_put_declarative_workspaces.yaml"))
def test_load_and_put_declarative_workspaces(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "load"
    with open(_current_dir / "expected" / "declarative_workspaces.json") as f:
        data = json.load(f)
        workspaces_e = CatalogDeclarativeWorkspaces.from_dict(data)

    try:
        _empty_workspaces(sdk)

        sdk.catalog_workspace.load_and_put_declarative_workspaces(path)
        workspaces_o = sdk.catalog_workspace.get_declarative_workspaces(exclude=["ACTIVITY_INFO"])
        assert workspaces_e == workspaces_o
        assert workspaces_e.to_dict(camel_case=True) == workspaces_o.to_dict(camel_case=True)
    finally:
        _refresh_workspaces(sdk)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_store_declarative_workspaces.yaml"))
def test_store_declarative_workspaces(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "store"
    recreate_directory(path)

    workspaces_e = sdk.catalog_workspace.get_declarative_workspaces()
    sdk.catalog_workspace.store_declarative_workspaces(path)
    workspaces_o = sdk.catalog_workspace.load_declarative_workspaces(path)

    assert workspaces_e == workspaces_o
    assert workspaces_e.to_dict(camel_case=True) == workspaces_o.to_dict(camel_case=True)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_put_declarative_workspaces.yaml"))
def test_put_declarative_workspaces(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    workspaces_e = sdk.catalog_workspace.get_declarative_workspaces(exclude=["ACTIVITY_INFO"])

    try:
        _empty_workspaces(sdk)

        sdk.catalog_workspace.put_declarative_workspaces(workspaces_e)
        workspaces_o = sdk.catalog_workspace.get_declarative_workspaces(exclude=["ACTIVITY_INFO"])
        assert workspaces_e == workspaces_o
        assert workspaces_e.to_dict(camel_case=True) == workspaces_o.to_dict(camel_case=True)
    finally:
        _refresh_workspaces(sdk)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_get_declarative_workspaces_snake_case.yaml"))
def test_get_declarative_workspaces_snake_case(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "expected" / "declarative_workspaces_snake_case.json"
    workspaces_o = sdk.catalog_workspace.get_declarative_workspaces(exclude=["ACTIVITY_INFO"])

    with open(path) as f:
        data = json.load(f)

    expected_o = CatalogDeclarativeWorkspaces.from_dict(data, camel_case=False)

    assert workspaces_o == expected_o
    assert workspaces_o.to_dict(camel_case=False) == data


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_get_declarative_workspaces.yaml"))
def test_get_declarative_workspaces(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "expected" / "declarative_workspaces.json"
    workspaces_o = sdk.catalog_workspace.get_declarative_workspaces(exclude=["ACTIVITY_INFO"])

    with open(path) as f:
        data = json.load(f)

    expected_o = CatalogDeclarativeWorkspaces.from_dict(data)

    assert workspaces_o == expected_o
    assert workspaces_o.to_api().to_dict(camel_case=True) == data


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_declarative_workspaces.yaml"))
def test_declarative_workspaces(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    client = GoodDataApiClient(host=test_config["host"], token=test_config["token"])
    layout_api = client.layout_api

    workspaces_o = sdk.catalog_workspace.get_declarative_workspaces(exclude=["ACTIVITY_INFO"])

    assert len(workspaces_o.workspaces) == 3
    assert len(workspaces_o.workspace_data_filters) == 2
    assert [workspace.id for workspace in workspaces_o.workspaces] == ["demo", "demo_west", "demo_west_california"]
    assert workspaces_o.to_dict(camel_case=True) == layout_api.get_workspaces_layout(exclude=["ACTIVITY_INFO"]).to_dict(
        camel_case=True
    )


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_update_workspace_invalid.yaml"))
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


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_update_workspace_valid.yaml"))
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
        _refresh_workspaces(sdk)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_delete_workspace.yaml"))
def test_delete_workspace(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    workspace_id = "demo_west_california"

    workspaces = sdk.catalog_workspace.list_workspaces()
    assert len(workspaces) == 3
    assert workspace_id in [w.id for w in workspaces]

    try:
        sdk.catalog_workspace.delete_workspace(workspace_id)
        workspaces = sdk.catalog_workspace.list_workspaces()
        assert len(workspaces) == 2
        assert workspace_id not in [w.id for w in workspaces]
    finally:
        _refresh_workspaces(sdk)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_delete_non_existing_workspace.yaml"))
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


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_delete_parent_workspace.yaml"))
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


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_create_workspace.yaml"))
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
        _refresh_workspaces(sdk)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_get_workspace.yaml"))
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


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_workspace_list.yaml"))
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


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_get_declarative_workspace_data_filters.yaml"))
def test_get_declarative_workspace_data_filters(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    client = GoodDataApiClient(host=test_config["host"], token=test_config["token"])
    layout_api = client.layout_api

    declarative_workspace_data_filters = sdk.catalog_workspace.get_declarative_workspace_data_filters()
    workspace_data_filters = declarative_workspace_data_filters.workspace_data_filters

    assert len(workspace_data_filters) == 2
    assert set(workspace_data_filter.id for workspace_data_filter in workspace_data_filters) == {
        "wdf__region",
        "wdf__state",
    }

    assert declarative_workspace_data_filters.to_dict(
        camel_case=True
    ) == layout_api.get_workspace_data_filters_layout().to_dict(camel_case=True)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_store_declarative_workspace_data_filters.yaml"))
def test_store_declarative_workspace_data_filters(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "store"
    recreate_directory(path)

    declarative_workspace_data_filters_e = sdk.catalog_workspace.get_declarative_workspace_data_filters()
    sdk.catalog_workspace.store_declarative_workspace_data_filters(path)
    declarative_workspace_data_filters_o = sdk.catalog_workspace.load_declarative_workspace_data_filters(path)

    assert declarative_workspace_data_filters_e == declarative_workspace_data_filters_o
    assert declarative_workspace_data_filters_e.to_dict(
        camel_case=True
    ) == declarative_workspace_data_filters_o.to_dict(camel_case=True)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_load_and_put_declarative_workspace_data_filters.yaml"))
def test_load_and_put_declarative_workspace_data_filters(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "load"
    workspace_data_filters_e = sdk.catalog_workspace.get_declarative_workspace_data_filters()

    try:
        _empty_workspace_data_filters(sdk)

        sdk.catalog_workspace.load_and_put_declarative_workspace_data_filters(path)
        workspace_data_filters_o = sdk.catalog_workspace.get_declarative_workspace_data_filters()
        assert workspace_data_filters_e == workspace_data_filters_o
        assert workspace_data_filters_e.to_dict(camel_case=True) == workspace_data_filters_o.to_dict(camel_case=True)
    finally:
        _refresh_workspaces(sdk)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_put_declarative_workspace_data_filters.yaml"))
def test_put_declarative_workspace_data_filters(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    declarative_workspace_data_filters_e = sdk.catalog_workspace.get_declarative_workspace_data_filters()

    try:
        _empty_workspace_data_filters(sdk)

        sdk.catalog_workspace.put_declarative_workspace_data_filters(declarative_workspace_data_filters_e)
        declarative_workspace_data_filters_o = sdk.catalog_workspace.get_declarative_workspace_data_filters()
        assert declarative_workspace_data_filters_e == declarative_workspace_data_filters_o
        assert declarative_workspace_data_filters_e.to_dict(
            camel_case=True
        ) == declarative_workspace_data_filters_o.to_dict(camel_case=True)
    finally:
        _refresh_workspaces(sdk)


@gd_vcr.use_cassette(str(_fixtures_dir / "user_data_filters_life_cycle.yaml"))
def test_user_data_filters_life_cycle(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    _are_user_data_filters_empty(sdk, test_config["workspace"])

    try:
        user_data_filter = CatalogUserDataFilter.init(
            user_data_filter_id=test_config["test_new_user_data_filter"],
            maql='{label/order_status} IN ("returned")',
            title="test_new_user_data_filter",
            user_id=test_config["demo_user"],
        )
        sdk.catalog_workspace.create_or_update_user_data_filter(
            workspace_id=test_config["workspace"], user_data_filter=user_data_filter
        )
        user_data_filters = sdk.catalog_workspace.list_user_data_filters(test_config["workspace"])
        assert len(user_data_filters) == 1
        assert user_data_filters[0].id == user_data_filter.id

        get_filter = sdk.catalog_workspace.get_user_data_filter(
            workspace_id=test_config["workspace"], user_data_filter_id=user_data_filter.id
        )

        assert get_filter is not None
        assert get_filter.id == user_data_filter.id
        assert get_filter.user_id == test_config["demo_user"]
        assert get_filter.user_group_id is None
        assert get_filter.label_ids == ["order_status"]

        sdk.catalog_workspace.delete_user_data_filter(
            workspace_id=test_config["workspace"], user_data_filter_id=get_filter.id
        )

        _are_user_data_filters_empty(sdk, test_config["workspace"])
    finally:
        _refresh_workspaces(sdk)


@gd_vcr.use_cassette(str(_fixtures_dir / "user_data_filters_for_user_group.yaml"))
def test_user_data_filters_for_user_group(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    _are_user_data_filters_empty(sdk, test_config["workspace"])

    try:
        user_data_filter = CatalogUserDataFilter.init(
            user_data_filter_id=test_config["test_new_user_data_filter"],
            maql='{label/order_status} IN ("returned")',
            title="test_new_user_data_filter",
            user_group_id=test_config["test_user_group"],
        )
        sdk.catalog_workspace.create_or_update_user_data_filter(
            workspace_id=test_config["workspace"], user_data_filter=user_data_filter
        )
        user_data_filters = sdk.catalog_workspace.list_user_data_filters(test_config["workspace"])
        assert len(user_data_filters) == 1
        assert user_data_filters[0].id == user_data_filter.id

        get_filter = sdk.catalog_workspace.get_user_data_filter(
            workspace_id=test_config["workspace"], user_data_filter_id=user_data_filter.id
        )

        assert get_filter is not None
        assert get_filter.id == user_data_filter.id
        assert get_filter.user_id is None
        assert get_filter.user_group_id == test_config["test_user_group"]
        assert get_filter.label_ids == ["order_status"]

        sdk.catalog_workspace.delete_user_data_filter(
            workspace_id=test_config["workspace"], user_data_filter_id=get_filter.id
        )

        _are_user_data_filters_empty(sdk, test_config["workspace"])
    finally:
        _refresh_workspaces(sdk)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_get_declarative_user_data_filters.yaml"))
def test_get_declarative_user_data_filters(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    client = GoodDataApiClient(host=test_config["host"], token=test_config["token"])
    layout_api = client.layout_api

    declarative_user_data_filters = sdk.catalog_workspace.get_declarative_user_data_filters(test_config["workspace"])
    user_data_filters = declarative_user_data_filters.user_data_filters

    assert len(user_data_filters) == 0
    assert user_data_filters == []

    assert declarative_user_data_filters.to_dict(camel_case=True) == layout_api.get_user_data_filters(
        test_config["workspace"]
    ).to_dict(camel_case=True)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_store_declarative_user_data_filters.yaml"))
def test_store_declarative_user_data_filters(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "store"
    recreate_directory(path)

    declarative_user_data_filters_e = sdk.catalog_workspace.get_declarative_user_data_filters(test_config["workspace"])
    sdk.catalog_workspace.store_declarative_user_data_filters(test_config["workspace"], path)
    declarative_user_data_filters_o = sdk.catalog_workspace.load_declarative_user_data_filters(path)

    assert declarative_user_data_filters_e == declarative_user_data_filters_o
    assert declarative_user_data_filters_e.to_dict(camel_case=True) == declarative_user_data_filters_o.to_dict(
        camel_case=True
    )


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_load_and_put_declarative_user_data_filters.yaml"))
def test_load_and_put_declarative_user_data_filters(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "load"
    user_data_filters_e = sdk.catalog_workspace.get_declarative_user_data_filters(test_config["workspace"])

    try:
        _empty_user_data_filters(test_config["workspace"], sdk)

        sdk.catalog_workspace.load_and_put_declarative_user_data_filters(test_config["workspace"], path)
        user_data_filters_o = sdk.catalog_workspace.get_declarative_user_data_filters(test_config["workspace"])
        assert user_data_filters_e == user_data_filters_o
        assert user_data_filters_e.to_dict(camel_case=True) == user_data_filters_o.to_dict(camel_case=True)
    finally:
        _refresh_workspaces(sdk)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_put_declarative_user_data_filters.yaml"))
def test_put_declarative_user_data_filters(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    user_data_filters_e = CatalogDeclarativeUserDataFilters(
        user_data_filters=[
            CatalogDeclarativeUserDataFilter(
                id="user_data_filter",
                title="youwillnotsee",
                maql="FALSE",
                user=CatalogUserIdentifier(id="demo", type="user"),
            )
        ]
    )

    try:
        sdk.catalog_workspace.put_declarative_user_data_filters(test_config["workspace"], user_data_filters_e)
        user_data_filters_o = sdk.catalog_workspace.get_declarative_user_data_filters(test_config["workspace"])

        assert user_data_filters_e == user_data_filters_o
        assert user_data_filters_e.to_dict() == user_data_filters_o.to_dict()
    finally:
        _refresh_workspaces(sdk)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_get_declarative_workspace.yaml"))
def test_get_declarative_workspace(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    client = GoodDataApiClient(host=test_config["host"], token=test_config["token"])
    layout_api = client.layout_api

    workspace = sdk.catalog_workspace.get_declarative_workspace(
        workspace_id=test_config["workspace"], exclude=["ACTIVITY_INFO"]
    )

    assert len(workspace.ldm.datasets) == 5
    assert len(workspace.ldm.date_instances) == 1
    assert len(workspace.analytics.analytical_dashboards) == 3
    assert len(workspace.analytics.dashboard_plugins) == 2
    assert len(workspace.analytics.filter_contexts) == 2
    assert len(workspace.analytics.metrics) == 24
    assert len(workspace.analytics.visualization_objects) == 15
    assert workspace.to_dict(camel_case=True) == layout_api.get_workspace_layout(
        workspace_id=test_config["workspace"], exclude=["ACTIVITY_INFO"]
    ).to_dict(camel_case=True)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_put_declarative_workspace.yaml"))
def test_put_declarative_workspace(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    sdk.catalog_workspace.create_or_update(
        workspace=CatalogWorkspace(workspace_id=test_config["workspace_test"], name=test_config["workspace_test"])
    )

    try:
        workspace_e = sdk.catalog_workspace.get_declarative_workspace(
            test_config["workspace"], exclude=["ACTIVITY_INFO"]
        )
        sdk.catalog_workspace.put_declarative_workspace(
            workspace_id=test_config["workspace_test"], workspace=workspace_e, standalone_copy=True
        )
        workspace_o = sdk.catalog_workspace.get_declarative_workspace(
            test_config["workspace_test"], exclude=["ACTIVITY_INFO"]
        )
        assert workspace_e != workspace_o
        workspace_e.remove_wdf_refs()
        assert workspace_e == workspace_o
        assert workspace_e.to_dict() == workspace_o.to_dict()
    finally:
        _refresh_workspaces(sdk)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_store_declarative_workspace.yaml"))
def test_store_declarative_workspace(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "store"
    recreate_directory(path)

    workspaces_e = sdk.catalog_workspace.get_declarative_workspace(
        workspace_id=test_config["workspace"], exclude=["ACTIVITY_INFO"]
    )
    sdk.catalog_workspace.store_declarative_workspace(
        workspace_id=test_config["workspace"], layout_root_path=path, exclude=["ACTIVITY_INFO"]
    )
    workspaces_o = sdk.catalog_workspace.load_declarative_workspace(
        workspace_id=test_config["workspace"], layout_root_path=path
    )

    assert workspaces_e == workspaces_o
    assert workspaces_e.to_dict(camel_case=True) == workspaces_o.to_dict(camel_case=True)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_load_and_put_declarative_workspace.yaml"))
def test_load_and_put_declarative_workspace(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "load"
    workspace_e = sdk.catalog_workspace.get_declarative_workspace(
        workspace_id=test_config["workspace"], exclude=["ACTIVITY_INFO"]
    )

    try:
        _empty_workspace(sdk, workspace_id=test_config["workspace"])

        sdk.catalog_workspace.load_and_put_declarative_workspace(
            workspace_id=test_config["workspace"], layout_root_path=path
        )
        workspace_o = sdk.catalog_workspace.get_declarative_workspace(
            workspace_id=test_config["workspace"], exclude=["ACTIVITY_INFO"]
        )
        assert workspace_e == workspace_o
        assert workspace_e.to_dict(camel_case=True) == workspace_o.to_dict(camel_case=True)
    finally:
        _refresh_workspaces(sdk)


def create_second_data_source(sdk: GoodDataSdk, ds_id: str) -> None:
    sdk.catalog_data_source.create_or_update_data_source(
        CatalogDataSourcePostgres(
            id=ds_id,
            name="Test2",
            db_specific_attributes=PostgresAttributes(host="localhost", db_name="demo"),
            schema="demo",
            credentials=BasicCredentials(
                username="demouser",
                password="demopass",
            ),
            url_params=[("autosave", "false")],
        )
    )


def delete_data_source(sdk: GoodDataSdk, ds_id: str) -> None:
    sdk.catalog_data_source.delete_data_source(ds_id)


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_clone_workspace.yaml"))
def test_clone_workspace(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    source_ws_id = test_config["workspace"]
    default_cloned_ws_id = "demo_clone"
    custom_cloned_ws_id = "demo_jacek"
    custom_cloned_ws_name = "Deno Jacek"
    data_source_mapping = {test_config["data_source"]: test_config["data_source2"]}

    try:
        # Must create the second DS, backend validates when putting the re-mapped LDM
        create_second_data_source(sdk, test_config["data_source2"])
        sdk.catalog_workspace.clone_workspace(source_ws_id, data_source_mapping=data_source_mapping, upper_case=True)
        default_cloned_ws = sdk.catalog_workspace.get_workspace(default_cloned_ws_id)
        assert default_cloned_ws.id == default_cloned_ws_id
        default_cloned_decl_ws = sdk.catalog_workspace.get_declarative_workspace(default_cloned_ws_id)
        assert default_cloned_decl_ws.ldm.datasets[0].data_source_table_id.data_source_id == test_config["data_source2"]
        assert default_cloned_decl_ws.ldm.datasets[0].facts[0].source_column == "BUDGET"

        sdk.catalog_workspace.clone_workspace(
            source_ws_id, target_workspace_id=custom_cloned_ws_id, target_workspace_name=custom_cloned_ws_name
        )
        custom_ws = sdk.catalog_workspace.get_workspace(custom_cloned_ws_id)
        assert custom_ws.name == custom_cloned_ws_name

        origin_permissions = sdk.catalog_permission.get_declarative_permissions(source_ws_id)
        cloned_permissions = sdk.catalog_permission.get_declarative_permissions(custom_cloned_ws_id)
        assert len(origin_permissions.permissions) == len(cloned_permissions.permissions)

        # Clone once again, test overwrite works
        sdk.catalog_workspace.clone_workspace(
            source_ws_id, data_source_mapping=data_source_mapping, upper_case=True, overwrite_existing=True
        )
    finally:
        _refresh_workspaces(sdk)
        delete_data_source(sdk, test_config["data_source2"])


def _translate_batch(to_translate: list[str]) -> list[str]:
    return [("Rozpočet" if x == "Budget" else x) for x in to_translate]


@gd_vcr.use_cassette(str(_fixtures_dir / "demo_translate_workspace.yaml"))
def test_translate_workspace(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    source_ws_id = test_config["workspace"]
    path_to_layouts = _current_dir / "translate"
    recreate_directory(path_to_layouts)
    path_to_config = _current_dir / "config" / "test_translate.yaml"
    with open(path_to_config) as fp:
        config = yaml.safe_load(fp)
    from_lang = config["from_language"]
    to_configs = config["to"]

    for to_config in to_configs:
        new_workspace_id = f"{source_ws_id}_{to_config['language']}"
        try:
            sdk.catalog_workspace.generate_localized_workspaces(
                source_ws_id,
                to_lang=to_config["language"],
                to_locale=to_config["locale"],
                from_lang=from_lang,
                translator_func=_translate_batch,
                provision_workspace=False,
                layout_root_path=path_to_layouts,
            )
            new_workspace = sdk.catalog_workspace.load_declarative_workspace(new_workspace_id, path_to_layouts)
            for dataset in new_workspace.ldm.datasets:
                for fact in dataset.facts:
                    if fact.id == "budget":
                        assert fact.title == "Rozpočet"

            # Run second time without translation function. Previous execution created translation file, which is used.
            sdk.catalog_workspace.generate_localized_workspaces(
                source_ws_id,
                to_lang=to_config["language"],
                to_locale=to_config["locale"],
                from_lang=from_lang,
                provision_workspace=True,
                layout_root_path=path_to_layouts,
            )
        finally:
            _refresh_workspaces(sdk)


@gd_vcr.use_cassette(str(_fixtures_dir / "create_workspace_setting.yaml"))
def test_create_workspace_setting(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    setting_id = "test_setting"
    setting_type = "LOCALE"
    content = {"value": "fr-FR"}
    setting = CatalogWorkspaceSetting(id=setting_id, setting_type=setting_type, content=content)

    try:
        sdk.catalog_workspace.create_or_update_workspace_setting(test_config["workspace"], setting)
        setting_o = sdk.catalog_workspace.get_workspace_setting(test_config["workspace"], setting_id)
        assert setting_o == setting
    finally:
        sdk.catalog_workspace.delete_workspace_setting(test_config["workspace"], setting_id)
        assert len(sdk.catalog_workspace.list_workspace_settings(test_config["workspace"])) == 0


@gd_vcr.use_cassette(str(_fixtures_dir / "list_workspace_settings.yaml"))
def test_list_workspace_settings(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    setting_id_1 = "test_setting_1"
    setting_type_1 = "LOCALE"
    content_1 = {"value": "fr-FR"}
    new_setting_1 = CatalogWorkspaceSetting(id=setting_id_1, setting_type=setting_type_1, content=content_1)

    setting_id_2 = "test_setting_2"
    setting_type_2 = "FORMAT_LOCALE"
    content_2 = {"value": "en-US"}
    new_setting_2 = CatalogWorkspaceSetting(id=setting_id_2, setting_type=setting_type_2, content=content_2)

    try:
        sdk.catalog_workspace.create_or_update_workspace_setting(test_config["workspace"], new_setting_1)
        sdk.catalog_workspace.create_or_update_workspace_setting(test_config["workspace"], new_setting_2)
        workspace_settings = sdk.catalog_workspace.list_workspace_settings(test_config["workspace"])
        assert len(workspace_settings) == 2
        assert new_setting_1 in workspace_settings
        assert new_setting_2 in workspace_settings
    finally:
        sdk.catalog_workspace.delete_workspace_setting(test_config["workspace"], setting_id_1)
        sdk.catalog_workspace.delete_workspace_setting(test_config["workspace"], setting_id_2)
        assert len(sdk.catalog_workspace.list_workspace_settings(test_config["workspace"])) == 0


@gd_vcr.use_cassette(str(_fixtures_dir / "delete_workspace_setting.yaml"))
def test_delete_workspace_setting(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    setting_id = "test_setting"
    setting_type = "LOCALE"
    content = {"value": "fr-FR"}
    setting = CatalogWorkspaceSetting(id=setting_id, setting_type=setting_type, content=content)

    try:
        sdk.catalog_workspace.create_or_update_workspace_setting(test_config["workspace"], setting)
        setting_o = sdk.catalog_workspace.get_workspace_setting(test_config["workspace"], setting_id)
        assert setting_o == setting
        sdk.catalog_workspace.delete_workspace_setting(test_config["workspace"], setting_id)
        settings = sdk.catalog_workspace.list_workspace_settings(test_config["workspace"])
        assert len(settings) == 0
    finally:
        sdk.catalog_workspace.delete_workspace_setting(test_config["workspace"], setting_id)
        assert len(sdk.catalog_workspace.list_workspace_settings(test_config["workspace"])) == 0


@gd_vcr.use_cassette(str(_fixtures_dir / "update_workspace_setting.yaml"))
def test_update_workspace_setting(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    setting_id = "test_setting"
    setting_type = "LOCALE"
    content = {"value": "fr-FR"}
    setting = CatalogWorkspaceSetting(id=setting_id, setting_type=setting_type, content=content)

    try:
        sdk.catalog_workspace.create_or_update_workspace_setting(test_config["workspace"], setting)
        setting_o = sdk.catalog_workspace.get_workspace_setting(test_config["workspace"], setting_id)
        assert setting_o == setting
        content = {"value": "en-US"}
        setting = CatalogWorkspaceSetting(id=setting_id, setting_type=setting_type, content=content)
        sdk.catalog_workspace.create_or_update_workspace_setting(test_config["workspace"], setting)
        setting_o = sdk.catalog_workspace.get_workspace_setting(test_config["workspace"], setting_id)
        assert setting_o == setting
    finally:
        sdk.catalog_workspace.delete_workspace_setting(test_config["workspace"], setting_id)
        assert len(sdk.catalog_workspace.list_workspace_settings(test_config["workspace"])) == 0


@gd_vcr.use_cassette(str(_fixtures_dir / "get_metadata_localization.yaml"))
def test_get_metadata_localization(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    test_workspace = test_config["workspace"]
    xliff = sdk.catalog_workspace.get_metadata_localization(workspace_id=test_workspace, target_language="fr-FR")

    tree = ET.ElementTree(ET.fromstring(xliff))

    # Check, if the returned xliff is valid.
    assert tree is not None


@gd_vcr.use_cassette(str(_fixtures_dir / "set_metadata_localization.yaml"))
def test_set_metadata_localization(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    test_workspace = test_config["workspace"]
    xliff = sdk.catalog_workspace.get_metadata_localization(workspace_id=test_workspace, target_language="fr-FR")

    sdk.catalog_workspace.set_metadata_localization(workspace_id=test_workspace, encoded_xml=xliff)


@gd_vcr.use_cassette(str(_fixtures_dir / "add_metadata_locale.yaml"))
def test_add_metadata_locale(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    test_workspace = test_config["workspace"]

    def translate(
        to_translate: str,
        already_translated: bool = False,
        old_translation: str = "",
    ):
        return f"{to_translate}."

    sdk.catalog_workspace.clean_metadata_localization(workspace_id=test_workspace, target_language="fr-FR")

    xliff_before = sdk.catalog_workspace.get_metadata_localization(workspace_id=test_workspace, target_language="fr-FR")

    sdk.catalog_workspace.add_metadata_locale(
        workspace_id=test_workspace, target_language="fr-FR", translator_func=translate, set_locale=False
    )

    xliff_after = sdk.catalog_workspace.get_metadata_localization(workspace_id=test_workspace, target_language="fr-FR")

    sdk.catalog_workspace.clean_metadata_localization(workspace_id=test_workspace, target_language="fr-FR")

    assert xliff_before != xliff_after


@gd_vcr.use_cassette(str(_fixtures_dir / "clean_metadata_locale.yaml"))
def test_clean_metadata_locale(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    test_workspace = test_config["workspace"]

    def translate(
        to_translate: str,
        already_translated: bool = False,
        old_translation: str = "",
    ):
        return f"{to_translate}."

    sdk.catalog_workspace.clean_metadata_localization(workspace_id=test_workspace, target_language="fr-FR")

    xliff_before = sdk.catalog_workspace.get_metadata_localization(workspace_id=test_workspace, target_language="fr-FR")

    sdk.catalog_workspace.add_metadata_locale(
        workspace_id=test_workspace, target_language="fr-FR", translator_func=translate, set_locale=False
    )

    xliff_after = sdk.catalog_workspace.get_metadata_localization(workspace_id=test_workspace, target_language="fr-FR")

    assert xliff_before != xliff_after

    sdk.catalog_workspace.clean_metadata_localization(workspace_id=test_workspace, target_language="fr-FR")

    xliff_after = sdk.catalog_workspace.get_metadata_localization(workspace_id=test_workspace, target_language="fr-FR")

    assert xliff_before == xliff_after


@gd_vcr.use_cassette(str(_fixtures_dir / "layout_automations.yaml"))
def test_layout_automations(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    workspace_id = test_config["workspace"]

    automations = sdk.catalog_workspace.get_declarative_automations(workspace_id)
    assert len(automations) == 0

    try:
        notification_channel = [
            CatalogDeclarativeNotificationChannel(
                id="webhook", name="Webhook", destination=CatalogWebhook(url="https://webhook.site", token="123")
            ),
        ]
        sdk.catalog_organization.put_declarative_notification_channels(notification_channel)
        automations_expected = [
            CatalogDeclarativeAutomation(
                id="automation",
                title="Automation",
                state="ACTIVE",
                notification_channel=CatalogNotificationChannelIdentifier(id="webhook"),
                schedule=CatalogAutomationSchedule(cron="0 0 * * *", first_run="2023-10-05 14:30:00+00:00"),
                metadata={"key": "value"},
            )
        ]
        sdk.catalog_workspace.put_declarative_automations(workspace_id, automations_expected)
        automations_o = sdk.catalog_workspace.get_declarative_automations(workspace_id)
        assert automations_expected == automations_o
    finally:
        sdk.catalog_workspace.put_declarative_automations(workspace_id, [])
        automations = sdk.catalog_workspace.get_declarative_automations(workspace_id)
        assert len(automations) == 0
        sdk.catalog_organization.put_declarative_notification_channels([])


@gd_vcr.use_cassette(str(_fixtures_dir / "layout_filter_views.yaml"))
def test_layout_filter_views(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    workspace_id = test_config["workspace"]

    filter_views = sdk.catalog_workspace.get_declarative_filter_views(workspace_id)
    assert len(filter_views) == 0

    content = json.loads(
        """
        {
            "filters": [
                {
                  "dateFilter": {
                    "from": "0",
                    "to": "0",
                    "granularity": "GDC.time.month",
                    "type": "relative"
                  }
                },
                {
                  "attributeFilter": {
                    "displayForm": {
                      "identifier": {
                        "id": "demo:campaign_name",
                        "type": "label"
                      }
                    },
                    "negativeSelection": true,
                    "attributeElements": {
                      "uris": []
                    },
                    "localIdentifier": "14b0807447ef4bc28f43e4fc5c337d1d",
                    "filterElementsBy": [],
                    "selectionMode": "multi"
                  }
                }
            ],
            "version": "2"
        }
        """
    )

    try:
        filter_views_expected = [
            CatalogDeclarativeFilterView(
                id="filter_view",
                title="Filter View",
                is_default=True,
                description="Filter View",
                tags=["tag1", "tag2"],
                user=CatalogUserIdentifier(id="demo", type="user"),
                analytical_dashboard=CatalogDeclarativeAnalyticalDashboardIdentifier(
                    id="campaign", type="analyticalDashboard"
                ),
                content=content,
            )
        ]
        sdk.catalog_workspace.put_declarative_filter_views(workspace_id, filter_views_expected)
        filter_views_o = sdk.catalog_workspace.get_declarative_filter_views(workspace_id)
        assert filter_views_expected == filter_views_o
    finally:
        sdk.catalog_workspace.put_declarative_filter_views(workspace_id, [])
        filter_views = sdk.catalog_workspace.get_declarative_filter_views(workspace_id)
        assert len(filter_views) == 0
