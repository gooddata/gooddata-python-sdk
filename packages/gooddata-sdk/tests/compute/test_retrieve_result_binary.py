# (C) 2024 GoodData Corporation
from __future__ import annotations

from unittest.mock import MagicMock

from gooddata_sdk.compute.model.execution import BareExecutionResponse
from gooddata_sdk.compute.service import ComputeService


def _make_mock_execution_response(result_id: str = "test-result-id") -> MagicMock:
    """Create a mock AfmExecutionResponse with a given result_id."""
    mock_response = MagicMock()
    mock_response.__getitem__ = MagicMock(
        side_effect=lambda key: {
            "execution_response": MagicMock(
                __getitem__=MagicMock(
                    side_effect=lambda k: {
                        "links": {"executionResult": result_id},
                        "dimensions": [],
                    }[k]
                )
            )
        }[key]
    )
    return mock_response


def test_bare_execution_response_read_result_binary():
    """Test that BareExecutionResponse.read_result_binary calls retrieve_result_binary correctly."""
    fake_binary_data = b"\x00\x01\x02\x03arrow_data"
    mock_http_response = MagicMock()
    mock_http_response.data = fake_binary_data

    mock_actions_api = MagicMock()
    mock_actions_api.retrieve_result_binary.return_value = mock_http_response

    mock_api_client = MagicMock()
    mock_api_client.actions_api = mock_actions_api

    mock_exec_response = _make_mock_execution_response("result-123")

    bare = BareExecutionResponse(
        api_client=mock_api_client,
        workspace_id="my-workspace",
        execution_response=mock_exec_response,
        cancel_token=None,
    )

    result = bare.read_result_binary()

    assert result == fake_binary_data
    mock_actions_api.retrieve_result_binary.assert_called_once_with(
        workspace_id="my-workspace",
        result_id="result-123",
        _check_return_type=False,
        _preload_content=False,
        _request_timeout=None,
    )


def test_bare_execution_response_read_result_binary_with_cancel_token():
    """Test that BareExecutionResponse.read_result_binary forwards cancel token."""
    fake_binary_data = b"arrow_stream_data"
    mock_http_response = MagicMock()
    mock_http_response.data = fake_binary_data

    mock_actions_api = MagicMock()
    mock_actions_api.retrieve_result_binary.return_value = mock_http_response

    mock_api_client = MagicMock()
    mock_api_client.actions_api = mock_actions_api

    mock_exec_response = _make_mock_execution_response("result-456")

    bare = BareExecutionResponse(
        api_client=mock_api_client,
        workspace_id="my-workspace",
        execution_response=mock_exec_response,
        cancel_token="cancel-token-xyz",
    )

    result = bare.read_result_binary(timeout=30)

    assert result == fake_binary_data
    mock_actions_api.retrieve_result_binary.assert_called_once_with(
        workspace_id="my-workspace",
        result_id="result-456",
        _check_return_type=False,
        _preload_content=False,
        _request_timeout=30,
        x_gdc_cancel_token="cancel-token-xyz",
    )


def test_compute_service_retrieve_result_binary():
    """Test that ComputeService.retrieve_result_binary calls the API correctly."""
    fake_binary_data = b"apache_arrow_file_data"
    mock_http_response = MagicMock()
    mock_http_response.data = fake_binary_data

    mock_actions_api = MagicMock()
    mock_actions_api.retrieve_result_binary.return_value = mock_http_response

    mock_api_client = MagicMock()
    mock_api_client.actions_api = mock_actions_api

    service = ComputeService(api_client=mock_api_client)

    result = service.retrieve_result_binary(
        workspace_id="workspace-1",
        result_id="result-789",
    )

    assert result == fake_binary_data
    mock_actions_api.retrieve_result_binary.assert_called_once_with(
        workspace_id="workspace-1",
        result_id="result-789",
        _check_return_type=False,
        _preload_content=False,
        _request_timeout=None,
    )


def test_compute_service_retrieve_result_binary_with_timeout():
    """Test that ComputeService.retrieve_result_binary forwards timeout correctly."""
    fake_binary_data = b"apache_arrow_stream_data"
    mock_http_response = MagicMock()
    mock_http_response.data = fake_binary_data

    mock_actions_api = MagicMock()
    mock_actions_api.retrieve_result_binary.return_value = mock_http_response

    mock_api_client = MagicMock()
    mock_api_client.actions_api = mock_actions_api

    service = ComputeService(api_client=mock_api_client)

    result = service.retrieve_result_binary(
        workspace_id="workspace-2",
        result_id="result-abc",
        timeout=(5, 60),
    )

    assert result == fake_binary_data
    mock_actions_api.retrieve_result_binary.assert_called_once_with(
        workspace_id="workspace-2",
        result_id="result-abc",
        _check_return_type=False,
        _preload_content=False,
        _request_timeout=(5, 60),
    )
