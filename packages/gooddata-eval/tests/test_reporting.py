# (C) 2026 GoodData Corporation
import orjson
from gooddata_eval.core.reporting.console import render_comparison, render_console
from gooddata_eval.core.reporting.json_report import (
    build_json_report,
    build_multi_model_report,
    write_json_report,
    write_multi_model_report,
)
from gooddata_eval.core.runner import EvalReport, ItemReport


def _report() -> EvalReport:
    return EvalReport(
        model="gpt-5.2",
        workspace_id="ws1",
        items=[
            ItemReport(
                id="i1",
                dataset_name="d",
                test_kind="visualization",
                question="q1",
                pass_at_k=True,
                runs=2,
                latency_s=2.5,
            ),
            ItemReport(
                id="i2",
                dataset_name="d",
                test_kind="visualization",
                question="q2",
                pass_at_k=False,
                runs=2,
                latency_s=3.0,
            ),
            ItemReport(id="i3", dataset_name="d", test_kind="metric_skill", question="q3", skipped=True),
        ],
    )


def test_build_json_report_keyed_by_item_id():
    data = build_json_report(_report())
    assert data["model"] == "gpt-5.2"
    assert data["summary"]["passed"] == 1
    assert data["summary"]["skipped"] == 1
    assert data["summary"]["latency_s"] == 5.5
    assert data["summary"]["avg_latency_s"] == 1.375
    assert data["items"]["i1"]["pass_at_k"] is True
    assert data["items"]["i1"]["latency_s"] == 2.5
    assert data["items"]["i1"]["avg_latency_s"] == 1.25


def test_write_json_report_creates_file(tmp_path):
    path = tmp_path / "out.json"
    write_json_report(_report(), path)
    loaded = orjson.loads(path.read_bytes())
    assert loaded["runs"]["gpt-5.2"]["items"]["i2"]["pass_at_k"] is False


def test_render_console_returns_summary_text():
    text = render_console(_report())
    assert "gpt-5.2" in text
    assert "1/3" in text
    assert "2.50s" in text  # i1 total latency
    assert "1.25s" in text  # i1 avg/run latency


def _two_reports():
    return [
        EvalReport(
            model="gpt-5.2",
            workspace_id="ws",
            items=[
                ItemReport(
                    id="i1",
                    dataset_name="d",
                    test_kind="visualization",
                    question="q1",
                    pass_at_k=True,
                    runs=1,
                    latency_s=10.0,
                    best_detail={"metrics_correct": True},
                ),
                ItemReport(
                    id="i2",
                    dataset_name="d",
                    test_kind="visualization",
                    question="q2",
                    pass_at_k=False,
                    runs=1,
                    latency_s=20.0,
                    best_detail={"metrics_correct": False},
                ),
            ],
        ),
        EvalReport(
            model="gpt-4o",
            workspace_id="ws",
            items=[
                ItemReport(
                    id="i1",
                    dataset_name="d",
                    test_kind="visualization",
                    question="q1",
                    pass_at_k=True,
                    runs=1,
                    latency_s=8.0,
                    best_detail={"metrics_correct": True},
                ),
                ItemReport(
                    id="i2",
                    dataset_name="d",
                    test_kind="visualization",
                    question="q2",
                    pass_at_k=True,
                    runs=1,
                    latency_s=12.0,
                    best_detail={"metrics_correct": True},
                ),
            ],
        ),
    ]


def test_build_multi_model_report_structure():
    data = build_multi_model_report(_two_reports())
    assert data["models"] == ["gpt-5.2", "gpt-4o"]
    assert "gpt-5.2" in data["runs"]
    assert "gpt-4o" in data["runs"]
    assert data["runs"]["gpt-5.2"]["model"] == "gpt-5.2"
    assert "comparison" in data
    assert data["comparison"]["gpt-5.2"]["passed"] == 1
    assert data["comparison"]["gpt-4o"]["passed"] == 2


def test_build_multi_model_report_comparison_keys():
    data = build_multi_model_report(_two_reports())
    cmp = data["comparison"]["gpt-4o"]
    assert cmp["total"] == 2
    assert cmp["pass_rate"] == 1.0
    assert "avg_quality_score" in cmp
    assert "avg_latency_s" in cmp
    assert "total_latency_s" in cmp


def test_write_multi_model_report_creates_file(tmp_path):
    path = tmp_path / "out.json"
    write_multi_model_report(_two_reports(), path)
    loaded = orjson.loads(path.read_bytes())
    assert loaded["models"] == ["gpt-5.2", "gpt-4o"]
    assert "comparison" in loaded


def test_render_comparison_shows_both_models_and_winner():
    text = render_comparison(_two_reports())
    assert "gpt-5.2" in text
    assert "gpt-4o" in text
    assert "Winner" in text
    # gpt-4o passed 2/2, gpt-5.2 passed 1/2 — gpt-4o wins
    assert "gpt-4o" in text.split("Winner")[1]


def test_render_comparison_single_report_returns_empty():
    assert render_comparison([EvalReport(model="gpt-5.2", workspace_id="ws")]) == ""


def test_build_multi_model_report_no_key_collision_same_model_different_providers():
    """Two runs with the same model_id but different providers must both survive in JSON."""
    r1 = EvalReport(
        model="claude-opus",
        provider_name="DirectAnthropic",
        workspace_id="ws",
        items=[
            ItemReport(id="i1", dataset_name="d", test_kind="visualization", question="q", pass_at_k=True, runs=1),
        ],
    )
    r2 = EvalReport(
        model="claude-opus",
        provider_name="HN_Anthropic",
        workspace_id="ws",
        items=[
            ItemReport(id="i1", dataset_name="d", test_kind="visualization", question="q", pass_at_k=False, runs=1),
        ],
    )
    data = build_multi_model_report([r1, r2])
    assert len(data["runs"]) == 2, "both runs must be present — no silent overwrite"
    assert len(data["comparison"]) == 2
    assert "DirectAnthropic/claude-opus" in data["runs"]
    assert "HN_Anthropic/claude-opus" in data["runs"]
    assert data["runs"]["DirectAnthropic/claude-opus"]["summary"]["passed"] == 1
    assert data["runs"]["HN_Anthropic/claude-opus"]["summary"]["passed"] == 0
