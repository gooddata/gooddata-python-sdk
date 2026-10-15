# (C) 2026 GoodData Corporation
import json
import re

import orjson
import pytest
from gooddata_eval.cli.main import main
from gooddata_eval.core.reporting.html_report import _redact, build_html, load_report_files


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


def _multi_date_doc():
    """What `merge_docs` produces for three models evaluated on two dates."""
    return {
        "runs": {
            f"{date} · {model}": {"model": model, "workspace_id": "ws", "items": {}}
            for date in ("2026-09-22", "2026-10-01")
            for model in ("gpt-5.2", "gpt-5.5", "gpt-5.6-luna")
        },
        "comparison": {
            f"{date} · {model}": {"provider_name": "openai", "passed": 1, "total": 2}
            for date in ("2026-09-22", "2026-10-01")
            for model in ("gpt-5.2", "gpt-5.5", "gpt-5.6-luna")
        },
    }


def test_redact_gives_one_model_one_alias_across_dates():
    """Three models over two dates is three aliases, not six.

    Numbering the run keys made the same model a different alias on each date, so
    nothing told the reader that Model D was Model A a week later -- which is the
    only question a multi-date report exists to answer.
    """
    redacted = _redact(_multi_date_doc())

    assert set(redacted["runs"]) == {
        "2026-09-22 · Model A",
        "2026-09-22 · Model B",
        "2026-09-22 · Model C",
        "2026-10-01 · Model A",
        "2026-10-01 · Model B",
        "2026-10-01 · Model C",
    }
    # The same alias on both dates must denote the same model.
    assert redacted["runs"]["2026-09-22 · Model A"]["model"] == "Model A"
    assert redacted["runs"]["2026-10-01 · Model A"]["model"] == "Model A"
    assert set(redacted["comparison"]) == set(redacted["runs"])
    assert all(e["provider_name"] == "" for e in redacted["comparison"].values())


def test_redact_still_hides_every_real_model_name():
    blob = json.dumps(_redact(_multi_date_doc()))
    for model in ("gpt-5.2", "gpt-5.5", "gpt-5.6-luna", "openai"):
        assert model not in blob


def test_redact_alias_survives_past_twenty_six_models():
    """chr(65 + n) walked off the alphabet: the 27th run was `Model [`."""
    doc = {
        "runs": {f"m{i}": {"model": f"model-{i}", "items": {}} for i in range(30)},
        "comparison": {},
    }
    aliases = [a.removeprefix("Model ") for a in _redact(doc)["runs"]]

    assert len(set(aliases)) == 30
    assert all(a.isalpha() for a in aliases), [a for a in aliases if not a.isalpha()]
    assert aliases[25:28] == ["Z", "AA", "AB"]


def test_redact_without_a_date_prefix_is_just_the_alias():
    """A single-source report keys runs by the bare model name."""
    doc = {"runs": {"gpt-5.2": {"model": "gpt-5.2", "items": {}}}, "comparison": {}}
    assert list(_redact(doc)["runs"]) == ["Model A"]


def test_redact_leaves_no_model_name_anywhere_in_a_run_key():
    """`merge_docs` prefixes the source filename onto the label, and a filename can
    name a *different* model than the run it labels. Substituting only the run's own
    model left the other one in plain sight in a redacted report."""
    doc = {
        "runs": {
            "gpt-5.5-baseline.json · gpt-5.2": {"model": "gpt-5.2", "items": {}},
            "gpt-5.5-baseline.json · gpt-5.5": {"model": "gpt-5.5", "items": {}},
        },
        "comparison": {},
    }
    redacted = _redact(doc)

    blob = json.dumps(redacted)
    for model in ("gpt-5.2", "gpt-5.5"):
        assert model not in blob, f"{model} survived redaction: {list(redacted['runs'])}"
    # Both rows agree on the redacted filename, so the two columns stay comparable.
    assert set(redacted["runs"]) == {
        "Model B-baseline.json · Model A",
        "Model B-baseline.json · Model B",
    }


def test_redact_does_not_let_a_short_model_name_corrupt_a_longer_one():
    """ "gpt-5" is a prefix of "gpt-5.2"; replacing it first would leave "Model A.2"."""
    doc = {
        "runs": {
            "2026-10-01 · gpt-5": {"model": "gpt-5", "items": {}},
            "2026-10-01 · gpt-5.2": {"model": "gpt-5.2", "items": {}},
        },
        "comparison": {},
    }
    redacted = _redact(doc)

    assert set(redacted["runs"]) == {"2026-10-01 · Model A", "2026-10-01 · Model B"}
    assert "gpt-5" not in json.dumps(redacted)
