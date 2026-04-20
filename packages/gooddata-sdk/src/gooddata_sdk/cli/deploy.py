# (C) 2024 GoodData Corporation
import argparse
from pathlib import Path

from gooddata_sdk import (
    CatalogDeclarativeDataSources,
    CatalogDeclarativeUserGroups,
    CatalogDeclarativeUsers,
    CatalogDeclarativeWorkspaceDataFilters,
    GoodDataSdk,
)
from gooddata_sdk.cli.constants import (
    CONFIG_FILE,
    DATA_SOURCES,
    USER_GROUPS,
    USERS,
    WORKSPACES,
    WORKSPACES_DATA_FILTERS,
)
from gooddata_sdk.cli.utils import measure_deploy
from gooddata_sdk.utils import read_layout_from_file


def _get_workspace_id(config_path: Path, profile: str = "default") -> str:
    """Extract workspace_id from the config file profile."""
    content = read_layout_from_file(config_path)
    if not isinstance(content, dict):
        raise ValueError(f"Invalid config file: {config_path}")
    profiles = content.get("profiles", {})
    default_profile_name = content.get("default_profile", profile)
    selected = default_profile_name if profile == "default" else profile
    if selected not in profiles:
        raise ValueError(f"Profile '{selected}' not found in config")
    workspace_id = profiles[selected].get("workspace_id")
    if workspace_id is None:
        raise ValueError(
            f"Profile '{selected}' does not have 'workspace_id' set. Required for deploying workspace objects."
        )
    return workspace_id


@measure_deploy(step=WORKSPACES)
def _deploy_workspaces(sdk: GoodDataSdk, path: Path, source_dir: str) -> None:
    config_path = path / CONFIG_FILE
    workspace_id = _get_workspace_id(config_path)
    workspace_model = sdk.catalog_workspace.load_declarative_workspace(
        workspace_id=workspace_id, layout_root_path=path
    )
    sdk.catalog_workspace.put_declarative_workspace(workspace_id=workspace_id, workspace=workspace_model)


@measure_deploy(step="data sources")
def _deploy_data_sources(sdk: GoodDataSdk, analytics_root_dir: Path, config_path: Path) -> None:
    data_sources = CatalogDeclarativeDataSources.load_from_disk(analytics_root_dir)
    sdk.catalog_data_source.put_declarative_data_sources(data_sources, config_file=config_path)


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


def deploy_all(path: Path, source_dir: str) -> None:
    config_path = path / CONFIG_FILE
    sdk = GoodDataSdk.create_from_profile(profiles_path=config_path)
    analytics_root_dir = path / source_dir

    print("Deploying the whole organization...")
    _deploy_data_sources(sdk, analytics_root_dir, config_path)
    _deploy_user_groups(sdk, analytics_root_dir)
    _deploy_users(sdk, analytics_root_dir)
    _deploy_workspaces(sdk, path, source_dir)
    print("Deployed successfully.")


def deploy_granular(path: Path, source_dir: str, args: argparse.Namespace) -> None:
    config_path = path / CONFIG_FILE
    analytics_root_dir = path / source_dir
    selected_entities = set(args.only)
    sdk = GoodDataSdk.create_from_profile(profiles_path=config_path)
    if DATA_SOURCES in selected_entities:
        _deploy_data_sources(sdk, analytics_root_dir, config_path)
    if USER_GROUPS in selected_entities:
        _deploy_user_groups(sdk, analytics_root_dir)
    if USERS in selected_entities:
        _deploy_users(sdk, analytics_root_dir)
    if WORKSPACES_DATA_FILTERS in selected_entities:
        _deploy_workspace_data_filters(sdk, analytics_root_dir)
    if WORKSPACES in selected_entities:
        _deploy_workspaces(sdk, path, source_dir)
