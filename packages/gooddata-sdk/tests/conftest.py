# (C) 2022 GoodData Corporation
import logging
import os
from pathlib import Path
from unittest import mock

import pytest
import yaml

logger = logging.getLogger(__name__)

_current_dir = Path(__file__).parent.absolute()
_credentials_path = _current_dir / "catalog" / "load" / "data_source_credentials" / "data_sources_credentials.yaml"

# ---------------------------------------------------------------------------
# Staging data source connection overrides
# Local Docker:  jdbc:postgresql://postgres:5432/tiger, user=postgres
# Staging k8s:   jdbc:postgresql://cnpg-cluster-pooler:5432/tiger, user=tiger
# ---------------------------------------------------------------------------
_LOCAL_DS_URL = "jdbc:postgresql://postgres:5432/tiger?sslmode=prefer"
_LOCAL_DS_USERNAME = "postgres"
_STAGING_DS_URL = "jdbc:postgresql://cnpg-cluster-pooler:5432/tiger?sslmode=prefer"
_STAGING_DS_USERNAME = "tiger"

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
        help="Absolut path to test configuration",
    )


@pytest.fixture(scope="session")
def test_config(request):
    config_path = Path(request.config.getoption("--gd-test-config"))
    with open(config_path) as f:
        config = yaml.safe_load(f)

    # Override token from TOKEN env var (set by make test-staging TOKEN=...)
    if config.get("staging", False):
        env_token = os.environ.get("TOKEN")
        if env_token:
            config["token"] = env_token

    return config


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
def staging_preflight(test_config):
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
# Staging fixture rewriting — patch JDBC URLs in test layout files
# ---------------------------------------------------------------------------

# Files that contain PostgreSQL JDBC connection strings and need patching
_STAGING_PATCH_FILES = [
    _current_dir
    / "catalog"
    / "load"
    / "gooddata_layouts"
    / "default"
    / "data_sources"
    / "demo-test-ds"
    / "demo-test-ds.yaml",
    _current_dir
    / "catalog"
    / "load_with_locale"
    / "gooddata_layouts"
    / "default"
    / "data_sources"
    / "demo-test-ds"
    / "demo-test-ds.yaml",
    _current_dir / "catalog" / "expected" / "declarative_data_sources.json",
]


_STAGING_BACKUP_SUFFIX = ".staging-backup"


def _backup_path(file_path: Path) -> Path:
    return file_path.with_suffix(file_path.suffix + _STAGING_BACKUP_SUFFIX)


def _restore_from_backup(file_path: Path) -> None:
    """Restore a file from its backup (left over from a previous interrupted run)."""
    backup = _backup_path(file_path)
    if backup.exists():
        file_path.write_text(backup.read_text())
        backup.unlink()
        logger.info(f"Restored from stale backup: {file_path}")


def _patch_file_for_staging(file_path: Path) -> bool:
    """Replace local JDBC URL/username with staging values. Writes backup to disk for crash safety."""
    if not file_path.exists():
        return False
    original = file_path.read_text()
    patched = original.replace(_LOCAL_DS_URL, _STAGING_DS_URL).replace(
        f"username: {_LOCAL_DS_USERNAME}", f"username: {_STAGING_DS_USERNAME}"
    )
    # Also handle JSON format (username as a JSON field)
    patched = patched.replace(f'"username": "{_LOCAL_DS_USERNAME}"', f'"username": "{_STAGING_DS_USERNAME}"')
    if patched != original:
        _backup_path(file_path).write_text(original)
        file_path.write_text(patched)
        logger.info(f"Patched for staging: {file_path}")
        return True
    return False


def _restore_patched_file(file_path: Path) -> None:
    """Restore a file from its backup and remove the backup."""
    backup = _backup_path(file_path)
    if backup.exists():
        file_path.write_text(backup.read_text())
        backup.unlink()
        logger.info(f"Restored original: {file_path}")


def _find_gooddata_layouts_dirs() -> list[Path]:
    """Find all gooddata_layouts directories under the test tree."""
    catalog_dir = _current_dir / "catalog"
    return sorted(catalog_dir.rglob("gooddata_layouts"))


def _create_org_layout_copies(org_id: str) -> list[Path]:
    """Copy default/ -> <org_id>/ in gooddata_layouts dirs that have 'default'.

    Always removes existing <org_id> directories first to avoid stale/incomplete
    copies from previous runs.

    Uses shutil.copytree for cross-platform reliability (Windows CI, Docker, worktrees).
    Also safe for store/translate tests that write into the org directory.

    Returns list of created directories for cleanup.
    """
    import shutil

    created: list[Path] = []
    for layouts_dir in _find_gooddata_layouts_dirs():
        default_dir = layouts_dir / "default"
        org_dir = layouts_dir / org_id
        if default_dir.is_dir():
            if org_dir.exists():
                shutil.rmtree(org_dir)
                logger.info(f"Removed stale layout dir: {org_dir}")
            shutil.copytree(default_dir, org_dir)
            logger.info(f"Copied layout dir: {default_dir} -> {org_dir}")
            created.append(org_dir)
    return created


@pytest.fixture(scope="session", autouse=True)
def staging_patch_fixtures(test_config, staging_preflight):
    """When staging: true, patch test fixtures for the staging environment.

    - Rewrites JDBC connection strings in fixture files
    - Copies gooddata_layouts/default/ -> gooddata_layouts/<org_id>/ so the SDK
      can find layout files (it uses the org ID as the directory name)

    Uses on-disk backups so that interrupted runs self-heal on the next start.
    """
    # Always restore leftover backups from a previous interrupted run
    for fpath in _STAGING_PATCH_FILES:
        _restore_from_backup(fpath)

    if not test_config.get("staging", False):
        yield
        return

    import shutil

    # 1. Patch JDBC connection strings in fixture files
    patched_files = [fpath for fpath in _STAGING_PATCH_FILES if _patch_file_for_staging(fpath)]
    logger.info(f"Patched {len(patched_files)} fixture files for staging")

    # 2. Copy layout dirs (gooddata_layouts/default -> gooddata_layouts/<org_id>)
    from gooddata_sdk import GoodDataSdk

    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    org_id = sdk.catalog_organization.get_organization().id
    copied_dirs = _create_org_layout_copies(org_id)
    logger.info(f"Created {len(copied_dirs)} layout copies for org '{org_id}'")

    yield

    # Restore patched files from backups
    for fpath in patched_files:
        _restore_patched_file(fpath)

    # Remove copied directories
    for d in copied_dirs:
        if d.is_dir():
            shutil.rmtree(d)
            logger.info(f"Removed layout copy: {d}")


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
