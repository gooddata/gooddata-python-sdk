# (C) 2026 GoodData Corporation
"""
Shared test fixtures for catalog tests.

Provides:
- safe_delete: cleanup utility that swallows exceptions
- sdk: session-scoped GoodDataSdk instance
- Snapshot/restore fixtures for staging-safe testing
"""

from __future__ import annotations

import copy
import logging
from pathlib import Path
from typing import Any, Callable

import pytest
from gooddata_sdk import CatalogDeclarativeDataSources, GoodDataSdk
from tests_support.file_utils import load_json

logger = logging.getLogger(__name__)

_current_dir = Path(__file__).parent.absolute()
_credentials_path = _current_dir / "load" / "data_source_credentials" / "data_sources_credentials.yaml"


def _capture_workspace_permissions(sdk: GoodDataSdk, workspaces: list) -> dict:
    """Capture permissions for all workspaces, skipping failures."""
    ws_permissions: dict = {}
    for ws in workspaces:
        try:
            ws_permissions[ws.id] = sdk.catalog_permission.get_declarative_permissions(ws.id)
        except Exception as e:  # noqa: PERF203
            logger.warning(f"Could not capture permissions for workspace {ws.id}: {e}")
    return ws_permissions


def _restore_workspace_permissions(sdk: GoodDataSdk, ws_permissions: dict) -> None:
    """Restore permissions for all workspaces, logging failures."""
    for ws_id, perms in ws_permissions.items():
        try:
            sdk.catalog_permission.put_declarative_permissions(ws_id, perms)
        except Exception as e:  # noqa: PERF203
            logger.warning(f"RESTORE FAILED [permissions for {ws_id}]: {e}")


def safe_delete(func: Callable, *args: Any, **kwargs: Any) -> None:
    """Call a cleanup function, swallowing any exception so it doesn't mask test failures.

    Use this in `finally` blocks instead of bare cleanup calls.
    """
    try:
        func(*args, **kwargs)
    except Exception as e:
        logger.warning(f"Cleanup failed (ignored): {type(e).__name__}: {e}")


def inject_ds_connection(
    data_sources: CatalogDeclarativeDataSources,
    test_config: dict,
    ds_id: str = "demo-test-ds",
) -> CatalogDeclarativeDataSources:
    """Return data_sources with environment-specific connection values injected.

    For local, returns input unchanged (values already match layout files).
    For staging, deep-copies and replaces url/username on the matching data source.
    """
    if not test_config.get("staging", False):
        return data_sources

    result = copy.deepcopy(data_sources)
    for ds in result.data_sources:
        if ds.id == ds_id:
            ds.url = test_config["ds_url"]
            ds.username = test_config["ds_username"]
    return result


def load_expected_data_sources(
    expected_json_path: Path,
    test_config: dict,
) -> CatalogDeclarativeDataSources:
    """Load data sources from expected JSON and inject environment-specific values.

    Combines load_json -> from_dict -> inject_ds_connection.
    """
    data = load_json(expected_json_path)
    ds = CatalogDeclarativeDataSources.from_dict(data)
    return inject_ds_connection(ds, test_config)


@pytest.fixture(scope="session")
def sdk(test_config):
    """Session-scoped GoodDataSdk instance."""
    return GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])


# ---------------------------------------------------------------------------
# Snapshot/restore fixtures
#
# Each fixture captures the current live state via GET before the test runs,
# yields it for the test to use, then restores via PUT in teardown.
# This is environment-agnostic: works against Docker, staging, or anything else.
# ---------------------------------------------------------------------------


@pytest.fixture()
def snapshot_workspaces(sdk):
    """Capture all workspaces, restore after test.

    Silently yields None if the server is unreachable (VCR replay mode).
    """
    try:
        original = sdk.catalog_workspace.get_declarative_workspaces(exclude=["ACTIVITY_INFO"])
    except Exception as e:
        logger.debug(f"snapshot_workspaces: server unreachable, skipping ({e})")
        yield None
        return
    yield original
    try:
        sdk.catalog_workspace.put_declarative_workspaces(original)
    except Exception as e:
        logger.error(f"RESTORE FAILED [workspaces]: {e}")


@pytest.fixture()
def snapshot_workspace_data_filters(sdk):
    """Capture workspace data filters, restore after test.

    Silently yields None if the server is unreachable (VCR replay mode).
    """
    try:
        original = sdk.catalog_workspace.get_declarative_workspace_data_filters()
    except Exception as e:
        logger.debug(f"snapshot_workspace_data_filters: server unreachable, skipping ({e})")
        yield None
        return
    yield original
    try:
        sdk.catalog_workspace.put_declarative_workspace_data_filters(original)
    except Exception as e:
        logger.error(f"RESTORE FAILED [workspace_data_filters]: {e}")


@pytest.fixture()
def snapshot_data_sources(sdk):
    """Capture all data sources, restore after test.

    Silently yields None if the server is unreachable (VCR replay mode).
    """
    try:
        original = sdk.catalog_data_source.get_declarative_data_sources()
    except Exception as e:
        logger.debug(f"snapshot_data_sources: server unreachable, skipping ({e})")
        yield None
        return
    yield original
    try:
        sdk.catalog_data_source.put_declarative_data_sources(original, _credentials_path)
    except Exception as e:
        logger.error(f"RESTORE FAILED [data_sources]: {e}")


@pytest.fixture()
def snapshot_notification_channels(sdk):
    """Capture notification channels, restore after test.

    Silently yields None if the server is unreachable (VCR replay mode).
    """
    try:
        original = sdk.catalog_organization.get_declarative_notification_channels()
    except Exception as e:
        logger.debug(f"snapshot_notification_channels: server unreachable, skipping ({e})")
        yield None
        return
    yield original
    try:
        sdk.catalog_organization.put_declarative_notification_channels(original)
    except Exception as e:
        logger.error(f"RESTORE FAILED [notification_channels]: {e}")


@pytest.fixture()
def snapshot_org_permissions(sdk):
    """Capture organization permissions, restore after test.

    Silently yields None if the server is unreachable (VCR replay mode).
    """
    try:
        original = sdk.catalog_permission.get_declarative_organization_permissions()
    except Exception as e:
        logger.debug(f"snapshot_org_permissions: server unreachable, skipping ({e})")
        yield None
        return
    yield original
    try:
        sdk.catalog_permission.put_declarative_organization_permissions(original)
    except Exception as e:
        logger.error(f"RESTORE FAILED [org_permissions]: {e}")


@pytest.fixture()
def snapshot_permissions(sdk, test_config):
    """Capture workspace permissions for the test workspace, restore after test.

    Silently yields None if the server is unreachable (VCR replay mode).
    """
    ws_id = test_config["workspace"]
    try:
        original = sdk.catalog_permission.get_declarative_permissions(ws_id)
    except Exception as e:
        logger.debug(f"snapshot_permissions: server unreachable, skipping ({e})")
        yield None
        return
    yield original
    try:
        sdk.catalog_permission.put_declarative_permissions(ws_id, original)
    except Exception as e:
        logger.error(f"RESTORE FAILED [permissions for {ws_id}]: {e}")


@pytest.fixture()
def snapshot_full_user_context(sdk):
    """Capture users, groups, AND their permission references.

    Needed for tests that nuke users/groups, because deleting a user
    cascade-deletes permissions referencing that user.

    Restores in correct order: users/groups first, then workspace permissions.
    Silently yields None if the server is unreachable (VCR replay mode).
    """
    try:
        users_groups = sdk.catalog_user.get_declarative_users_user_groups()
    except Exception as e:
        logger.debug(f"snapshot_full_user_context: server unreachable, skipping ({e})")
        yield None
        return

    workspaces = sdk.catalog_workspace.list_workspaces()
    ws_permissions = _capture_workspace_permissions(sdk, workspaces)

    data_sources = sdk.catalog_data_source.get_declarative_data_sources()

    yield users_groups

    # Restore users and groups first
    try:
        sdk.catalog_user.put_declarative_users_user_groups(users_groups)
    except Exception as e:
        logger.error(f"RESTORE FAILED [users_user_groups]: {e}")

    # Restore data sources (includes DS-level permissions)
    try:
        sdk.catalog_data_source.put_declarative_data_sources(data_sources, _credentials_path)
    except Exception as e:
        logger.error(f"RESTORE FAILED [data_sources]: {e}")

    # Restore workspace permissions
    _restore_workspace_permissions(sdk, ws_permissions)
