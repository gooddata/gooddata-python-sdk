# (C) 2026 GoodData Corporation
import json
import re

import orjson
import pytest
from gooddata_eval.cli.main import main
from gooddata_eval.core.reporting.html_report import build_html, load_report_files


def _doc(model: str, passed: bool) -> dict:
    return {
        "models": [model],
        "runs": {
            model: {
                "model": model,
                "workspace_id": "ws1",
                "summary": {"total": 1, "passed": int(passed), "failed": int(not passed), "avg_latency_s": 2.5},
                "items": {
                    "item-1": {
                        "test_kind": "visualization",
                        "question": "How many orders?",
                        "pass_at_k": passed,
                        "conversation_id": "conv-secret",
                        "response_id": "resp-secret",
                        "reasoning": ["**Thinking**\n\ninternal thoughts"],
                        "detail": {
                            "metrics_correct": passed,
                            "latency_breakdown": [
                                {"seq": 0, "kind": "tool", "name": "search", "index": 0, "duration_s": 1.0}
                            ],
                            "turns": 2,
                            "transcript": [
                                {"turn": 1, "role": "user", "text": "How many orders?"},
                                {"turn": 1, "role": "assistant", "text": "Which order status?"},
                                {"turn": 2, "role": "simulated_user", "text": "primed with the expected answer"},
                            ],
                        },
                    }
                },
            }
        },
        "comparison": {model: {"passed": int(passed), "total": 1, "pass_rate": float(passed)}},
    }


def _embedded(html: str) -> dict:
    blob = re.search(r'<script id="data" type="application/json">(.*?)</script>', html, re.S).group(1)
    return json.loads(blob)


def test_merges_files_into_one_run_per_source(tmp_path):
    for name, passed in (("run-a", True), ("run-b", False)):
        (tmp_path / f"{name}.json").write_bytes(orjson.dumps(_doc("gpt-5", passed)))

    doc = load_report_files([tmp_path / "run-a.json", tmp_path / "run-b.json"])

    # Same model in both files must stay two columns, not overwrite each other.
    assert sorted(doc["runs"]) == ["run-a · gpt-5", "run-b · gpt-5"]
    assert sorted(doc["comparison"]) == ["run-a · gpt-5", "run-b · gpt-5"]


def test_legacy_single_run_file_is_accepted(tmp_path):
    legacy = _doc("gpt-5", True)["runs"]["gpt-5"]
    (tmp_path / "old.json").write_bytes(orjson.dumps(legacy))

    assert list(load_report_files([tmp_path / "old.json"])["runs"]) == ["gpt-5"]


def test_html_embeds_parseable_data_and_no_external_refs():
    html = build_html(_doc("gpt-5", False))

    data = _embedded(html)
    assert data["runs"]["gpt-5"]["items"]["item-1"]["conversation_id"] == "conv-secret"
    assert not re.search(r'(src|href)="(?!#)', html), "report must be self-contained"


def test_redact_drops_ids_reasoning_and_model_name():
    html = build_html(_doc("gpt-5", False), redact=True)

    assert "conv-secret" not in html
    assert "resp-secret" not in html
    assert "internal thoughts" not in html
    assert "gpt-5" not in html
    data = _embedded(html)
    assert list(data["runs"]) == ["Model A"]
    # The evaluation itself survives redaction -- only identity goes.
    assert data["runs"]["Model A"]["items"]["item-1"]["question"] == "How many orders?"
    assert data["runs"]["Model A"]["items"]["item-1"]["detail"]["latency_breakdown"]


def test_redact_drops_the_transcript_but_keeps_the_turn_count():
    html = build_html(_doc("gpt-5", False), redact=True)

    # The simulated user is primed with the expected output, so the exchange discloses how
    # we score. "It took 2 turns" is still a fair thing to show a customer.
    assert "primed with the expected answer" not in html
    detail = _embedded(html)["runs"]["Model A"]["items"]["item-1"]["detail"]
    assert "transcript" not in detail
    assert detail["turns"] == 2


def test_closing_script_tag_in_data_cannot_break_out():
    doc = _doc("gpt-5", False)
    doc["runs"]["gpt-5"]["items"]["item-1"]["question"] = "</script><script>alert(1)</script>"

    html = build_html(doc)

    # The blob must survive to the end of the payload -- if a "</script>" inside the data
    # had terminated the host tag early, this capture would be truncated and not parse.
    assert _embedded(html)["runs"]["gpt-5"]["items"]["item-1"]["question"] == "</script><script>alert(1)</script>"


def test_cli_report_command_writes_html(tmp_path):
    src = tmp_path / "results.json"
    src.write_bytes(orjson.dumps(_doc("gpt-5", True)))
    out = tmp_path / "report.html"

    assert main(["report", str(src), "-o", str(out), "--title", "MSXi eval"]) == 0
    assert "MSXi eval" in out.read_text()


@pytest.mark.parametrize("redact", [False, True])
def test_cli_report_command_needs_no_credentials(tmp_path, monkeypatch, redact):
    monkeypatch.delenv("GOODDATA_TOKEN", raising=False)
    monkeypatch.delenv("GOODDATA_HOST", raising=False)
    src = tmp_path / "results.json"
    src.write_bytes(orjson.dumps(_doc("gpt-5", True)))
    out = tmp_path / "report.html"

    argv = ["report", str(src), "-o", str(out)] + (["--redact"] if redact else [])
    assert main(argv) == 0
    assert out.exists()
