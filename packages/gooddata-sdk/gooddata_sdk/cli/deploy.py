# (C) 2024 GoodData Corporation
import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

from gooddata_sdk import (
    CatalogDeclarativeDataSources,
    CatalogDeclarativeUserGroups,
    CatalogDeclarativeUsers,
    CatalogDeclarativeWorkspace,
    CatalogDeclarativeWorkspaceDataFilters,
    CatalogDeclarativeWorkspaces,
    GoodDataSdk,
)
from gooddata_sdk.cli.constants import (
    BASE_DIR,
    CONFIG_FILE,
    DATA_SOURCES,
    GD_COMMAND,
    USER_GROUPS,
    USERS,
    WORKSPACES,
    WORKSPACES_DATA_FILTERS,
)
from gooddata_sdk.cli.utils import measure_deploy


def _call_gd_stram_out(path: Path) -> dict[str, Any]:
    """
    Call 'gd stream-out' command to read workspaces file structure using Node.js CLI.
    """
    assert (path / CONFIG_FILE).exists() and (path / BASE_DIR).exists()
    p = subprocess.Popen(
        [GD_COMMAND, "stream-out", "--no-validate"],
        cwd=path,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output, err = p.communicate()
    if err:
        print(f"Deploy workspaces failed with the following error {err=}.")
    data = json.loads(output.decode())
    if WORKSPACES not in data:
        raise ValueError("No workspaces found in the output.")
    return data


@measure_deploy(step=WORKSPACES)
def _deploy_workspaces_with_filters(sdk: GoodDataSdk, path: Path) -> None:
    analytics_root_dir = path / BASE_DIR
    data = _call_gd_stram_out(path)
    workspaces = [CatalogDeclarativeWorkspace.from_dict(workspace_dict) for workspace_dict in data[WORKSPACES]]
    # fetch this information first, so we do not lose them
    workspace_data_filters = CatalogDeclarativeWorkspaceDataFilters.load_from_disk(analytics_root_dir)
    workspaces_o = CatalogDeclarativeWorkspaces(
        workspaces=workspaces, workspace_data_filters=workspace_data_filters.workspace_data_filters
    )
    sdk.catalog_workspace.put_declarative_workspaces(workspaces_o)


@measure_deploy(step="data sources")
def _deploy_data_sources(sdk: GoodDataSdk, analytics_root_dir: Path) -> None:
    data_sources = CatalogDeclarativeDataSources.load_from_disk(analytics_root_dir)
    sdk.catalog_data_source.put_declarative_data_sources(
        data_sources, config_file=analytics_root_dir.parent / "gooddata.yaml"
    )


@measure_deploy(step="user groups")
def _deploy_user_groups(sdk: GoodDataSdk, analytics_root_dir: Path) -> None:
    user_groups = CatalogDeclarativeUserGroups.load_from_disk(analytics_root_dir)
    sdk.catalog_user.put_declarative_user_groups(user_groups)


@measure_deploy(step=USERS)
def _deploy_users(sdk: GoodDataSdk, analytics_root_dir: Path) -> None:
    users = CatalogDeclarativeUsers.load_from_disk(analytics_root_dir)
    sdk.catalog_user.put_declarative_users(users)


@measure_deploy(step="workspace data filters")
def _deploy_workspace_data_filters(sdk: GoodDataSdk, analytics_root_dir: Path) -> None:
    workspace_data_filters = CatalogDeclarativeWorkspaceDataFilters.load_from_disk(analytics_root_dir)
    sdk.catalog_workspace.put_declarative_workspace_data_filters(workspace_data_filters)


def deploy_all(path: Path) -> None:
    init_file = path / CONFIG_FILE
    sdk = GoodDataSdk.create_from_profile(profiles_path=init_file)

    analytics_root_dir = path / BASE_DIR

    print("Deploying the whole organization... ⏲️⏲️⏲️")
    _deploy_data_sources(sdk, analytics_root_dir)
    _deploy_user_groups(sdk, analytics_root_dir)
    _deploy_users(sdk, analytics_root_dir)
    _deploy_workspaces_with_filters(sdk, path)
    print("Deployed 🚀🚀🚀")


def deploy_granular(path: Path, args: argparse.Namespace) -> None:
    init_file = path / CONFIG_FILE
    analytics_root_dir = path / "analytics"
    selected_entities = set(args.only)
    sdk = GoodDataSdk.create_from_profile(profiles_path=init_file)
    if DATA_SOURCES in selected_entities:
        _deploy_data_sources(sdk, analytics_root_dir)
    if USER_GROUPS in selected_entities:
        _deploy_user_groups(sdk, analytics_root_dir)
    if USERS in selected_entities:
        _deploy_users(sdk, analytics_root_dir)
    if WORKSPACES_DATA_FILTERS in selected_entities:
        _deploy_workspace_data_filters(sdk, analytics_root_dir)
    if WORKSPACES in selected_entities:
        _deploy_workspaces_with_filters(sdk, analytics_root_dir.parent)
