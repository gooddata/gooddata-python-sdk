# (C) 2026 GoodData Corporation
from __future__ import annotations

import io
from unittest.mock import MagicMock, patch

import pytest

pyarrow = pytest.importorskip("pyarrow")


def _make_ipc_stream_bytes() -> bytes:
    """Return minimal Arrow IPC stream bytes for a one-row table."""
    import pyarrow as pa
    from pyarrow import ipc

    table = pa.table({"x": pa.array([1.0])})
    buf = io.BytesIO()
    with ipc.new_stream(buf, table.schema) as writer:
        writer.write_table(table)
    return buf.getvalue()


class _FakeResponse(io.RawIOBase):
    """Minimal file-like with release_conn to simulate a urllib3 HTTPResponse."""

    def __init__(self, data: bytes) -> None:
        super().__init__()
        self._buf = io.BytesIO(data)
        self.release_conn = MagicMock()

    def read(self, n: int = -1) -> bytes:
        return self._buf.read(n)

    def readable(self) -> bool:
        return True

    def readinto(self, b: bytearray) -> int:
        data = self._buf.read(len(b))
        n = len(data)
        b[:n] = data
        return n


def _make_bare(ipc_bytes: bytes):
    """Return a BareExecutionResponse backed by a mock API client."""
    from gooddata_sdk.compute.model.execution import BareExecutionResponse

    mock_api_client = MagicMock()
    mock_response = _FakeResponse(ipc_bytes)
    mock_api_client.actions_api.api_client.call_api.return_value = mock_response

    afm_exec_response = {
        "execution_response": {
            "links": {"executionResult": "result-id-123"},
            "dimensions": [],
        }
    }
    bare = BareExecutionResponse(
        api_client=mock_api_client,
        workspace_id="ws-id",
        execution_response=afm_exec_response,
    )
    return bare, mock_response


def test_read_result_arrow_returns_table() -> None:
    """read_result_arrow reads the stream from the binary endpoint and returns a pa.Table."""
    import pyarrow as pa

    ipc_bytes = _make_ipc_stream_bytes()
    bare, mock_response = _make_bare(ipc_bytes)

    result = bare.read_result_arrow()

    assert isinstance(result, pa.Table)
    mock_response.release_conn.assert_called_once()


def test_read_result_arrow_requests_stream_format() -> None:
    """read_result_arrow sets Accept: application/vnd.apache.arrow.stream explicitly."""
    ipc_bytes = _make_ipc_stream_bytes()
    bare, _ = _make_bare(ipc_bytes)

    bare.read_result_arrow()

    call_kwargs = bare._actions_api.api_client.call_api.call_args.kwargs
    assert call_kwargs["header_params"]["Accept"] == "application/vnd.apache.arrow.stream"


def test_read_result_arrow_without_cancel_token() -> None:
    """Without a cancel_token the call omits the cancel header."""
    ipc_bytes = _make_ipc_stream_bytes()
    bare, _ = _make_bare(ipc_bytes)

    bare.read_result_arrow()

    call_kwargs = bare._actions_api.api_client.call_api.call_args.kwargs
    assert "X-GDC-CANCEL-TOKEN" not in call_kwargs["header_params"]


def test_read_result_arrow_no_pyarrow_raises() -> None:
    """When pyarrow is not installed, read_result_arrow raises ImportError."""
    from gooddata_sdk.compute.model import execution as _exec_mod

    ipc_bytes = _make_ipc_stream_bytes()
    bare, _ = _make_bare(ipc_bytes)

    with patch.object(_exec_mod, "_ipc", None), pytest.raises(ImportError, match="pyarrow is required"):
        bare.read_result_arrow()
