# (C) 2025 GoodData Corporation
from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from gooddata_sdk.compute.model.execution import ArrowFormat, BareExecutionResponse, Execution


def _make_bare_exec_response(mock_response_data: bytes = b"arrow-data") -> tuple[BareExecutionResponse, MagicMock]:
    """Build a BareExecutionResponse with a mocked actions API."""
    api_client = MagicMock()
    exec_response = MagicMock()
    exec_response.__getitem__ = MagicMock(
        side_effect=lambda k: {"executionResult": "result-id-123"} if k == "links" else MagicMock()
    )
    afm_exec_response = MagicMock()
    afm_exec_response.__getitem__ = MagicMock(
        side_effect=lambda k: exec_response if k == "execution_response" else MagicMock()
    )

    mock_http_response = MagicMock()
    mock_http_response.data = mock_response_data
    api_client.actions_api.retrieve_result_binary.return_value = mock_http_response

    bare = BareExecutionResponse(
        api_client=api_client,
        workspace_id="ws-1",
        execution_response=afm_exec_response,
    )
    return bare, api_client.actions_api


@pytest.mark.parametrize(
    "accept",
    [
        "application/vnd.apache.arrow.file",
        "application/vnd.apache.arrow.stream",
    ],
)
def test_bare_execution_response_read_result_binary_formats(accept: ArrowFormat) -> None:
    """BareExecutionResponse.read_result_binary() passes the correct accept type to the API."""
    expected_bytes = b"\x00\x00\x00arrow"
    bare, actions_api = _make_bare_exec_response(mock_response_data=expected_bytes)

    result = bare.read_result_binary(accept=accept)

    assert result == expected_bytes
    actions_api.retrieve_result_binary.assert_called_once_with(
        workspace_id="ws-1",
        result_id="result-id-123",
        accept_content_types=[accept],
        _check_return_type=False,
        _preload_content=False,
    )


def test_bare_execution_response_read_result_binary_default_format() -> None:
    """BareExecutionResponse.read_result_binary() defaults to arrow.file format."""
    bare, actions_api = _make_bare_exec_response()

    bare.read_result_binary()

    call_kwargs = actions_api.retrieve_result_binary.call_args[1]
    assert call_kwargs["accept_content_types"] == ["application/vnd.apache.arrow.file"]


def test_execution_read_result_binary_delegates() -> None:
    """Execution.read_result_binary() delegates to BareExecutionResponse.read_result_binary()."""
    api_client = MagicMock()
    exec_response = MagicMock()
    exec_response.__getitem__ = MagicMock(
        side_effect=lambda k: {"executionResult": "result-id-456"} if k == "links" else []
    )
    afm_exec_response = MagicMock()
    afm_exec_response.__getitem__ = MagicMock(
        side_effect=lambda k: exec_response if k == "execution_response" else MagicMock()
    )

    expected_bytes = b"stream-data"
    mock_http_response = MagicMock()
    mock_http_response.data = expected_bytes
    api_client.actions_api.retrieve_result_binary.return_value = mock_http_response

    exec_def = MagicMock()
    execution = Execution(
        api_client=api_client,
        workspace_id="ws-2",
        exec_def=exec_def,
        response=afm_exec_response,
    )

    result = execution.read_result_binary(accept="application/vnd.apache.arrow.stream")

    assert result == expected_bytes
    api_client.actions_api.retrieve_result_binary.assert_called_once_with(
        workspace_id="ws-2",
        result_id="result-id-456",
        accept_content_types=["application/vnd.apache.arrow.stream"],
        _check_return_type=False,
        _preload_content=False,
    )
