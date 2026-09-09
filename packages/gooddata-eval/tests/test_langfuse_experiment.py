# (C) 2026 GoodData Corporation
from __future__ import annotations

import json
from datetime import datetime, timezone

from gooddata_eval.core.langfuse.experiment import (
    ExperimentItem,
    ExperimentRun,
    ScoreTarget,
    build_experiment_root_span,
    experiment_id_for,
)


def _attr(span, key):
    for attribute in span.attributes:
        if attribute["key"] == key:
            return attribute
    return None


def test_experiment_id_for_is_stable():
    assert experiment_id_for("run0") == experiment_id_for("run0")


def test_experiment_id_for_differs_by_run_name():
    assert experiment_id_for("run0") != experiment_id_for("run1")


def test_build_experiment_root_span_root_observation_id_equals_span_id():
    run = ExperimentRun(name="run0", dataset_id="ds-1")
    item = ExperimentItem(item_id="item-1")
    span = build_experiment_root_span(
        run,
        item,
        start=datetime(2025, 1, 1, tzinfo=timezone.utc),
        end=datetime(2025, 1, 1, tzinfo=timezone.utc),
        trace_name="gd-eval: q",
    )
    attr = _attr(span, "langfuse.experiment.item.root_observation_id")
    assert attr["value"]["stringValue"] == span.span_id


def test_build_experiment_root_span_dataset_id_only_when_run_given():
    item = ExperimentItem(item_id="item-1")
    span_without_run = build_experiment_root_span(
        None,
        item,
        start=datetime(2025, 1, 1, tzinfo=timezone.utc),
        end=datetime(2025, 1, 1, tzinfo=timezone.utc),
        trace_name="gd-eval: q",
    )
    assert _attr(span_without_run, "langfuse.experiment.dataset.id") is None

    run = ExperimentRun(name="run0", dataset_id="ds-1")
    span_with_run = build_experiment_root_span(
        run,
        item,
        start=datetime(2025, 1, 1, tzinfo=timezone.utc),
        end=datetime(2025, 1, 1, tzinfo=timezone.utc),
        trace_name="gd-eval: q",
    )
    assert _attr(span_with_run, "langfuse.experiment.dataset.id")["value"]["stringValue"] == "ds-1"


def test_build_experiment_root_span_no_experiment_attrs_when_run_none():
    item = ExperimentItem(item_id="item-1")
    span = build_experiment_root_span(
        None,
        item,
        start=datetime(2025, 1, 1, tzinfo=timezone.utc),
        end=datetime(2025, 1, 1, tzinfo=timezone.utc),
        trace_name="gd-eval: q",
    )
    assert not any(a["key"].startswith("langfuse.experiment.") for a in span.attributes)
    # still a valid observation span
    assert _attr(span, "langfuse.observation.type")["value"]["stringValue"] == "span"
    assert _attr(span, "langfuse.trace.name")["value"]["stringValue"] == "gd-eval: q"


def test_build_experiment_root_span_io_json_strings():
    run = ExperimentRun(name="run0", dataset_id="ds-1")
    item = ExperimentItem(item_id="item-1", input={"question": "q"}, output={"passed": True})
    span = build_experiment_root_span(
        run,
        item,
        start=datetime(2025, 1, 1, tzinfo=timezone.utc),
        end=datetime(2025, 1, 1, tzinfo=timezone.utc),
        trace_name="gd-eval: q",
    )
    input_attr = _attr(span, "langfuse.observation.input")
    output_attr = _attr(span, "langfuse.observation.output")
    assert json.loads(input_attr["value"]["stringValue"]) == {"question": "q"}
    assert json.loads(output_attr["value"]["stringValue"]) == {"passed": True}


def test_build_experiment_root_span_tags_array_value():
    run = ExperimentRun(name="run0", dataset_id="ds-1")
    item = ExperimentItem(item_id="item-1")
    span = build_experiment_root_span(
        run,
        item,
        start=datetime(2025, 1, 1, tzinfo=timezone.utc),
        end=datetime(2025, 1, 1, tzinfo=timezone.utc),
        trace_name="gd-eval: q",
        tags=("gd-eval",),
    )
    tags_attr = _attr(span, "langfuse.trace.tags")
    assert tags_attr["value"] == {"arrayValue": {"values": [{"stringValue": "gd-eval"}]}}


def test_build_experiment_root_span_omits_tags_when_empty():
    run = ExperimentRun(name="run0", dataset_id="ds-1")
    item = ExperimentItem(item_id="item-1")
    span = build_experiment_root_span(
        run,
        item,
        start=datetime(2025, 1, 1, tzinfo=timezone.utc),
        end=datetime(2025, 1, 1, tzinfo=timezone.utc),
        trace_name="gd-eval: q",
    )
    assert _attr(span, "langfuse.trace.tags") is None


def test_build_experiment_root_span_clamps_end_before_start():
    start = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    end = datetime(2025, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
    run = ExperimentRun(name="run0", dataset_id="ds-1")
    item = ExperimentItem(item_id="item-1")
    span = build_experiment_root_span(run, item, start=start, end=end, trace_name="gd-eval: q")
    assert span.end == start


def test_build_experiment_root_span_omits_none_optional_attrs():
    run = ExperimentRun(name="run0", dataset_id="ds-1")
    item = ExperimentItem(item_id="item-1")
    span = build_experiment_root_span(
        run,
        item,
        start=datetime(2025, 1, 1, tzinfo=timezone.utc),
        end=datetime(2025, 1, 1, tzinfo=timezone.utc),
        trace_name="gd-eval: q",
    )
    assert _attr(span, "langfuse.session.id") is None
    assert _attr(span, "langfuse.version") is None
    assert _attr(span, "langfuse.environment") is None
    assert _attr(span, "langfuse.experiment.description") is None
    assert _attr(span, "langfuse.experiment.item.expected_output") is None


def test_build_experiment_root_span_full_wire_key_contract():
    run = ExperimentRun(
        name="run0",
        dataset_id="ds-1",
        metadata={"model_version": "gpt", "testing_framework": "tavern-e2e"},
    )
    item = ExperimentItem(item_id="item-1")
    span = build_experiment_root_span(
        run,
        item,
        start=datetime(2025, 1, 1, tzinfo=timezone.utc),
        end=datetime(2025, 1, 1, tzinfo=timezone.utc),
        trace_name="gd-eval: q",
        session_id="c1",
        version="gpt-5.2",
        environment="staging",
        observation_metadata={"gen_ai_trace_id": "abc", "conversation_id": "c1"},
    )
    keys = {a["key"] for a in span.attributes}
    assert "langfuse.session.id" in keys
    assert "langfuse.version" in keys
    assert "langfuse.environment" in keys
    assert "langfuse.observation.metadata.gen_ai_trace_id" in keys
    assert "langfuse.observation.metadata.conversation_id" in keys
    assert "langfuse.experiment.metadata.model_version" in keys
    assert "langfuse.experiment.metadata.testing_framework" in keys


def test_score_target_str_value_prefers_gen_ai_trace_id():
    target = ScoreTarget("g", "t", "s")
    assert target == "g"
    assert target.gen_ai_trace_id == "g"
    assert target.experiment_trace_id == "t"
    assert target.experiment_span_id == "s"


def test_score_target_str_value_falls_back_to_experiment_trace_id():
    target = ScoreTarget(None, "t", "s")
    assert str(target) == "t"


def test_score_target_destinations_order_and_skipping():
    target = ScoreTarget("g", "t", "s")
    assert target.destinations() == [("g", None), ("t", "s")]


def test_score_target_destinations_skips_missing_gen_ai():
    target = ScoreTarget(None, "t", "s")
    assert target.destinations() == [("t", "s")]


def test_score_target_destinations_empty_when_nothing_set():
    target = ScoreTarget()
    assert target.destinations() == []
    assert str(target) == ""
