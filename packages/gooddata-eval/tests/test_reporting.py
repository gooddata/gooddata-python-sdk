# (C) 2026 GoodData Corporation
import orjson
from gooddata_eval.core.reporting.console import render_console
from gooddata_eval.core.reporting.json_report import build_json_report, write_json_report
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
    assert loaded["items"]["i2"]["pass_at_k"] is False


def test_render_console_returns_summary_text():
    text = render_console(_report())
    assert "gpt-5.2" in text
    assert "1/3" in text
    assert "2.50s" in text  # i1 total latency
    assert "1.25s" in text  # i1 avg/run latency
