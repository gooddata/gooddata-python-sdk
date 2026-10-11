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
                        "failed_runs": [
                            {
                                "run_index": 2,
                                "passed": False,
                                "error": None,
                                "conversation_id": "run-conv-secret",
                                "response_id": "run-resp-secret",
                                "reasoning_step_count": 1,
                                "reasoning_steps": ["**Thinking**\n\nper-run internal thoughts"],
                                "tool_call_count": 1,
                                "tool_names": ["search_objects"],
                                "latency_s": 3.5,
                                "detail": {
                                    "metrics_correct": False,
                                    "turns": 1,
                                    "transcript": [
                                        {"turn": 1, "role": "simulated_user", "text": "per-run primed answer"}
                                    ],
                                    "tool_calls": [{"name": "search_objects", "result": "row data"}],
                                },
                            }
                        ],
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


def test_redact_reaches_inside_failed_runs():
    """Per-run records carry their own ids and their own raw reasoning.

    Redacting only the item's top level left the identical content one level down: the
    top-level `reasoning` was dropped while the same text survived verbatim in
    `failed_runs`, in a report labelled customer-safe.
    """
    html = build_html(_doc("gpt-5", False), redact=True)

    assert "run-conv-secret" not in html
    assert "run-resp-secret" not in html
    assert "per-run internal thoughts" not in html

    run = _embedded(html)["runs"]["Model A"]["items"]["item-1"]["failed_runs"][0]
    assert "conversation_id" not in run
    assert "response_id" not in run
    assert "reasoning_steps" not in run
    # What the run actually did survives -- the same line the top level draws.
    assert run["run_index"] == 2
    assert run["passed"] is False
    assert run["reasoning_step_count"] == 1
    assert run["tool_names"] == ["search_objects"]
    assert run["latency_s"] == 3.5


def test_redact_reaches_inside_a_failed_run_s_own_detail():
    """A per-run `detail` carries the same transcript and tool payloads as the top one."""
    html = build_html(_doc("gpt-5", False), redact=True)

    assert "per-run primed answer" not in html
    assert "row data" not in html

    detail = _embedded(html)["runs"]["Model A"]["items"]["item-1"]["failed_runs"][0]["detail"]
    assert "transcript" not in detail
    assert "tool_calls" not in detail
    assert detail["turns"] == 1
    assert detail["metrics_correct"] is False


def test_failed_runs_survive_an_unredacted_report():
    """The field is diagnostic data; only `--redact` strips it."""
    run = _embedded(build_html(_doc("gpt-5", False)))["runs"]["gpt-5"]["items"]["item-1"]["failed_runs"][0]

    assert run["conversation_id"] == "run-conv-secret"
    assert run["reasoning_steps"] == ["**Thinking**\n\nper-run internal thoughts"]


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


_TRACES = {"n": 4, "mean": 2.5, "min": 1.0, "p50": 2.5, "p70": 3.1, "p90": 3.7, "p99": 3.97, "max": 4.0}
_RUNS = {"n": 2, "mean": 20.0, "min": 10.0, "p50": 20.0, "p70": 24.0, "p90": 28.0, "p99": 29.8, "max": 30.0}
_BY_MODE = {
    "single_shot": {"total": 3, "passed": 2, "traces_s": _TRACES},
    "multi_turn": {"total": 1, "passed": 1, "traces_s": _TRACES, "runs_s": _RUNS},
}


def _doc_with_modes(model: str) -> dict:
    doc = _doc(model, True)
    doc["runs"][model]["summary"]["by_mode"] = _BY_MODE
    doc["runs"][model]["items"]["item-1"].update({"mode": "single_shot", "trace_latencies_s": [1.0, 2.0]})
    doc["comparison"][model]["by_mode"] = _BY_MODE
    return doc


def test_html_carries_the_mode_split_it_was_built_from():
    data = _embedded(build_html(_doc_with_modes("gpt-5")))

    assert data["runs"]["gpt-5"]["summary"]["by_mode"] == _BY_MODE
    assert data["comparison"]["gpt-5"]["by_mode"] == _BY_MODE
    item = data["runs"]["gpt-5"]["items"]["item-1"]
    assert (item["mode"], item["trace_latencies_s"]) == ("single_shot", [1.0, 2.0])


def test_redact_keeps_the_mode_split_and_latency():
    """Latency and the section an item falls in are facts about the run, not about our
    infrastructure -- the same line redaction already draws for per-item latency."""
    data = _embedded(build_html(_doc_with_modes("gpt-5"), redact=True))

    assert data["runs"]["Model A"]["summary"]["by_mode"] == _BY_MODE
    assert data["comparison"]["Model A"]["by_mode"] == _BY_MODE
    assert data["runs"]["Model A"]["items"]["item-1"]["trace_latencies_s"] == [1.0, 2.0]


def test_the_page_has_single_shot_and_multi_turn_sections_read_from_the_report():
    """The report is a view over the JSON: the page names the sections and populations and reads
    the figures from `by_mode`. It holds no percentile arithmetic that could disagree with the
    console or the JSON."""
    html = build_html(_doc_with_modes("gpt-5"))

    assert "by_mode" in html
    for text in ("Single-shot · latency per trace", "Multi-turn · conversations", "Per trace", "Per full run"):
        assert text in html
    for label in ("P50", "P70", "P90", "P99"):
        assert label in html
    section = html.split("// ---------- latency by mode")[1].split("function cmp(label)")[0]
    assert "sort(" not in section


def test_html_uses_the_goodata_tokens_and_loads_no_web_font():
    html = build_html(_doc("gpt-5", True))

    for token in ("#14b2e2", "#dafe85", "#464e56", "#dde4eb", "#f5f8fa"):
        assert token in html, f"design token {token} missing"
    assert '"Avenir Next", Avenir' in html
    # Self-contained: a web font, import or remote stylesheet would break file:// and offline use.
    assert "@font-face" not in html
    assert "@import" not in html
    assert "url(" not in html


def test_building_the_html_does_not_invent_a_mode_split_for_an_older_report():
    """Files written before gd-eval split latency by mode carry no `by_mode`. The page says so;
    nothing here backfills a figure the run never measured."""
    data = _embedded(build_html(_doc("gpt-5", True)))

    assert "by_mode" not in data["runs"]["gpt-5"]["summary"]
    assert "by_mode" not in data["comparison"]["gpt-5"]
