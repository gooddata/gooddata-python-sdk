# (C) 2026 GoodData Corporation
import hashlib
import re

import pytest
from gooddata_eval.core.langfuse.item_scope import (
    ItemTraceScope,
    current_scope,
    item_scope,
    trace_ids_for,
)

_SCOPE = ItemTraceScope(base_name="b", suffix_runs=False, dataset_id="d", item_id="i")


def test_trace_id_is_the_langfuse_sdk_seeded_trace_id():
    # langfuse.Langfuse.create_trace_id(seed=...) -- gen-ai and Langfuse tooling agree on it.
    assert trace_ids_for("conv-1")[0] == hashlib.sha256(b"conv-1").digest()[:16].hex()


def test_ids_are_deterministic_well_formed_and_distinct():
    trace_id, span_id = trace_ids_for("conv-1")
    assert trace_ids_for("conv-1") == (trace_id, span_id)
    assert re.fullmatch(r"[0-9a-f]{32}", trace_id)
    assert re.fullmatch(r"[0-9a-f]{16}", span_id)
    assert not trace_id.startswith(span_id)
    assert trace_ids_for("conv-2") != (trace_id, span_id)


def test_run_name_is_suffixed_only_when_the_item_has_several_runs():
    assert _SCOPE.run_name(0) == "b"
    assert ItemTraceScope("b", True, "d", "i").run_name(1) == "b_run1"


def test_the_scope_is_visible_only_inside_the_block_and_only_with_the_switch_on(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("GOODDATA_EVAL_JOIN_GENAI_TRACE", "1")
    with item_scope(_SCOPE):
        assert current_scope() is _SCOPE
        monkeypatch.setenv("GOODDATA_EVAL_JOIN_GENAI_TRACE", "0")
        assert current_scope() is None
    monkeypatch.setenv("GOODDATA_EVAL_JOIN_GENAI_TRACE", "1")
    assert current_scope() is None


def test_the_scope_is_reset_when_the_run_raises(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("GOODDATA_EVAL_JOIN_GENAI_TRACE", "1")
    with pytest.raises(RuntimeError), item_scope(_SCOPE):
        raise RuntimeError
    assert current_scope() is None
