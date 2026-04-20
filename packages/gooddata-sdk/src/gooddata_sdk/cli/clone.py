# (C) 2024 GoodData Corporation
import argparse
import shutil
from pathlib import Path

from gooddata_sdk import GoodDataSdk
from gooddata_sdk.cli.constants import (
    CONFIG_FILE,
    DATA_SOURCES,
    USER_GROUPS,
    USERS,
    WORKSPACES,
    WORKSPACES_DATA_FILTERS,
)
from gooddata_sdk.cli.deploy import _get_workspace_id
from gooddata_sdk.cli.utils import measure_clone


@measure_clone(step="workspaces")
def _clone_workspaces(sdk: GoodDataSdk, path: Path, source_dir: str) -> None:
    config_path = path / CONFIG_FILE
    workspace_id = _get_workspace_id(config_path)
    sdk.catalog_workspace.store_declarative_workspace(workspace_id=workspace_id, layout_root_path=path)


@measure_clone(step="data sources")
def _clone_data_sources(sdk: GoodDataSdk, analytics_root_dir: Path) -> None:
    data_sources = sdk.catalog_data_source.get_declarative_data_sources()
    data_sources.store_to_disk(analytics_root_dir)


@measure_clone(step="user groups")
def _clone_user_groups(sdk: GoodDataSdk, analytics_root_dir: Path) -> None:
    user_groups = sdk.catalog_user.get_declarative_user_groups()
    user_groups.store_to_disk(analytics_root_dir)


@measure_clone(step="users")
def _clone_users(sdk: GoodDataSdk, analytics_root_dir: Path) -> None:
    users = sdk.catalog_user.get_declarative_users()
    users.store_to_disk(analytics_root_dir)


@measure_clone(step="workspace data filters")
def _clone_workspace_data_filters(sdk: GoodDataSdk, analytics_root_dir: Path) -> None:
    workspace_data_filters = sdk.catalog_workspace.get_declarative_workspace_data_filters()
    workspace_data_filters.store_to_disk(analytics_root_dir)


def clone_all(path: Path, source_dir: str) -> None:
    config_path = path / CONFIG_FILE
    sdk = GoodDataSdk.create_from_profile(profiles_path=config_path)
    analytics_root_dir = path / source_dir

    # clean the directory
    if analytics_root_dir.exists():
        shutil.rmtree(analytics_root_dir)
    analytics_root_dir.mkdir()

    print("Cloning the whole organization...")
    _clone_data_sources(sdk, analytics_root_dir)
    _clone_user_groups(sdk, analytics_root_dir)
    _clone_users(sdk, analytics_root_dir)
    _clone_workspace_data_filters(sdk, analytics_root_dir)
    _clone_workspaces(sdk, path, source_dir)
    print("Cloning finished.")


def clone_granular(path: Path, source_dir: str, args: argparse.Namespace) -> None:
    config_path = path / CONFIG_FILE
    analytics_root_dir = path / source_dir
    sdk = GoodDataSdk.create_from_profile(profiles_path=config_path)
    selected_entities = set(args.only)
    if DATA_SOURCES in selected_entities:
        _clone_data_sources(sdk, analytics_root_dir)
    if USER_GROUPS in selected_entities:
        _clone_user_groups(sdk, analytics_root_dir)
    if USERS in selected_entities:
        _clone_users(sdk, analytics_root_dir)
    if WORKSPACES_DATA_FILTERS in selected_entities:
        _clone_workspace_data_filters(sdk, analytics_root_dir)
    if WORKSPACES in selected_entities:
        _clone_workspaces(sdk, path, source_dir)
