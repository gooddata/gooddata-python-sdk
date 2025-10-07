# (C) 2025 GoodData Corporation

import json
import os
import shutil
import tempfile
from pathlib import Path

import pytest

from gooddata_pipelines.backup_and_restore.constants import DirNames
from gooddata_pipelines.backup_and_restore.models.storage import (
    BackupRestoreConfig,
    S3StorageConfig,
    StorageType,
)
from gooddata_pipelines.backup_and_restore.restore_manager import (
    RestoreManager,
    WorkspaceModel,
    WorkspaceToRestore,
)
from gooddata_pipelines.backup_and_restore.storage.s3_storage import S3Storage
from tests.conftest import TEST_DATA_DIR

TEST_DATA_SUBDIR = f"{TEST_DATA_DIR}/restore"

MOCK_DL_TARGET = Path("overlays.zip")
TEST_CONF_PATH = f"{TEST_DATA_SUBDIR}/test_conf.yaml"
TEST_UDF_ROOT = Path(f"{TEST_DATA_SUBDIR}/test_udf_root").absolute()

S3_BACKUP_PATH = "some/s3/backup/path/org_id/"
S3_BUCKET = "some-s3-bucket"


# Small reusable fixtures to avoid repeated mocking
@pytest.fixture()
def conf_s3() -> BackupRestoreConfig:
    return BackupRestoreConfig.from_yaml(TEST_CONF_PATH)


@pytest.fixture()
def s3_storage(mocker, conf_s3: BackupRestoreConfig) -> S3Storage:
    mocker.patch.object(S3Storage, "_verify_connection", return_value=None)
    storage = S3Storage(conf_s3)
    return storage


@pytest.fixture()
def s3_bucket(mocker, s3_storage: S3Storage):
    bucket = mocker.MagicMock()
    s3_storage._bucket = bucket  # type: ignore[attr-defined]
    return bucket


@pytest.fixture()
def gd_api_instance(mocker):
    gd_api_cls = mocker.patch(
        "gooddata_pipelines.backup_and_restore.base_manager.GoodDataApi",
    )
    gd_api_instance = gd_api_cls.return_value
    gd_api_instance._sdk = mocker.MagicMock()
    return gd_api_instance


@pytest.fixture()
def restore_manager(mocker, gd_api_instance) -> RestoreManager:  # noqa: ARG001
    mocker.patch(
        "gooddata_pipelines.backup_and_restore.base_manager.S3Storage",
        autospec=True,
    )
    config = BackupRestoreConfig(
        storage_type=StorageType.S3,
        storage=S3StorageConfig(backup_path=S3_BACKUP_PATH, bucket=S3_BUCKET),
    )
    manager = RestoreManager.create(host="host", token="token", config=config)
    return manager


def assert_not_called_with(target, *args, **kwargs):
    try:
        target.assert_called_with(*args, **kwargs)
    except AssertionError:
        return
    formatted_call = target._format_mock_call_signature(args, kwargs)
    raise AssertionError(f"Expected {formatted_call} to not have been called.")


def test_s3_storage_success(s3_storage, s3_bucket, mocker):
    """S3Storage: downloads the first zip object when objects are present."""
    dir_marker = mocker.MagicMock()
    zip_obj = mocker.MagicMock()
    zip_obj.key = f"{S3_BACKUP_PATH}ws_id/gooddata_layouts.zip"
    s3_bucket.objects.filter.return_value = [dir_marker, zip_obj]

    with tempfile.TemporaryDirectory() as tempdir:
        target_path = Path(tempdir, MOCK_DL_TARGET)
        s3_storage.get_ws_declaration("ws_id/", target_path)
        s3_bucket.download_file.assert_called_once_with(
            zip_obj.key, target_path
        )


def test_s3_storage_no_target_only_dir(s3_storage, s3_bucket, mocker):
    """S3Storage: raises when only a directory marker exists under the prefix."""
    s3_bucket.objects.filter.return_value = [mocker.MagicMock()]
    with pytest.raises(Exception):
        s3_storage.get_ws_declaration("ws_id/", MOCK_DL_TARGET)


def test_s3_storage_no_target(s3_storage, s3_bucket, mocker):
    """S3Storage: raises when no objects exist for the given prefix."""
    s3_bucket.objects.filter.return_value = []
    with pytest.raises(Exception):
        s3_storage.get_ws_declaration("bad_target/", MOCK_DL_TARGET)


def test_restore_empty_workspace(restore_manager, gd_api_instance, mocker):
    """RestoreManager: valid layout triggers LDM and AM PUTs."""
    mocker.patch.object(
        restore_manager.storage, "get_ws_declaration", return_value=None
    )

    def create_empty_ws(_, destination: Path):
        os.mkdir(destination / DirNames.LAYOUTS)
        os.mkdir(destination / DirNames.LAYOUTS / DirNames.LDM)
        os.mkdir(destination / DirNames.LAYOUTS / DirNames.AM)
        os.mkdir(destination / DirNames.LAYOUTS / DirNames.UDF)
        os.mkdir(destination / DirNames.LAYOUTS / "filter_views")
        os.mkdir(destination / DirNames.LAYOUTS / "automations")

    mocker.patch.object(
        restore_manager, "_extract_zip_archive", side_effect=create_empty_ws
    )

    workspace_model = WorkspaceModel(
        logical_data_model=mocker.Mock(), analytics_model=mocker.Mock()
    )
    mocker.patch.object(
        restore_manager, "_load_workspace_layout", return_value=workspace_model
    )
    mocker.patch.object(
        restore_manager,
        "_load_user_data_filters",
        return_value={"userDataFilters": []},
    )
    mocker.patch.object(
        restore_manager, "_load_and_put_filter_views", return_value=None
    )
    mocker.patch.object(
        restore_manager, "_load_and_post_automations", return_value=None
    )

    restore_manager.restore(
        [WorkspaceToRestore(id="ws_id", path="some/ws/path")]
    )

    gd_api_instance._sdk.catalog_workspace_content.put_declarative_ldm.assert_called_once_with(
        "ws_id", workspace_model.logical_data_model
    )
    gd_api_instance._sdk.catalog_workspace_content.put_declarative_analytics_model.assert_called_once_with(
        "ws_id", workspace_model.analytics_model
    )


def test_invalid_workspace_on_disk_is_skipped(
    restore_manager, gd_api_instance, mocker
):
    """RestoreManager: invalid layout (missing dirs) is skipped; no PUTs."""
    mocker.patch.object(
        restore_manager.storage, "get_ws_declaration", return_value=None
    )

    def create_invalid_ws(_, destination: Path):
        os.mkdir(destination / DirNames.LAYOUTS)
        os.mkdir(destination / DirNames.LAYOUTS / DirNames.LDM)
        # Missing AM and UDF

    mocker.patch.object(
        restore_manager, "_extract_zip_archive", side_effect=create_invalid_ws
    )

    restore_manager.restore(
        [WorkspaceToRestore(id="ws_id", path="some/ws/path")]
    )

    gd_api_instance._sdk.catalog_workspace_content.put_declarative_ldm.assert_not_called()
    gd_api_instance._sdk.catalog_workspace_content.put_declarative_analytics_model.assert_not_called()


def test_restore_multiple_workspaces_with_partial_failure(
    restore_manager, gd_api_instance, mocker
):
    """RestoreManager: multiple targets; on partial failure only successful PUTs occur."""
    ws_catalog = gd_api_instance._sdk.catalog_workspace_content

    mocker.patch.object(
        restore_manager.storage, "get_ws_declaration", return_value=None
    )

    def create_valid_ws(_, destination: Path):
        os.mkdir(destination / DirNames.LAYOUTS)
        os.mkdir(destination / DirNames.LAYOUTS / DirNames.LDM)
        os.mkdir(destination / DirNames.LAYOUTS / DirNames.AM)
        os.mkdir(destination / DirNames.LAYOUTS / DirNames.UDF)

    mocker.patch.object(
        restore_manager, "_extract_zip_archive", side_effect=create_valid_ws
    )

    workspace_model = WorkspaceModel(
        logical_data_model=mocker.Mock(), analytics_model=mocker.Mock()
    )
    # First load succeeds, second raises
    mocker.patch.object(
        restore_manager,
        "_load_workspace_layout",
        side_effect=[workspace_model, Exception()],
    )
    mocker.patch.object(
        restore_manager,
        "_load_user_data_filters",
        return_value={"userDataFilters": []},
    )

    targets = [
        WorkspaceToRestore(id="ws_id_1", path="ws_id_1"),
        WorkspaceToRestore(id="ws_id_2", path="ws_id_1"),
    ]
    restore_manager.restore(targets)

    ws_catalog.put_declarative_ldm.assert_any_call(
        "ws_id_1", workspace_model.logical_data_model
    )
    ws_catalog.put_declarative_analytics_model.assert_any_call(
        "ws_id_1", workspace_model.analytics_model
    )
    assert_not_called_with(
        ws_catalog.put_declarative_ldm, "ws_id_2", mocker.ANY
    )
    assert_not_called_with(
        ws_catalog.put_declarative_analytics_model, "ws_id_2", mocker.ANY
    )


def test_load_user_data_filters_reads_yaml(mocker):
    """RestoreManager: reads YAML UDFs into expected API body structure."""
    mocker.patch(
        "gooddata_pipelines.backup_and_restore.base_manager.S3Storage",
        autospec=True,
    )
    gd_api_cls = mocker.patch(
        "gooddata_pipelines.backup_and_restore.base_manager.GoodDataApi",
    )
    gd_api_instance = gd_api_cls.return_value
    gd_api_instance._sdk = mocker.MagicMock()

    config = BackupRestoreConfig(
        storage_type=StorageType.S3,
        storage=S3StorageConfig(backup_path=S3_BACKUP_PATH, bucket=S3_BUCKET),
    )
    manager = RestoreManager.create(host="host", token="token", config=config)

    # Build a clean temp directory and copy only YAML fixtures from test data
    with tempfile.TemporaryDirectory() as tempdir:
        temp_root = Path(tempdir)
        src_udf_dir = (TEST_UDF_ROOT / DirNames.UDF).absolute()
        dst_udf_dir = temp_root / DirNames.UDF

        def ignore_non_yaml(_dir, names):
            return [n for n in names if not n.endswith(".yaml")]

        shutil.copytree(src_udf_dir, dst_udf_dir, ignore=ignore_non_yaml)

        result = manager._load_user_data_filters(temp_root)

    user_data_filters_expected = {
        "userDataFilters": [
            {
                "id": "datafilter2",
                "maql": '{label/campaign_channels.category} = "1"',
                "title": "Status filter",
                "user": {
                    "id": "5c867a8a-12af-45bf-8d85-c7d16bedebd1",
                    "type": "user",
                },
            },
            {
                "id": "datafilter4",
                "maql": '{label/campaign_channels.category} = "1"',
                "title": "Status filter",
                "user": {
                    "id": "5c867a8a-12af-45bf-8d85-c7d16bedebd1",
                    "type": "user",
                },
            },
        ]
    }

    sorted_result = sorted(
        json.dumps(d, sort_keys=True) for d in result["userDataFilters"]
    )
    sorted_expected = sorted(
        json.dumps(d, sort_keys=True)
        for d in user_data_filters_expected["userDataFilters"]
    )

    assert sorted_result == sorted_expected


def test_manager_create_uses_s3_storage(mocker):
    """RestoreManager.create: builds S3 storage when storage_type is S3."""
    storage_cls = mocker.patch(
        "gooddata_pipelines.backup_and_restore.base_manager.S3Storage",
        autospec=True,
    )
    mocker.patch(
        "gooddata_pipelines.backup_and_restore.base_manager.GoodDataApi",
    )
    config = BackupRestoreConfig(
        storage_type=StorageType.S3,
        storage=S3StorageConfig(backup_path=S3_BACKUP_PATH, bucket=S3_BUCKET),
    )
    RestoreManager.create(host="host", token="token", config=config)
    storage_cls.assert_called_once()


def test_manager_create_from_profile(mocker):
    """RestoreManager.create_from_profile: uses profile content to init GoodDataApi."""
    mocker.patch(
        "gooddata_pipelines.backup_and_restore.base_manager.S3Storage",
        autospec=True,
    )
    gd_api_cls = mocker.patch(
        "gooddata_pipelines.backup_and_restore.base_manager.GoodDataApi",
    )
    mocker.patch(
        "gooddata_pipelines.backup_and_restore.base_manager.profile_content",
        return_value={"host": "h", "token": "t"},
    )

    config = BackupRestoreConfig(
        storage_type=StorageType.S3,
        storage=S3StorageConfig(backup_path=S3_BACKUP_PATH, bucket=S3_BUCKET),
    )
    RestoreManager.create_from_profile(config)
    gd_api_cls.assert_called_once_with("h", "t")
