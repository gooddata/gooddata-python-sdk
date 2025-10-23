# (C) 2025 GoodData Corporation

import logging

import pytest

from gooddata_pipelines.logger.logger import LogObserver
from gooddata_pipelines.provisioning.entities.workspaces.models import (
    WorkspaceFullLoad,
)
from gooddata_pipelines.provisioning.entities.workspaces.workspace_data_validator import (
    WorkspaceDataValidator,
)
from gooddata_pipelines.provisioning.utils.exceptions import (
    WorkspaceException,
)

# Set up logging for the test
logger = logging.getLogger("test_logger")

observer = LogObserver()
observer.subscribe(logger)


@pytest.fixture
def validator(mock_gooddata_api):
    return WorkspaceDataValidator(mock_gooddata_api)


def test_check_basic_integrity_on_valid_data(validator) -> None:
    source_group: list[WorkspaceFullLoad] = [
        WorkspaceFullLoad(
            parent_id="parent_id_1",
            workspace_id="workspace_id_1",
            workspace_name="workspace_name_1",
            workspace_data_filter_id="wdf_id_1",
            workspace_data_filter_values=["wdf_values_1"],
        ),
        WorkspaceFullLoad(
            parent_id="parent_id_2",
            workspace_id="workspace_id_2",
            workspace_name="workspace_name_2",
            workspace_data_filter_id=None,
            workspace_data_filter_values=None,
        ),
        WorkspaceFullLoad(
            parent_id="parent_id_3",
            workspace_id="workspace_id_3",
            workspace_name="workspace_name_3",
            workspace_data_filter_id="wdf_id_1",
            workspace_data_filter_values=["wdf_values_1"],
        ),
        WorkspaceFullLoad(
            parent_id="parent_id_3",
            workspace_id="workspace_id_3",
            workspace_name="workspace_name_3",
            workspace_data_filter_id="wdf_id_2",
            workspace_data_filter_values=["wdf_values_1", "wdf_values_2"],
        ),
    ]

    parent_workspaces, parent_wdf_map = validator._check_basic_integrity(
        source_group
    )

    assert parent_workspaces == {"parent_id_1", "parent_id_2", "parent_id_3"}
    assert parent_wdf_map == {
        "parent_id_1": ["wdf_id_1"],
        "parent_id_3": ["wdf_id_1", "wdf_id_2"],
    }


def test_check_basic_integrity_missing_parent_id(validator) -> None:
    source_group: list[WorkspaceFullLoad] = [
        WorkspaceFullLoad(
            parent_id="",
            workspace_id="workspace_id_1",
            workspace_name="workspace_name_1",
            workspace_data_filter_id=None,
            workspace_data_filter_values=None,
        ),
    ]

    try:
        validator._check_basic_integrity(source_group)
    except Exception as e:
        assert isinstance(e, WorkspaceException)
        assert e.error_message == "Parent ID is not defined in source data."
        assert e.workspace_id == "workspace_id_1"


def test_check_basic_integrity_missing_workspace_id(validator) -> None:
    source_group: list[WorkspaceFullLoad] = [
        WorkspaceFullLoad(
            parent_id="parent_id_1",
            workspace_id="",
            workspace_name="workspace_name_1",
            workspace_data_filter_id=None,
            workspace_data_filter_values=None,
        ),
    ]

    try:
        validator._check_basic_integrity(source_group)
    except Exception as e:
        assert isinstance(e, WorkspaceException)
        assert (
            e.error_message
            == "Workspace ID is not defined for parent parent_id_1"
        )


def test_check_basic_integrity_missing_wdf_id(validator) -> None:
    source_group: list[WorkspaceFullLoad] = [
        WorkspaceFullLoad(
            parent_id="parent_id_1",
            workspace_id="workspace_id_1",
            workspace_name="workspace_name_1",
            workspace_data_filter_id=None,
            workspace_data_filter_values=["some_values"],
        ),
    ]

    try:
        validator._check_basic_integrity(source_group)
    except Exception as e:
        assert isinstance(e, WorkspaceException)
        assert (
            e.error_message
            == "WDF values are provided but WDF ID is not defined."
        )
        assert e.workspace_name == "workspace_name_1"
        assert e.workspace_id == "workspace_id_1"
        assert e.wdf_values == "some_values"


def test_check_basic_integrity_missing_wdf_values(validator) -> None:
    source_group: list[WorkspaceFullLoad] = [
        WorkspaceFullLoad(
            parent_id="parent_id_1",
            workspace_id="workspace_id_1",
            workspace_name="workspace_name_1",
            workspace_data_filter_id="wdf_id_1",
            workspace_data_filter_values=None,
        ),
    ]

    try:
        validator._check_basic_integrity(source_group)
    except Exception as e:
        assert isinstance(e, WorkspaceException)
        assert (
            e.error_message
            == "WDF ID is defined but no WDF values are provided"
        )
        assert e.workspace_id == "workspace_id_1"
        assert e.wdf_id == "wdf_id_1"
        assert e.workspace_name == "workspace_name_1"
        assert e.wdf_values is None


def test_check_basic_integrity_missing_both_ids(validator) -> None:
    source_group: list[WorkspaceFullLoad] = [
        WorkspaceFullLoad(
            parent_id="",
            workspace_id="",
            workspace_name="",
            workspace_data_filter_id=None,
            workspace_data_filter_values=None,
        ),
    ]

    try:
        validator._check_basic_integrity(source_group)
    except Exception as e:
        assert isinstance(e, WorkspaceException)
        assert e.error_message == (
            "Parent ID and workspace ID are not defined for at least one row. Please check the source data."
        )


def test_check_basic_integrity_duplicates_warning(validator, caplog) -> None:
    source_group: list[WorkspaceFullLoad] = [
        WorkspaceFullLoad(
            parent_id="parent_id_1",
            workspace_id="workspace_id_1",
            workspace_name="workspace_name_1",
            workspace_data_filter_id="wdf_id_1",
            workspace_data_filter_values=["wdf_values_1"],
        ),
        WorkspaceFullLoad(
            parent_id="parent_id_1",
            workspace_id="workspace_id_1",
            workspace_name="workspace_name_1",
            workspace_data_filter_id="wdf_id_1",
            workspace_data_filter_values=["wdf_values_1"],
        ),
    ]
    with caplog.at_level("WARNING"):
        validator._check_basic_integrity(source_group)

    warning_log_found = any(
        "Duplicate combinations of parent_id, workspace_id, wdf_id exist in the source data."
        in message
        for message in caplog.messages
    )

    assert warning_log_found, (
        "Warning log for duplicate combinations not found in logs."
    )
