# (C) 2025 GoodData Corporation

from typing import Any

import orjson
import pytest
from pydantic import ValidationError
from requests import Response

from gooddata_pipelines.provisioning.entities.workspaces.workspace_data_filters import (
    WDFSetting,
    WorkspaceDataFilterManager,
)
from gooddata_pipelines.provisioning.entities.workspaces.workspace_data_parser import (
    WorkspaceDataMaps,
)
from gooddata_pipelines.provisioning.utils.context_objects import (
    WorkspaceContext,
)
from gooddata_pipelines.provisioning.utils.exceptions import WorkspaceException
from tests.data.mock_responses import (
    WDF_ACTUAL_WDF_SETTINGS,
    WDF_VALID_PAYLOAD,
)


@pytest.fixture
def wdf_manager(mock_gooddata_api):
    return WorkspaceDataFilterManager(mock_gooddata_api, WorkspaceDataMaps())


def test_create_wdf_setting_dict(wdf_manager) -> None:
    """Test construction of the WDF setting dictionary."""
    wdf_setting_id: str = "expected_wdf_setting_id"
    wdf_id: str = "expected_wdf_id"
    wdf_values: list[str] = ["expected", "wdf", "values"]

    expected_setting: dict[str, Any] = {
        "data": {
            "attributes": {"filterValues": wdf_values},
            "id": wdf_setting_id,
            "relationships": {
                "workspaceDataFilter": {
                    "data": {"id": wdf_id, "type": "workspaceDataFilter"}
                }
            },
            "type": "workspaceDataFilterSetting",
        }
    }

    result_setting: dict[str, Any] = wdf_manager._create_wdf_setting_dict(
        wdf_setting_id, wdf_id, wdf_values
    )

    assert result_setting == expected_setting, (
        f"Expected {expected_setting}, but got {result_setting}"
    )


def test_get_wdf_settings_for_workspace_valid_payload(
    wdf_manager, mock_gooddata_api, mocker
) -> None:
    """Test processing of a valid response"""
    workspace_id: str = "expected_workspace_id"
    mock_response: Response = Response()
    mock_response.status_code = 200

    payload = WDF_VALID_PAYLOAD

    mock_response._content = orjson.dumps(payload)

    mocker.patch.object(
        mock_gooddata_api,
        "get_workspace_data_filter_settings",
        return_value=mock_response,
    )

    result = wdf_manager._get_wdf_settings_for_workspace(workspace_id)

    assert isinstance(result[0], WDFSetting), (
        f"Expected WDFSetting instance, but got {type(result)}"
    )


def test_get_wdf_settings_for_workspace_invalid_payload(
    wdf_manager, mock_gooddata_api, mocker
) -> None:
    """Test with an invalid payload -> will raise ValidationError / ValueError"""
    workspace_id: str = "expected_workspace_id"
    mock_response: Response = Response()
    mock_response.status_code = 200

    payload = {
        "data": [
            {
                "id": "expected_wdf_setting_id",
                "type": "workspaceDataFilterSetting",
                "attributes": {
                    "missing": "data",
                },
            }
        ]
    }

    mock_response._content = orjson.dumps(payload)

    mocker.patch.object(
        mock_gooddata_api,
        "get_workspace_data_filter_settings",
        return_value=mock_response,
    )

    with pytest.raises(ValidationError):
        wdf_manager._get_wdf_settings_for_workspace(workspace_id)


def test_get_actual_wdf_setting_id_and_values(wdf_manager) -> None:
    """Test getting the actual WDF setting ID and values."""
    data: dict[str, Any] = WDF_VALID_PAYLOAD["data"][0]
    actual_wdf_settings: list[WDFSetting] = [WDFSetting(**data)]
    wdf_id: str = "expected_wdf_id"

    actual_wdf_setting_id, actual_wdf_values = (
        wdf_manager._get_actual_wdf_setting_id_and_values(
            actual_wdf_settings, wdf_id
        )
    )

    assert actual_wdf_setting_id == "expected_wdf_setting_id", (
        f"Expected 'expected_wdf_setting_id', but got {actual_wdf_setting_id}"
    )

    assert actual_wdf_values == ["expected", "wdf", "values"], (
        f"Expected ['expected', 'wdf', 'values'], but got {actual_wdf_values}"
    )


def test_get_actual_wdf_setting_id_and_values_no_actuals(wdf_manager) -> None:
    """Should raise ValueError if no actuals are found"""
    actual_wdf_settings: list[WDFSetting] = []
    wdf_id: str = "expected_wdf_id"

    with pytest.raises(WorkspaceException):
        actual_wdf_setting_id, actual_wdf_values = (
            wdf_manager._get_actual_wdf_setting_id_and_values(
                actual_wdf_settings, wdf_id
            )
        )


def test_get_actual_wdf_setting_id_and_values_no_match(wdf_manager) -> None:
    """Should raise ValueError if no match is found"""
    data: dict[str, Any] = WDF_VALID_PAYLOAD["data"][0]
    actual_wdf_settings: list[WDFSetting] = [WDFSetting(**data)]
    wdf_id: str = "non_existent_wdf_id"

    with pytest.raises(WorkspaceException):
        actual_wdf_setting_id, actual_wdf_values = (
            wdf_manager._get_actual_wdf_setting_id_and_values(
                actual_wdf_settings, wdf_id
            )
        )


def test_compare_wdf_settings(wdf_manager, mocker) -> None:
    """Test the comparison of WDF settings."""
    workspace_context: WorkspaceContext = WorkspaceContext(
        workspace_id="workspace_id", workspace_name="workspace_name"
    )
    source_wdf_config: dict[str, list[str]] = {
        "expected_wdf_id": ["expected", "wdf", "values"],
        "expected_wdf_id_2": ["unexpected", "wdf", "values"],
        "expected_wdf_id_3": ["expected", "wdf", "values"],
    }
    actual_wdf_settings: list[WDFSetting] = [
        WDFSetting(**setting) for setting in WDF_ACTUAL_WDF_SETTINGS
    ]

    mock_put = mocker.patch.object(wdf_manager, "_put_wdf_setting")
    mock_post = mocker.patch.object(wdf_manager, "_post_wdf_setting")
    mock_delete = mocker.patch.object(
        wdf_manager, "_delete_redundant_wdf_setting"
    )

    wdf_manager._compare_wdf_settings(
        workspace_context,
        source_wdf_config,
        actual_wdf_settings,
    )

    assert mock_put.call_count == 1, "Expected one PUT call"
    assert mock_post.call_count == 1, "Expected one POST call"
    assert mock_delete.call_count == 1, "Expected one DELETE call"
