# (C) 2025 GoodData Corporation

import os
import shutil
import tempfile
from pathlib import Path
from unittest import mock

import boto3
import pytest
from moto import mock_aws

from gooddata_pipelines.backup_and_restore.backup_manager import (
    BackupBatch,
    BackupManager,
)
from gooddata_pipelines.backup_and_restore.constants import BackupSettings
from gooddata_pipelines.backup_and_restore.models.storage import (
    BackupRestoreConfig,
    LocalStorageConfig,
    S3StorageConfig,
    StorageType,
)
from gooddata_pipelines.backup_and_restore.storage.local_storage import (
    LocalStorage,
)
from gooddata_pipelines.backup_and_restore.storage.s3_storage import S3Storage
from tests.conftest import TEST_DATA_DIR

TEST_DATA_SUBDIR = f"{TEST_DATA_DIR}/backup"

S3_BACKUP_PATH = "some/s3/backup/path/org_id/"
S3_BUCKET = "some-s3-bucket"

LOCAL_CONFIG = BackupRestoreConfig(
    storage_type=StorageType.LOCAL,
    storage=LocalStorageConfig(backup_path=f"{TEST_DATA_DIR}/local_export"),
)

S3_CONFIG = BackupRestoreConfig(
    storage_type=StorageType.S3,
    storage=S3StorageConfig(
        bucket=S3_BUCKET,
        backup_path=S3_BACKUP_PATH,
        profile="default",
    ),
)


@pytest.fixture
def backup_manager(mock_logger):
    with (
        mock.patch.object(BackupManager, "_api", create=True),
        mock.patch(
            "gooddata_pipelines.api.gooddata_api_wrapper.GoodDataApi.get_organization_id",
            return_value="services",
        ),
    ):
        manager = BackupManager.create(
            S3_CONFIG,
            "host",
            "token",
        )
        manager.logger.subscribe(mock_logger)
        return manager


@pytest.fixture()
def s3():
    with mock_aws():
        yield boto3.resource("s3")


@pytest.fixture(scope="function")
def s3_bucket(s3):
    s3.create_bucket(Bucket=S3_BUCKET)
    yield s3.Bucket(S3_BUCKET)


@pytest.fixture(scope="function")
def create_backups_in_bucket(s3_bucket):
    def create_backups(
        ws_ids: list[str], is_e2e: bool = False, suffix: str = "bla"
    ):
        # If used within e2e test, add some suffix to path
        # in order to simulate a more realistic scenario
        path_suffix = f"/{suffix}" if is_e2e else ""

        for ws_id in ws_ids:
            s3_bucket.put_object(
                Bucket=S3_BUCKET, Key=f"{S3_BACKUP_PATH}{ws_id}{path_suffix}/"
            )
            s3_bucket.put_object(
                Bucket=S3_BUCKET,
                Key=f"{S3_BACKUP_PATH}{ws_id}{path_suffix}/gooddata_layouts.zip",
            )

    return create_backups


def assert_not_called_with(target, *args, **kwargs):
    try:
        target.assert_called_with(*args, **kwargs)
    except AssertionError:
        return
    formatted_call = target._format_mock_call_signature(args, kwargs)
    raise AssertionError(f"Expected {formatted_call} to not have been called.")


def test_get_s3_storage(backup_manager):
    """Test get_storage method with literal string as input."""
    s3_storage = backup_manager._get_storage(S3_CONFIG)
    assert isinstance(s3_storage, S3Storage)


def test_get_local_storage(backup_manager):
    """Test get_storage method with literal string as input."""
    local_storage = backup_manager._get_storage(LOCAL_CONFIG)
    assert isinstance(local_storage, LocalStorage)


# Test that zipping gooddata_layouts folder works
def test_archive_gooddata_layouts_to_zip(backup_manager):
    with tempfile.TemporaryDirectory() as tmpdir:
        shutil.copytree(
            Path(
                f"{TEST_DATA_SUBDIR}/test_exports/services/",
            ),
            Path(tmpdir + "/services"),
        )
        backup_manager._archive_gooddata_layouts_to_zip(
            str(Path(tmpdir, "services"))
        )

        zip_exists = os.path.isfile(
            Path(
                tmpdir,
                "services/wsid1/20230713-132759-1_3_1_dev5/gooddata_layouts.zip",
            )
        )
        gooddata_layouts_dir_exists = os.path.isdir(
            Path(
                tmpdir,
                "services/wsid1/20230713-132759-1_3_1_dev5/gooddata_layouts",
            )
        )

        assert gooddata_layouts_dir_exists is False
        assert zip_exists

        zip_exists = os.path.isfile(
            Path(
                tmpdir,
                "services/wsid2/20230713-132759-1_3_1_dev5/gooddata_layouts.zip",
            )
        )
        gooddata_layouts_dir_exists = os.path.isdir(
            Path(
                tmpdir,
                "services/wsid2/20230713-132759-1_3_1_dev5/gooddata_layouts",
            )
        )

        assert gooddata_layouts_dir_exists is False
        assert zip_exists

        zip_exists = os.path.isfile(
            Path(
                tmpdir,
                "services/wsid3/20230713-132759-1_3_1_dev5/gooddata_layouts.zip",
            )
        )
        gooddata_layouts_dir_exists = os.path.isdir(
            Path(
                tmpdir,
                "services/wsid3/20230713-132759-1_3_1_dev5/gooddata_layouts",
            )
        )

        assert gooddata_layouts_dir_exists is False
        assert zip_exists


def test_store_user_data_filters(backup_manager):
    user_data_filters = {
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
    user_data_filter_folderlocation = f"{TEST_DATA_SUBDIR}/test_exports/services/wsid1/20230713-132759-1_3_1_dev5/gooddata_layouts/services/workspaces/wsid1/user_data_filters"
    backup_manager._store_user_data_filters(
        user_data_filters,
        Path(
            f"{TEST_DATA_SUBDIR}/test_exports/services/wsid1/20230713-132759-1_3_1_dev5",
        ),
        "wsid1",
    )
    user_data_filter_folder = os.path.isdir(
        Path(user_data_filter_folderlocation)
    )
    user_data_filter2 = os.path.isfile(
        Path(f"{user_data_filter_folderlocation}/datafilter2.yaml")
    )
    user_data_filter4 = os.path.isfile(
        Path(f"{user_data_filter_folderlocation}/datafilter4.yaml")
    )
    assert user_data_filter_folder
    assert user_data_filter2
    assert user_data_filter4

    count = 0
    for path in os.listdir(user_data_filter_folderlocation):
        if os.path.isfile(os.path.join(user_data_filter_folderlocation, path)):
            count += 1

    assert count == 2

    shutil.rmtree(
        Path(
            f"{TEST_DATA_SUBDIR}/test_exports/services/wsid1/20230713-132759-1_3_1_dev5/gooddata_layouts/services/workspaces/wsid1/user_data_filters",
        )
    )


def test_local_storage_export(backup_manager):
    with tempfile.TemporaryDirectory() as tmpdir:
        org_store_location = Path(tmpdir + "/services")
        shutil.copytree(
            Path(
                f"{TEST_DATA_SUBDIR}/test_exports/services/",
            ),
            org_store_location,
        )
        local_storage = backup_manager._get_storage(LOCAL_CONFIG)

        local_storage.export(
            folder=tmpdir,
            org_id="services",
        )

        local_export_folder_exist = os.path.isdir(
            Path(
                f"{TEST_DATA_DIR}/local_export/services/wsid1/20230713-132759-1_3_1_dev5/gooddata_layouts/services/workspaces/wsid1/analytics_model"
            )
        )
        local_export_folder2_exist = os.path.isdir(
            Path(
                f"{TEST_DATA_DIR}/local_export/services/wsid3/20230713-132759-1_3_1_dev5/gooddata_layouts/services/workspaces/wsid3/ldm"
            )
        )

        local_export_folder3_exist = os.path.isdir(
            Path(
                f"{TEST_DATA_DIR}/local_export/services/wsid3/20230713-132759-1_3_1_dev5/gooddata_layouts/services/workspaces/wsid3/user_data_filters"
            )
        )

        local_export_file_exist = os.path.isfile(
            Path(
                f"{TEST_DATA_DIR}/local_export/services/wsid2/20230713-132759-1_3_1_dev5/gooddata_layouts/services/workspaces/wsid2/analytics_model/analytical_dashboards/id.yaml"
            )
        )
        assert local_export_folder_exist
        assert local_export_folder2_exist
        assert local_export_folder3_exist
        assert local_export_file_exist
        shutil.rmtree(f"{TEST_DATA_DIR}/local_export")


def test_file_upload(backup_manager, s3, s3_bucket):
    backup_manager.storage.export(
        f"{TEST_DATA_SUBDIR}/test_exports", "services"
    )
    s3.Object(
        S3_BUCKET,
        "some/s3/backup/path/org_id/services/wsid2/20230713-132759-1_3_1_dev5/gooddata_layouts/services/workspaces/wsid2/analytics_model/filter_contexts/id.yaml",
    ).load()


def test_split_to_batches(backup_manager):
    workspaces = ["ws1", "ws2", "ws3", "ws4", "ws5"]
    batch_size = 2
    expected_batches = [
        BackupBatch(["ws1", "ws2"]),
        BackupBatch(["ws3", "ws4"]),
        BackupBatch(["ws5"]),
    ]

    result = backup_manager._split_to_batches(workspaces, batch_size)

    for i, batch in enumerate(result):
        assert isinstance(batch, BackupBatch)
        assert batch.list_of_ids == expected_batches[i].list_of_ids


@mock.patch(
    "gooddata_pipelines.backup_and_restore.backup_manager.BackupManager._get_workspace_export"
)
@mock.patch(
    "gooddata_pipelines.backup_and_restore.backup_manager.BackupManager._archive_gooddata_layouts_to_zip"
)
def test_process_batch_success(
    archive_gooddata_layouts_to_zip_mock,
    get_workspace_export_mock,
    backup_manager,
):
    # Mock the storage's export method
    backup_manager.storage = mock.Mock()
    batch = BackupBatch(["ws1", "ws2"])

    backup_manager._process_batch(
        batch=batch,
        retry_count=0,
    )

    get_workspace_export_mock.assert_called_once()
    archive_gooddata_layouts_to_zip_mock.assert_called_once()
    backup_manager.storage.export.assert_called_once()


@mock.patch(
    "gooddata_pipelines.backup_and_restore.backup_manager.BackupManager._get_workspace_export"
)
@mock.patch(
    "gooddata_pipelines.backup_and_restore.backup_manager.BackupManager._archive_gooddata_layouts_to_zip"
)
def test_process_batch_retries_on_exception(
    archive_gooddata_layouts_to_zip_mock,
    get_workspace_export_mock,
    backup_manager,
    capsys,
):
    backup_manager.storage = mock.Mock()
    batch = BackupBatch(["ws1"])

    # Raise exception on first call, succeed on second
    call_count = {"count": 0}

    def fail_once(*args, **kwargs):
        if call_count["count"] == 0:
            call_count["count"] += 1
            raise Exception("fail")
        return None

    get_workspace_export_mock.side_effect = fail_once

    backup_manager._process_batch(
        batch=batch,
    )

    assert get_workspace_export_mock.call_count == 2
    captured = capsys.readouterr()
    assert captured.out.startswith(
        "Exception encountered while processing a batch. Retrying"
    )
    backup_manager.storage.export.assert_called_once()


@mock.patch(
    "gooddata_pipelines.backup_and_restore.backup_manager.BackupManager._get_workspace_export"
)
@mock.patch(
    "gooddata_pipelines.backup_and_restore.backup_manager.BackupManager._archive_gooddata_layouts_to_zip"
)
def test_process_batch_raises_after_max_retries(
    archive_gooddata_layouts_to_zip_mock,
    get_workspace_export_mock,
    backup_manager,
    capsys,
):
    backup_manager.storage = mock.Mock()
    batch = BackupBatch(["ws1"])
    get_workspace_export_mock.side_effect = Exception("fail")

    with pytest.raises(Exception) as exc_info:
        backup_manager._process_batch(
            batch=batch,
            retry_count=BackupSettings.MAX_RETRIES,
        )
    assert str(exc_info.value) == "fail"
    captured = capsys.readouterr()
    assert captured.out.startswith("Batch failed:")
