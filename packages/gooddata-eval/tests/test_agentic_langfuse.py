# (C) 2026 GoodData Corporation
"""Tests for the agentic Langfuse integration helpers (core/agentic/_langfuse.py).

The HTTP client and the Langfuse API are mocked throughout — no network.
"""
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from gooddata_eval.core.agentic import _langfuse as lf


# --------------------------------------------------------------------------- #
# HttpxLangfuseClient + factories
# --------------------------------------------------------------------------- #
def test_client_requires_credentials(monkeypatch):
    monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
    monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
    with pytest.raises(RuntimeError, match="Langfuse credentials not set"):
        lf.HttpxLangfuseClient()


def test_try_make_langfuse_client_returns_none_without_creds(monkeypatch):
    monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
    monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
    assert lf.try_make_langfuse_client() is None


def test_client_create_score_posts_batch(monkeypatch):
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pub")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sec")
    fake_http = MagicMock()
    with patch.object(lf.httpx, "Client", return_value=fake_http):
        client = lf.HttpxLangfuseClient()
        client.create_score(trace_id="t1", name="assertion", value=True, data_type="BOOLEAN")
    fake_http.post.assert_called_once()
    body = fake_http.post.call_args.kwargs["json"]["batch"][0]["body"]
    assert body["traceId"] == "t1"
    assert body["value"] == 1.0  # bool coerced to numeric


def test_try_make_langfuse_client_succeeds_with_creds(monkeypatch):
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pub")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sec")
    with patch.object(lf.httpx, "Client", return_value=MagicMock()):
        assert isinstance(lf.try_make_langfuse_client(), lf.HttpxLangfuseClient)


# --------------------------------------------------------------------------- #
# get_model_version / build_run_context
# --------------------------------------------------------------------------- #
def test_get_model_version_prefers_override():
    assert lf.get_model_version("h", "t", "ws", override="my-model") == "my-model"


def test_get_model_version_returns_empty_on_sdk_failure():
    # SDK raises (no network) → swallowed, returns "".
    sdk_mod = MagicMock()
    sdk_mod.GoodDataSdk.create.side_effect = RuntimeError("no connection")
    with patch.dict("sys.modules", {"gooddata_sdk": sdk_mod}):
        assert lf.get_model_version("h", "t", "ws") == ""


def test_build_run_context_includes_model_when_known():
    with patch.object(lf, "get_model_version", return_value="gpt-5.2"):
        base, meta = lf.build_run_context("h", "t", "ws", "myds", "2026-06-20_00-00-00", None)
    assert base == "myds_2026-06-20_00-00-00_gpt-5.2"
    assert meta["model_version"] == "gpt-5.2"


def test_build_run_context_omits_model_when_unknown():
    with patch.object(lf, "get_model_version", return_value=""):
        base, meta = lf.build_run_context("h", "t", "ws", "myds", "2026-06-20_00-00-00", None)
    assert base == "myds_2026-06-20_00-00-00"
    assert "model_version" not in meta


# --------------------------------------------------------------------------- #
# score_safe / log_quality_and_value_scores
# --------------------------------------------------------------------------- #
def test_score_safe_noop_without_trace_id():
    fake = MagicMock()
    lf.score_safe(fake, None, name="x", value=1, data_type="NUMERIC")
    fake.create_score.assert_not_called()


def test_score_safe_swallows_errors():
    fake = MagicMock()
    fake.create_score.side_effect = RuntimeError("boom")
    lf.score_safe(fake, "t1", name="x", value=1, data_type="NUMERIC")  # must not raise
    fake.create_score.assert_called_once()


def test_log_quality_and_value_scores_logs_two_scores():
    fake = MagicMock()
    lf.log_quality_and_value_scores(
        fake, "t1", strict_checks={"a": True, "b": False}, latency_sec=6.0, cost_usd=0.01
    )
    names = [c.kwargs["name"] for c in fake.create_score.call_args_list]
    assert "quality_score" in names and "value_score" in names
    quality_call = next(c for c in fake.create_score.call_args_list if c.kwargs["name"] == "quality_score")
    assert quality_call.kwargs["value"] == 0.5  # 1 of 2 strict checks passed


def test_log_quality_and_value_scores_noop_when_empty():
    fake = MagicMock()
    lf.log_quality_and_value_scores(fake, "t1", strict_checks={})
    fake.create_score.assert_not_called()


# --------------------------------------------------------------------------- #
# observe (context manager)
# --------------------------------------------------------------------------- #
def test_observe_creates_dataset_run_item_and_yields_trace_id():
    fake = MagicMock()
    with lf.observe(fake, "trace-1", "item-1", "run-1", {"testing_framework": "x"}) as tid:
        assert tid == "trace-1"
    fake.api.dataset_run_items.create.assert_called_once()


def test_observe_without_trace_id_yields_none_and_does_not_create():
    fake = MagicMock()
    with lf.observe(fake, None, "item-1", "run-1") as tid:
        assert tid is None
    fake.api.dataset_run_items.create.assert_not_called()


def test_observe_sets_trace_version_when_model_version_present():
    fake = MagicMock(spec=["api", "update_trace_version"])
    with lf.observe(fake, "trace-1", "item-1", "run-1", {"model_version": "gpt-5.2"}):
        pass
    fake.update_trace_version.assert_called_once_with("trace-1", "gpt-5.2")


# --------------------------------------------------------------------------- #
# find_traces_per_conversation
# --------------------------------------------------------------------------- #
def test_find_traces_skips_when_skip_env_set(monkeypatch):
    monkeypatch.setenv(lf.SKIP_ENV_VAR, "1")
    result = lf.find_traces_per_conversation(MagicMock(), ["c1", "c2"], datetime.now(timezone.utc))
    assert result == {"c1": None, "c2": None}


def test_find_traces_returns_highest_latency_trace(monkeypatch):
    monkeypatch.delenv(lf.SKIP_ENV_VAR, raising=False)
    monkeypatch.setattr(lf.time, "sleep", lambda _s: None)

    t_lo = SimpleNamespace(session_id="c1", latency=1.0, metadata={})
    t_hi = SimpleNamespace(session_id="c1", latency=5.0, metadata={})

    fake = MagicMock()
    # trace.list signature must lack session_id so local filtering runs
    fake.api.trace.list = lambda **kwargs: SimpleNamespace(data=[t_lo, t_hi])

    result = lf.find_traces_per_conversation(fake, ["c1"], datetime.now(timezone.utc))
    assert result["c1"] is t_hi  # highest latency wins
