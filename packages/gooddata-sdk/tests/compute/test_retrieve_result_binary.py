# (C) 2025 GoodData Corporation
from __future__ import annotations

from unittest.mock import MagicMock

from gooddata_sdk.compute.service import ComputeService


def _make_service(mock_actions_api: MagicMock) -> ComputeService:
    api_client = MagicMock()
    api_client.actions_api = mock_actions_api
    api_client.entities_api = MagicMock()
    return ComputeService(api_client)


def test_retrieve_result_binary_calls_api_with_correct_params():
    mock_actions_api = MagicMock()
    expected_bytes = b"arrow_binary_data"
    mock_response = MagicMock()
    mock_response.data = expected_bytes
    mock_actions_api.retrieve_result_binary.return_value = mock_response

    service = _make_service(mock_actions_api)
    result = service.retrieve_result_binary("ws1", "result-42")

    mock_actions_api.retrieve_result_binary.assert_called_once_with(
        workspace_id="ws1",
        result_id="result-42",
        _check_return_type=False,
        _preload_content=False,
    )
    assert result == expected_bytes


def test_retrieve_result_binary_returns_bytes():
    mock_actions_api = MagicMock()
    mock_response = MagicMock()
    mock_response.data = b"\x00\x01\x02"
    mock_actions_api.retrieve_result_binary.return_value = mock_response

    service = _make_service(mock_actions_api)
    result = service.retrieve_result_binary("workspace", "rid")

    assert isinstance(result, bytes)
    assert result == b"\x00\x01\x02"
