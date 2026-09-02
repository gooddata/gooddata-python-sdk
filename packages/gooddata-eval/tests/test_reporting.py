# (C) 2026 GoodData Corporation
import io

import orjson
from gooddata_eval.core.reporting.console import render_comparison, render_console
from gooddata_eval.core.reporting.json_report import (
    build_json_report,
    build_multi_model_report,
    write_json_report,
    write_multi_model_report,
)
from gooddata_eval.core.runner import EvalReport, ItemReport
from rich.console import Console


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
                reasoning_steps=["step one", "step two"],
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
    assert data["items"]["i1"]["reasoning"] == ["step one", "step two"]
    assert data["items"]["i2"]["reasoning"] == []


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


def _timed_report() -> EvalReport:
    return EvalReport(
        model="gpt-5.2",
        workspace_id="ws1",
        items=[
            ItemReport(
                id="i1",
                dataset_name="d",
                test_kind="agentic_general_question",
                question="q1",
                pass_at_k=True,
                runs=1,
                latency_s=6.0,
                agent_latency_s=4.0,
                judge_latency_s=2.0,
                langfuse_latency_s=31.5,
            )
        ],
    )


def test_json_report_breaks_an_item_down_by_phase():
    # Without this the report has one latency number per item and no way to tell a slow
    # agent from a slow judge -- the question the whole exercise exists to answer.
    item = build_json_report(_timed_report())["items"]["i1"]

    assert item["latency_breakdown_s"] == {
        "agent_s": 4.0,
        "judge_s": 2.0,
        "simulated_user_s": 0.0,
        "langfuse_s": 31.5,
    }


def test_json_report_keeps_langfuse_time_out_of_the_item_latency():
    # langfuse_s is reported *beside* latency_s, never folded into it: trace linking runs
    # off the critical path, so adding it back would re-create the 40s items in the report
    # even though the run no longer waits for them.
    item = build_json_report(_timed_report())["items"]["i1"]

    assert item["latency_s"] == 6.0
    assert item["latency_breakdown_s"]["langfuse_s"] == 31.5


def test_json_report_still_has_every_key_it_had_before():
    # Additive-only: the breakdown is a new key, not a reshaping of the existing report,
    # so anything already parsing these files keeps working.
    item = build_json_report(_report())["items"]["i1"]

    assert {
        "dataset_name",
        "test_kind",
        "question",
        "pass_at_k",
        "skipped",
        "error",
        "runs",
        "latency_s",
        "avg_latency_s",
        "best_run_latency_s",
        "detail",
        "conversation_id",
        "response_id",
        "reasoning",
    } <= set(item)


def test_console_summary_does_not_call_the_item_total_agent_time():
    # report.latency_s is the sum of each item's critical path -- agent AND judge AND
    # simulated user. Now that agentic runs set wall_clock_s, this branch fires for them
    # for the first time, and now that agent_latency_s exists as a real, different number,
    # labelling the total "agent time" states something false.
    report = _timed_report()
    report.wall_clock_s = 40.0  # >1s from latency_s, so the two-number form is used

    out = render_console(report, console=Console(record=True, width=200))

    assert "40.00s wall-clock" in out
    assert "agent time" not in out


# --- a pass@K that was not unanimous must say so (4/5 used to print as a clean PASS) ---


def _rendered(report: EvalReport) -> str:
    buf = io.StringIO()
    render_console(report, console=Console(file=buf, width=200, no_color=True))
    return buf.getvalue()


def _item(item_id: str, *, runs: int, runs_passed: int, passed: bool, effective: int | None = None) -> ItemReport:
    r = ItemReport(id=item_id, dataset_name="d", test_kind="agentic_general_question", question="q")
    r.pass_at_k = passed
    r.runs = runs
    r.runs_passed = runs_passed
    r.runs_effective = effective
    r.latency_s = 1.0
    r.best_detail = {"judge_passed": passed}
    return r


def test_console_reports_how_many_runs_passed_when_it_was_not_unanimous():
    """quality_score reads best_detail -- the winning run alone -- so a 1/5 item and a 5/5
    item printed identically: PASS, 100%, empty Notes. The count was already computed by
    every agentic kind and then dropped on the floor.
    """
    report = EvalReport(model="m")
    report.items = [
        _item("solid", runs=5, runs_passed=5, passed=True),
        _item("flaky", runs=5, runs_passed=4, passed=True),
        _item("coinflip", runs=5, runs_passed=1, passed=True),
    ]

    text = _rendered(report)

    assert "4/5 runs passed" in text
    assert "1/5 runs passed" in text
    # A unanimous pass stays uncluttered -- the note is a warning, not decoration.
    solid_row = next(line for line in text.splitlines() if "solid" in line)
    assert "runs passed" not in solid_row


def test_console_summary_separates_pass_at_k_from_unanimity():
    report = EvalReport(model="m")
    report.items = [
        _item("a", runs=3, runs_passed=3, passed=True),
        _item("b", runs=3, runs_passed=1, passed=True),
    ]

    assert "2/2 passed, 1 on every run" in _rendered(report)


def test_console_summary_stays_quiet_when_every_pass_was_unanimous():
    report = EvalReport(model="m")
    report.items = [_item("a", runs=3, runs_passed=3, passed=True)]

    text = _rendered(report)
    assert "1/1 passed (" in text
    assert "on every run" not in text


def test_json_report_carries_runs_passed_and_unanimity():
    report = EvalReport(model="m")
    report.items = [
        _item("solid", runs=5, runs_passed=5, passed=True),
        _item("flaky", runs=5, runs_passed=4, passed=True),
    ]

    run = build_json_report(report)

    assert run["summary"]["passed"] == 2
    assert run["summary"]["passed_all_runs"] == 1
    items = run["items"]
    by_id = items if isinstance(items, dict) else {i["id"]: i for i in items}
    assert (by_id["solid"]["runs_passed"], by_id["solid"]["pass_power_k"]) == (5, True)
    assert (by_id["flaky"]["runs_passed"], by_id["flaky"]["pass_power_k"]) == (4, False)


def test_a_kind_that_runs_once_is_not_reported_as_k_runs():
    # agentic_conversation takes no k and drives its fixture once whatever --runs says.
    # Trusting K there reported four runs that never happened, and divided the latency by 5.
    report = EvalReport(model="m")
    report.items = [_item("conv", runs=5, runs_passed=1, passed=True, effective=1)]

    text = _rendered(report)
    conv_row = next(line for line in text.splitlines() if "conv" in line and "PASS" in line)
    assert " 1 " in conv_row, f"the Runs column should show the 1 run it made: {conv_row}"
    assert "runs passed" not in conv_row, "1 of 1 is unanimous"


def test_an_errored_item_is_not_reported_as_passing_every_run():
    """An item can error after earlier runs passed, leaving runs_passed == runs_total.

    That is not unanimity -- the last run produced no verdict at all -- so pass^K must not
    claim it, and passed_all_runs must not count it.
    """
    errored = _item("boom", runs=2, runs_passed=2, passed=False, effective=2)
    errored.error = "judge returned no readable verdict for any of the 2 run(s)"

    assert errored.pass_power_k is False

    report = EvalReport(model="m")
    report.items = [errored]
    assert build_json_report(report)["summary"]["passed_all_runs"] == 0


def test_an_errored_item_is_counted_as_errored_not_as_a_failure():
    # `total - passed - skipped` counted an errored item as both. A judge fault is
    # documented to report as an error instead of K failures, so `failed` must exclude it.
    errored = _item("boom", runs=2, runs_passed=0, passed=False, effective=2)
    errored.error = "judge returned no readable verdict"
    genuine = _item("nope", runs=2, runs_passed=0, passed=False, effective=2)
    report = EvalReport(model="m")
    report.items = [errored, genuine]

    summary = build_json_report(report)["summary"]
    assert (summary["failed"], summary["errored"]) == (1, 1)


def test_avg_per_run_divides_by_the_runs_actually_taken():
    # The Runs column reports runs_effective, so an average over the requested K reported
    # a per-run latency for runs that never happened.
    once = _item("conv", runs=5, runs_passed=1, passed=True, effective=1)
    once.latency_s = 10.0

    assert once.runs_total == 1
    assert once.avg_latency_s == 10.0
