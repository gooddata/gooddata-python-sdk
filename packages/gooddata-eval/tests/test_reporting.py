# (C) 2026 GoodData Corporation
import io
from datetime import datetime, timezone

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


def test_build_json_report_writes_started_at_as_utc_iso():
    report = _report()
    report.started_at = datetime(2026, 10, 14, 14, 30, 21, 412873, tzinfo=timezone.utc)
    assert build_json_report(report)["summary"]["started_at"] == "2026-10-14T14:30:21.412873+00:00"


def test_build_json_report_started_at_is_null_when_the_run_was_never_timed():
    assert build_json_report(_report())["summary"]["started_at"] is None


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


def test_json_runs_and_the_aggregate_average_use_the_runs_actually_taken():
    # Same divisor everywhere: the item's own average already used runs_total, but the JSON
    # `runs` field and the run-level average still reported the requested K.
    once = _item("conv", runs=5, runs_passed=1, passed=True, effective=1)
    once.latency_s = 10.0
    report = EvalReport(model="m", items=[once])

    data = build_json_report(report)

    assert data["items"]["conv"]["runs"] == 1
    assert report.total_runs == 1
    assert data["summary"]["avg_latency_s"] == 10.0


def test_the_report_counts_the_runs_the_judge_could_not_grade():
    item = _item("a", runs=3, runs_passed=2, passed=True)
    item.runs_ungraded = 1
    report = EvalReport(model="m", items=[item])

    data = build_json_report(report)
    out = _rendered(report)

    assert data["items"]["a"]["runs_ungraded"] == 1
    assert "2/3 runs passed; 1 run(s) ungraded" in out


def test_a_failed_item_says_when_a_criterion_went_ungraded():
    # `passed` is False with no False bool in the detail, so the generic "did not pass strict
    # checks" alone would hide why: a mandatory criterion the judge never assessed.
    item = _item("s", runs=1, runs_passed=0, passed=False)
    item.best_detail = {"include_0": True, "ungraded_criteria": 1}
    report = EvalReport(model="m", items=[item])

    out = _rendered(report)

    assert "did not pass strict checks; 1 criterion(s) ungraded" in out


def test_json_report_carries_failed_runs_beside_the_winning_detail():
    """`detail` keeps its exact meaning -- the winning run -- so every existing consumer of
    this report is unaffected; the failing attempts arrive alongside it rather than
    replacing it."""
    report = EvalReport(model="gpt-5.2")
    report.items.append(
        ItemReport(
            id="i1",
            dataset_name="d",
            test_kind="agentic_dashboard_summary",
            question="q",
            pass_at_k=True,
            runs=2,
            runs_passed=1,
            best_detail={"rubric_0": True},
            conversation_id="conv-2",
            failed_runs=[
                {
                    "run_index": 1,
                    "passed": False,
                    "error": None,
                    "detail": {"rubric_0": False},
                    "conversation_id": "conv-1",
                    "response_id": "resp-1",
                    "stream_ended": True,
                    "reasoning_steps": ["why it went wrong"],
                }
            ],
        )
    )

    item = build_json_report(report)["items"]["i1"]
    assert item["detail"] == {"rubric_0": True}
    assert item["conversation_id"] == "conv-2"
    assert [r["detail"] for r in item["failed_runs"]] == [{"rubric_0": False}]
    assert item["failed_runs"][0]["conversation_id"] == "conv-1"


def test_json_report_failed_runs_is_empty_for_a_clean_item():
    report = EvalReport(model="gpt-5.2")
    report.items.append(
        ItemReport(id="i1", dataset_name="d", test_kind="visualization", question="q", pass_at_k=True, runs=2)
    )
    assert build_json_report(report)["items"]["i1"]["failed_runs"] == []


def _mixed_report(model: str = "gpt-5.2", *, single: list[float] | None = None) -> EvalReport:
    """Two single-shot items (one trace each) and one multi-turn conversation (three turns)."""
    single = single if single is not None else [1.0, 3.0]
    items = [
        ItemReport(
            id=f"s{n}",
            dataset_name="d",
            test_kind="visualization",
            question=f"q{n}",
            pass_at_k=n == 1,
            runs=1,
            latency_s=latency + 0.5,
            trace_latencies_s=[latency],
            run_latencies_s=[latency + 0.5],
        )
        for n, latency in enumerate(single, start=1)
    ]
    items.append(
        ItemReport(
            id="m1",
            dataset_name="d",
            test_kind="agentic_metric_skill",
            question="converse",
            pass_at_k=True,
            runs=1,
            latency_s=30.0,
            trace_latencies_s=[2.0, 4.0, 6.0],
            run_latencies_s=[30.0],
        )
    )
    return EvalReport(model=model, workspace_id="ws1", items=items)


def test_json_report_splits_pass_counts_and_latency_by_mode():
    summary = build_multi_model_report([_mixed_report()])["runs"]["gpt-5.2"]["summary"]

    single = summary["by_mode"]["single_shot"]
    assert (single["total"], single["passed"]) == (2, 1)
    # Two single-shot items, one trace each: the main per-trace figure.
    assert single["traces_s"] == {
        "n": 2,
        "mean": 2.0,
        "trimmed_mean": None,
        "min": 1.0,
        "p50": 2.0,
        "p70": 2.4,
        "p90": 2.8,
        "p99": 2.98,
        "max": 3.0,
    }
    assert "runs_s" not in single

    multi = summary["by_mode"]["multi_turn"]
    assert (multi["total"], multi["passed"]) == (1, 1)
    # Three turns of one conversation are three traces, and one full run.
    assert multi["traces_s"]["n"] == 3 and multi["traces_s"]["p50"] == 4.0
    assert multi["runs_s"]["n"] == 1 and multi["runs_s"]["max"] == 30.0


def test_json_comparison_entry_repeats_the_mode_split():
    # The HTML reads the comparison entry and falls back to the summary, so both carry it.
    data = build_multi_model_report([_mixed_report()])

    assert data["comparison"]["gpt-5.2"]["by_mode"] == data["runs"]["gpt-5.2"]["summary"]["by_mode"]


def test_json_items_state_their_mode_and_trace_latencies():
    items = build_multi_model_report([_mixed_report()])["runs"]["gpt-5.2"]["items"]

    assert items["s1"]["mode"] == "single_shot"
    assert items["s1"]["trace_latencies_s"] == [1.0]
    assert items["m1"]["mode"] == "multi_turn"
    assert items["m1"]["trace_latencies_s"] == [2.0, 4.0, 6.0]
    assert items["m1"]["run_latencies_s"] == [30.0]


def test_json_report_states_no_latency_distribution_when_nothing_was_timed():
    # null, not zeroes: a P99 of 0s would claim a measurement that never happened.
    by_mode = build_multi_model_report([_report()])["runs"]["gpt-5.2"]["summary"]["by_mode"]

    assert by_mode["single_shot"]["traces_s"] is None
    assert by_mode["multi_turn"] == {"total": 0, "passed": 0, "traces_s": None, "runs_s": None}


def test_json_report_leaves_the_existing_latency_figures_alone():
    summary = build_json_report(_mixed_report())["summary"]

    assert summary["latency_s"] == 1.5 + 3.5 + 30.0
    assert summary["avg_latency_s"] == round(35.0 / 3, 3)


def test_console_prints_each_modes_latency_beneath_the_summary():
    text = render_console(_mixed_report())

    assert "By mode: single-shot 1/2 passed · multi-turn 1/1 passed" in text
    assert "Latency, single-shot per trace (n=2): P50 2.00s · P70 2.40s · P90 2.80s · P99 2.98s" in text
    assert "Latency, multi-turn per trace (n=3): P50 4.00s" in text
    assert "Latency, multi-turn per full run (n=1): P50 30.00s" in text
    assert text.index("Summary:") < text.index("By mode:") < text.index("per trace (n=2)")


def test_console_leaves_out_a_mode_with_no_items_and_a_distribution_with_no_samples():
    only_single = EvalReport(model="m", items=[_mixed_report().items[0]])

    text = render_console(only_single)

    assert "single-shot 0/1 passed" not in text and "single-shot 1/1 passed" in text
    assert "multi-turn" not in text


def test_console_omits_the_mode_lines_when_nothing_was_evaluated():
    assert "By mode" not in render_console(EvalReport(model="m"))


def test_comparison_table_sets_single_shot_trace_median_and_tail_side_by_side():
    reports = [
        _mixed_report("gpt-5.2", single=[10.0, 20.0]),
        _mixed_report("gpt-4o", single=[8.0, 12.0]),
    ]

    text = render_comparison(reports, console=Console(record=True, width=200))

    for column in ("Trace P50", "Trace P90", "Trace P99"):
        assert column in text
    assert "15.00s" in text  # gpt-5.2 median of its single-shot traces 10 and 20
    assert "19.00s" in text  # gpt-5.2 P90
    assert "10.00s" in text  # gpt-4o median of 8 and 12
    assert "single-shot chat-turn response time" in text
