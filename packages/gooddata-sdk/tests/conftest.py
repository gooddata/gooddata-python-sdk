# (C) 2022 GoodData Corporation
import logging
import os
from pathlib import Path
from unittest import mock

import pytest
import yaml
from tests_support.vcrpy_utils import configure_normalization

logger = logging.getLogger(__name__)

_current_dir = Path(__file__).parent.absolute()
_credentials_path = _current_dir / "catalog" / "load" / "data_source_credentials" / "data_sources_credentials.yaml"

# ---------------------------------------------------------------------------
# Failure tracker — used by session snapshot to decide whether to restore
# ---------------------------------------------------------------------------
_session_has_failures = False


def pytest_runtest_makereport(item, call):
    """Track whether any test has failed during the session."""
    global _session_has_failures
    if call.excinfo is not None:
        _session_has_failures = True


def pytest_addoption(parser):
    default_config_path = Path(__file__).parent / "gd_test_config.yaml"
    parser.addoption(
        "--gd-test-config",
        action="store",
        default=str(default_config_path),
        help="Path to test configuration file",
    )


@pytest.fixture(scope="session")
def test_config(request):
    config_path = Path(request.config.getoption("--gd-test-config"))
    with open(config_path) as f:
        config = yaml.safe_load(f)

    # Merge environment-specific overrides into top-level config
    env_name = os.environ.get("GD_TEST_ENV", "local")
    environments = config.pop("environments", {})
    if env_name in environments:
        config.update(environments[env_name])

    # Override secrets from env vars (staging CI passes these)
    env_token = os.environ.get("TOKEN")
    if env_token:
        config["token"] = env_token
    env_ds_password = os.environ.get("DS_PASSWORD")
    if env_ds_password:
        config["ds_password"] = env_ds_password

    # Initialize VCR cassette normalization so recordings from any environment
    # produce identical cassette files (canonical localhost values).
    configure_normalization(config)

    return config


@pytest.fixture(scope="session", autouse=True)
def _patch_ds_credentials(test_config):
    """Override demo-test-ds password in memory.

    The credentials file (data_sources_credentials.yaml) contains a placeholder
    value for demo-test-ds. This fixture patches _credentials_from_file() to
    replace it with the real password — from DS_PASSWORD env var (staging) or
    from the test config ds_password (local).
    """
    ds_password = os.environ.get("DS_PASSWORD") or test_config.get("ds_password")
    if not ds_password:
        yield
        return

    from gooddata_sdk.catalog.data_source.service import CatalogDataSourceService

    original = CatalogDataSourceService._credentials_from_file

    @staticmethod
    def _patched_credentials_from_file(credentials_path):
        credentials = original(credentials_path)
        if "demo-test-ds" in credentials:
            credentials["demo-test-ds"] = ds_password
        return credentials

    CatalogDataSourceService._credentials_from_file = _patched_credentials_from_file
    logger.info("Patched _credentials_from_file to override demo-test-ds password in memory")

    yield

    CatalogDataSourceService._credentials_from_file = staticmethod(original)


@pytest.fixture()
def setenvvar(monkeypatch):
    with mock.patch.dict(os.environ, clear=True):
        envvars = {"OK_TOKEN": "secret_password", "ENV_VAR": "secret"}
        for k, v in envvars.items():
            monkeypatch.setenv(k, v)
        yield


# ---------------------------------------------------------------------------
# Staging preflight — validates connectivity and required resources
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session", autouse=True)
def staging_preflight(test_config, _patch_ds_credentials):
    """When staging: true, verify connectivity and that required resources exist.

    Calls pytest.exit() on failure so the session stops immediately with a clear
    diagnostic instead of cascading into hundreds of confusing errors.
    """
    if not test_config.get("staging", False):
        yield
        return

    from gooddata_sdk import GoodDataSdk

    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    # 1. Connectivity check
    try:
        if not sdk.support.is_available:
            pytest.exit("PREFLIGHT FAILED: server responded but is_available returned False")
    except Exception as e:
        pytest.exit(f"PREFLIGHT FAILED: cannot reach {test_config['host']} — {type(e).__name__}: {e}")

    # 2. Required resources check
    missing = []
    user_ids = set()

    # Workspaces
    try:
        workspace_ids = {ws.id for ws in sdk.catalog_workspace.list_workspaces()}
        for ws_id in [test_config["workspace"], test_config["workspace_with_parent"]]:
            if ws_id not in workspace_ids:
                missing.append(f"workspace '{ws_id}'")  # noqa: PERF401
    except Exception as e:
        missing.append(f"workspaces (list failed: {e})")

    # Data source
    try:
        ds_ids = {ds.id for ds in sdk.catalog_data_source.list_data_sources()}
        if test_config["data_source"] not in ds_ids:
            missing.append(f"data_source '{test_config['data_source']}'")
    except Exception as e:
        missing.append(f"data_sources (list failed: {e})")

    # Users (reuse list from auto-discovery if available)
    if user_ids:
        for uid in [test_config["demo_user"], test_config["test_user"]]:
            if uid not in user_ids:
                missing.append(f"user '{uid}'")  # noqa: PERF401
    else:
        try:
            user_ids = {u.id for u in sdk.catalog_user.list_users()}
            for uid in [test_config["demo_user"], test_config["test_user"]]:
                if uid not in user_ids:
                    missing.append(f"user '{uid}'")  # noqa: PERF401
        except Exception as e:
            missing.append(f"users (list failed: {e})")

    # User groups
    try:
        group_ids = {g.id for g in sdk.catalog_user.list_user_groups()}
        for gid in [test_config["admin_user_group"], test_config["test_user_group"]]:
            if gid not in group_ids:
                missing.append(f"user_group '{gid}'")  # noqa: PERF401
    except Exception as e:
        missing.append(f"user_groups (list failed: {e})")

    if missing:
        report = "\n  - ".join(missing)
        pytest.exit(f"PREFLIGHT FAILED: required resources missing:\n  - {report}")

    logger.info("Staging preflight passed — all resources present")
    yield


# ---------------------------------------------------------------------------
# Staging org_id symlinks — so SDK finds layouts at gooddata_layouts/{org_id}/
# ---------------------------------------------------------------------------

_LAYOUT_ROOTS = [
    _current_dir / "catalog" / "load" / "gooddata_layouts",
    _current_dir / "catalog" / "load" / "workspace_content" / "gooddata_layouts",
    _current_dir / "catalog" / "load_with_locale" / "gooddata_layouts",
]


@pytest.fixture(scope="session", autouse=True)
def staging_org_symlinks(test_config, staging_preflight):
    """For staging: create org_id symlinks so the SDK finds layouts at the right path.

    Layout files are stored under gooddata_layouts/default/. On staging, the SDK
    resolves org_id to the real staging value. Symlinks make both paths point to
    the same directory.
    """
    org_id = test_config.get("org_id", "default")
    symlinks_created = []
    if org_id != "default":
        for layout_root in _LAYOUT_ROOTS:
            symlink = layout_root / org_id
            if not symlink.exists():
                symlink.symlink_to("default")
                symlinks_created.append(symlink)
        logger.info(f"Created org_id symlinks for '{org_id}'")

    yield

    for symlink in symlinks_created:
        symlink.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# Session-level snapshot/restore — safety net for staging
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session", autouse=True)
def staging_session_snapshot(test_config, staging_preflight):
    """When staging: true, capture full environment state before tests run.

    On teardown, if any test failed, restore everything to the captured state.
    This is the last line of defense — per-test snapshot fixtures are the first.
    """
    if not test_config.get("staging", False):
        yield
        return

    from gooddata_sdk import GoodDataSdk

    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    # --- Capture ---
    snapshot = {}
    logger.info("Capturing session snapshot...")

    try:
        snapshot["users_groups"] = sdk.catalog_user.get_declarative_users_user_groups()
    except Exception as e:
        logger.error(f"Snapshot capture failed [users_groups]: {e}")

    try:
        snapshot["data_sources"] = sdk.catalog_data_source.get_declarative_data_sources()
    except Exception as e:
        logger.error(f"Snapshot capture failed [data_sources]: {e}")

    try:
        snapshot["workspaces"] = sdk.catalog_workspace.get_declarative_workspaces(exclude=["ACTIVITY_INFO"])
    except Exception as e:
        logger.error(f"Snapshot capture failed [workspaces]: {e}")

    try:
        snapshot["workspace_data_filters"] = sdk.catalog_workspace.get_declarative_workspace_data_filters()
    except Exception as e:
        logger.error(f"Snapshot capture failed [workspace_data_filters]: {e}")

    try:
        snapshot["org_permissions"] = sdk.catalog_permission.get_declarative_organization_permissions()
    except Exception as e:
        logger.error(f"Snapshot capture failed [org_permissions]: {e}")

    try:
        snapshot["notification_channels"] = sdk.catalog_organization.get_declarative_notification_channels()
    except Exception as e:
        logger.error(f"Snapshot capture failed [notification_channels]: {e}")

    # Per-workspace permissions
    ws_permissions = {}
    try:
        for ws in sdk.catalog_workspace.list_workspaces():
            try:
                ws_permissions[ws.id] = sdk.catalog_permission.get_declarative_permissions(ws.id)
            except Exception as e:  # noqa: PERF203
                logger.warning(f"Could not capture permissions for workspace {ws.id}: {e}")
    except Exception as e:
        logger.error(f"Snapshot capture failed [workspace list for permissions]: {e}")
    snapshot["ws_permissions"] = ws_permissions

    logger.info("Session snapshot captured")

    # --- Tests run ---
    yield snapshot

    # --- Restore (only if failures) ---
    if not _session_has_failures:
        logger.info("All tests passed — skipping session restore")
        return

    logger.warning("Test failures detected — restoring session snapshot...")

    # Restore order matters: users/groups → data sources → workspaces →
    # workspace data filters → org permissions → notification channels →
    # per-workspace permissions

    if "users_groups" in snapshot:
        try:
            sdk.catalog_user.put_declarative_users_user_groups(snapshot["users_groups"])
            logger.info("Restored [users_groups]")
        except Exception as e:
            logger.error(f"RESTORE FAILED [users_groups]: {e}")

    if "data_sources" in snapshot:
        try:
            sdk.catalog_data_source.put_declarative_data_sources(snapshot["data_sources"], _credentials_path)
            logger.info("Restored [data_sources]")
        except Exception as e:
            logger.error(f"RESTORE FAILED [data_sources]: {e}")

    if "workspaces" in snapshot:
        try:
            sdk.catalog_workspace.put_declarative_workspaces(snapshot["workspaces"])
            logger.info("Restored [workspaces]")
        except Exception as e:
            logger.error(f"RESTORE FAILED [workspaces]: {e}")

    if "workspace_data_filters" in snapshot:
        try:
            sdk.catalog_workspace.put_declarative_workspace_data_filters(snapshot["workspace_data_filters"])
            logger.info("Restored [workspace_data_filters]")
        except Exception as e:
            logger.error(f"RESTORE FAILED [workspace_data_filters]: {e}")

    if "org_permissions" in snapshot:
        try:
            sdk.catalog_permission.put_declarative_organization_permissions(snapshot["org_permissions"])
            logger.info("Restored [org_permissions]")
        except Exception as e:
            logger.error(f"RESTORE FAILED [org_permissions]: {e}")

    if "notification_channels" in snapshot:
        try:
            sdk.catalog_organization.put_declarative_notification_channels(snapshot["notification_channels"])
            logger.info("Restored [notification_channels]")
        except Exception as e:
            logger.error(f"RESTORE FAILED [notification_channels]: {e}")

    for ws_id, perms in snapshot.get("ws_permissions", {}).items():
        try:
            sdk.catalog_permission.put_declarative_permissions(ws_id, perms)
            logger.info(f"Restored [permissions for {ws_id}]")
        except Exception as e:  # noqa: PERF203
            logger.warning(f"RESTORE FAILED [permissions for {ws_id}]: {e}")
