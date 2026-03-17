# (C) 2026 GoodData Corporation
from __future__ import annotations

from unittest.mock import MagicMock, patch

from gooddata_sdk.compute.model.execution import BareExecutionResponse


def _make_bare_exec_response(cancel_token: str | None = None) -> BareExecutionResponse:
    """Build a BareExecutionResponse with a mocked API client."""
    api_client = MagicMock()
    execution_response = {
        "execution_response": {
            "links": {"executionResult": "result-123"},
            "dimensions": [],
        }
    }
    return BareExecutionResponse(
        api_client=api_client,
        workspace_id="ws-1",
        execution_response=execution_response,
        cancel_token=cancel_token,
    )


def test_read_result_binary_no_cancel_token():
    """read_result_binary passes no cancel token when neither provided nor stored."""
    resp = _make_bare_exec_response(cancel_token=None)
    mock_binary = MagicMock()
    resp._actions_api.retrieve_result_binary.return_value = mock_binary

    result = resp.read_result_binary()

    resp._actions_api.retrieve_result_binary.assert_called_once_with(
        workspace_id="ws-1",
        result_id="result-123",
        _check_return_type=False,
    )
    assert result is mock_binary


def test_read_result_binary_with_stored_cancel_token():
    """read_result_binary forwards the stored cancel token when no explicit token given."""
    resp = _make_bare_exec_response(cancel_token="stored-token")
    mock_binary = MagicMock()
    resp._actions_api.retrieve_result_binary.return_value = mock_binary

    result = resp.read_result_binary()

    resp._actions_api.retrieve_result_binary.assert_called_once_with(
        workspace_id="ws-1",
        result_id="result-123",
        _check_return_type=False,
        x_gdc_cancel_token="stored-token",
    )
    assert result is mock_binary


def test_read_result_binary_with_explicit_cancel_token():
    """read_result_binary uses explicit cancel token, overriding the stored one."""
    resp = _make_bare_exec_response(cancel_token="stored-token")
    mock_binary = MagicMock()
    resp._actions_api.retrieve_result_binary.return_value = mock_binary

    result = resp.read_result_binary(x_gdc_cancel_token="explicit-token")

    resp._actions_api.retrieve_result_binary.assert_called_once_with(
        workspace_id="ws-1",
        result_id="result-123",
        _check_return_type=False,
        x_gdc_cancel_token="explicit-token",
    )
    assert result is mock_binary


def test_read_result_binary_does_not_pass_paging_params():
    """read_result_binary must NOT pass offset, limit, or excludedTotalDimensions."""
    resp = _make_bare_exec_response()
    resp._actions_api.retrieve_result_binary.return_value = MagicMock()

    resp.read_result_binary()

    call_kwargs = resp._actions_api.retrieve_result_binary.call_args[1]
    assert "offset" not in call_kwargs
    assert "limit" not in call_kwargs
    assert "excluded_total_dimensions" not in call_kwargs
