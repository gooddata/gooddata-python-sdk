# (C) 2026 GoodData Corporation
"""The K gate: which of pass@K / pass^K decides an item, and what reaches Langfuse."""

import contextlib
import importlib
import inspect
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.cli.agentic_runner import run_agentic_items
from gooddata_eval.cli.main import _reject_power_gate_on_ungated_items
from gooddata_eval.core.agentic._gate import (
    DEFAULT_GATE,
    gate_failure_note,
    gate_label,
    gate_passed,
    log_gate_scores,
    stamp_gate_metadata,
)
from gooddata_eval.core.agentic.alert_skill import AlertSkillAssertionError
from gooddata_eval.core.agentic.general_question import (
    GeneralQuestionAssertionError,
    evaluate_agentic_general_question,
)
from gooddata_eval.core.config import RunConfig, normalize_gate
from gooddata_eval.core.models import AgenticEvalOutcome, ChatResult, DatasetItem
from gooddata_eval.core.reporting.console import render_console
from gooddata_eval.core.reporting.json_report import build_json_report
from gooddata_eval.core.runner import EvalReport, ItemReport


def test_the_default_gate_is_the_historic_pass_at_k():
    assert DEFAULT_GATE == "any"
    assert gate_passed(None, pass_at_k=True, pass_power_k=False) is True


@pytest.mark.parametrize("value", ["power", "POWER", " Power "])
def test_gate_is_normalized_from_any_casing(value):
    assert normalize_gate(value) == "power"


@pytest.mark.parametrize("value", [None, "", "   "])
def test_absent_gate_means_the_default(value):
    assert normalize_gate(value) == DEFAULT_GATE


@pytest.mark.parametrize("value", ["all", "majority", "pass^k", "1"])
def test_an_unknown_gate_is_rejected_rather_than_silently_lax(value):
    """Falling through to pass@K would pick the laxer gate and look deliberate."""
    with pytest.raises(ValueError, match="Invalid eval gate"):
        normalize_gate(value)


@pytest.mark.parametrize(
    "gate,pass_at_k,pass_power_k,expected",
    [
        ("any", True, False, True),
        ("power", True, False, False),
        ("any", True, True, True),
        ("power", True, True, True),
        ("any", False, False, False),
        ("power", False, False, False),
    ],
)
def test_gate_selects_the_matching_verdict(gate, pass_at_k, pass_power_k, expected):
    assert gate_passed(gate, pass_at_k=pass_at_k, pass_power_k=pass_power_k) is expected


def test_the_two_gates_agree_at_k_1():
    """What makes it safe to set the gate globally and raise K only where it is wanted."""
    for verdict in (True, False):
        assert gate_passed("any", pass_at_k=verdict, pass_power_k=verdict) is gate_passed(
            "power", pass_at_k=verdict, pass_power_k=verdict
        )


def test_gate_label_names_the_gate_and_k():
    assert gate_label("power", 3) == "pass^3"
    assert gate_label("any", 2) == "pass@2"


def test_failure_note_calls_out_an_unstable_item_rather_than_a_broken_one():
    """The message body describes the BEST run, which under pass^K can be one that passed."""
    note = gate_failure_note("power", 2, 3)
    assert "pass^3" in note and "2/3" in note and "unstable" in note


def test_failure_note_does_not_call_a_clean_failure_unstable():
    assert "unstable" not in gate_failure_note("power", 0, 3)
    assert "0/3" in gate_failure_note("power", 0, 3)
    assert "0/1" in gate_failure_note("any", 0, 1)


def test_failure_note_blames_the_judge_not_the_agent_for_an_ungraded_run():
    """An ungraded run is in runs_total but can never be in runs_passed, so calling the
    remainder instability reports a judge outage as a flaky agent."""
    note = gate_failure_note("power", 1, 2, 1)
    assert "1 ungraded" in note
    assert "unstable" not in note


def test_gate_scores_use_K_stable_names():
    """`pass_at_2` becomes `pass_at_3` the moment K changes, splitting every view on it."""
    ctx = MagicMock()
    log_gate_scores(ctx, "trace-1", gate="power", pass_at_k=True, pass_power_k=False)

    logged = {c.kwargs["name"]: c.kwargs["value"] for c in ctx.score.call_args_list}
    assert logged == {"pass_at_k": True, "pass_power_k": False, "gate_passed": False}
    assert not [name for name in logged if name[-1].isdigit()]


def test_gate_passed_is_logged_not_left_to_be_derived():
    """A reader cannot recompute it without the gate, and a report that disagrees with what
    the run gated on is worse than no report."""
    ctx = MagicMock()
    log_gate_scores(ctx, "trace-1", gate="any", pass_at_k=True, pass_power_k=False)

    logged = {c.kwargs["name"]: c.kwargs["value"] for c in ctx.score.call_args_list}
    assert logged["gate_passed"] is True  # same inputs as above, opposite verdict


def test_k_and_gate_ride_the_run_metadata_not_extra_scores():
    metadata = {"github_run_id": "1", "model_version": "gpt-5.6-luna"}
    assert stamp_gate_metadata(metadata, k=3, gate="POWER") is metadata
    assert metadata == {
        "github_run_id": "1",
        "model_version": "gpt-5.6-luna",
        "eval_k": 3,
        "eval_gate": "power",
    }


# --------------------------------------------------------------------------- #
# end to end through an evaluator: general_question is the smallest one
# --------------------------------------------------------------------------- #
@contextlib.contextmanager
def _judged(*verdicts: bool):
    judge = MagicMock()
    judge.model = "gpt-4o"
    judge.score.side_effect = [(v, f"reason-{i}") for i, v in enumerate(verdicts)]
    client = MagicMock()
    client.create_conversation.side_effect = [f"conv-{i}" for i in range(1, len(verdicts) + 1)]
    client.send_message.return_value = ChatResult.model_validate({"textResponse": "answer"})
    with (
        patch("gooddata_eval.core.agentic.general_question.ChatClient", return_value=client),
        patch("gooddata_eval.core.agentic.general_question.LLMJudge", return_value=judge),
    ):
        yield


def _evaluate(gate, verdicts):
    with _judged(*verdicts):
        evaluate_agentic_general_question(
            host="https://example.com",
            token="tok",
            workspace_id="ws",
            question="Q",
            expected_output="rubric",
            k=len(verdicts),
            gate=gate,
            initial_conversation_id="conv-0",
            langfuse=None,
        )


def test_a_flaky_item_passes_under_any_and_fails_under_power():
    """2 of 3 runs passing is green under pass@K and red under pass^K."""
    _evaluate("any", (True, False, True))  # does not raise

    with pytest.raises(GeneralQuestionAssertionError) as exc:
        _evaluate("power", (True, False, True))
    assert "pass^3" in str(exc.value)
    assert "2/3" in str(exc.value)
    assert exc.value.runs_passed == 2
    assert exc.value.runs_effective == 3


def test_a_clean_item_passes_under_both_gates():
    _evaluate("any", (True, True, True))
    _evaluate("power", (True, True, True))


def test_a_hard_failure_fails_under_both_gates():
    """No gate choice rescues an item that fails every run."""
    for gate in ("any", "power"):
        with pytest.raises(GeneralQuestionAssertionError):
            _evaluate(gate, (False, False, False))


# --------------------------------------------------------------------------- #
# signature compatibility — `gate` must not shift an existing positional argument
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "module_name",
    [
        "visualization",
        "metric_skill",
        "alert_skill",
        "kda_skill",
        "general_question",
        "guardrail",
        "search_tool",
    ],
)
def test_gate_is_the_last_parameter_of_every_evaluator(module_name):
    """Inserted anywhere earlier, a positional caller binds max_iterations or
    initial_conversation_id to `gate`, which then reaches normalize_gate and raises."""
    module = importlib.import_module(f"gooddata_eval.core.agentic.{module_name}")
    fn = next(v for k, v in vars(module).items() if k.startswith("evaluate_agentic_"))
    names = [p.name for p in inspect.signature(fn).parameters.values()]

    assert names[-1] == "gate"
    assert names[5] == "k"
    assert names[6] in ("max_iterations", "initial_conversation_id")


def test_a_positional_seventh_argument_still_binds_where_it_used_to():
    """The regression the parameter order protects: 7 positional args, no keywords."""
    with _judged(True):
        evaluate_agentic_general_question(
            "https://example.com",  # host
            "tok",  # token
            "ws",  # workspace_id
            "Q",  # question
            "rubric",  # expected_output
            1,  # k
            "conv-0",  # initial_conversation_id -- NOT gate
        )


# --------------------------------------------------------------------------- #
# mixed datasets — run_items has no gate, so pass^K cannot be honoured for it
# --------------------------------------------------------------------------- #
def _item(test_kind, item_id="i1"):
    return DatasetItem(id=item_id, dataset_name="d", test_kind=test_kind, question="q", expected_output="e")


def _config(gate):
    return RunConfig(host="https://h", token="t", workspace_id="w", gate=gate)


def test_power_gate_is_refused_when_the_dataset_has_non_agentic_items():
    """test_kind is resolved per item, so a dataset can mix the two paths. Running anyway
    would decide half the items on pass@K and still label the report `power`."""
    with pytest.raises(ValueError, match="applies to kinds that repeat K runs"):
        _reject_power_gate_on_ungated_items(_config("power"), [_item("visualization")])


def test_power_gate_is_refused_for_an_agentic_kind_that_takes_no_k():
    """agentic_conversation is in AGENTIC_TEST_KINDS but _dispatch_agentic passes it no
    gate, so accepting it labels a report `power` that it was not decided under."""
    with pytest.raises(ValueError, match="agentic_conversation"):
        _reject_power_gate_on_ungated_items(
            _config("power"), [_item("agentic_visualization", "i1"), _item("agentic_conversation", "i2")]
        )


def test_an_unsupported_kind_is_skipped_rather_than_refused():
    """run_items skips it with a warning under --gate any; refusing here would make one
    misspelled test_kind abort a dataset the default gate runs in full."""
    _reject_power_gate_on_ungated_items(
        _config("power"), [_item("agentic_visualization", "i1"), _item("nonsense_kind", "i2")]
    )


def test_the_refusal_names_the_kinds_to_split_out():
    with pytest.raises(ValueError) as exc:
        _reject_power_gate_on_ungated_items(
            _config("power"), [_item("visualization", "i1"), _item("search_tool", "i2")]
        )
    assert "2 item(s)" in str(exc.value)
    assert "['search_tool', 'visualization']" in str(exc.value)


def test_a_purely_agentic_dataset_is_accepted_under_the_power_gate():
    _reject_power_gate_on_ungated_items(_config("power"), [_item("agentic_visualization")])
    _reject_power_gate_on_ungated_items(_config("power"), [])


def test_the_default_gate_accepts_a_mixed_dataset():
    """pass@K is what the non-agentic path already does, so nothing is misrepresented."""
    _reject_power_gate_on_ungated_items(_config("any"), [_item("visualization")])


# --------------------------------------------------------------------------- #
# reporting — the gate verdict and pass@K are different facts and both are reported
# --------------------------------------------------------------------------- #
def _flaky_item():
    """2 of 3 runs passed: pass@K true, pass^K false, and the best run is a passing one."""
    return ItemReport(
        id="i1",
        dataset_name="d",
        test_kind="agentic_general_question",
        question="q",
        pass_at_k=True,
        gate_passed=False,
        runs=3,
        runs_passed=2,
        best_detail={"general_question_pass": True},
    )


def test_pass_at_k_stays_literal_when_the_power_gate_fails_the_item():
    """The Langfuse score named pass_at_k is summary.pass_at_k, so a JSON field of the same
    name reporting the gate instead makes two outputs of one run disagree."""
    data = build_json_report(EvalReport(model="m", gate="power", items=[_flaky_item()]))

    assert data["items"]["i1"]["pass_at_k"] is True
    assert data["items"]["i1"]["gate_passed"] is False
    assert data["summary"]["passed"] == 0
    assert data["summary"]["failed"] == 1


def test_an_ungated_item_reports_pass_at_k_as_its_verdict():
    """run_items has no gate, so nothing sets gate_passed and pass@K decides."""
    item = ItemReport(id="i1", dataset_name="d", test_kind="visualization", question="q", pass_at_k=True, runs=2)
    data = build_json_report(EvalReport(model="m", items=[item]))

    assert data["items"]["i1"]["gate_passed"] is True
    assert data["summary"]["passed"] == 1


def test_the_console_says_why_a_power_gate_failure_is_a_failure():
    """best_detail describes the best run, which under pass^K passed -- so no check reads
    False and Quality prints 100%. Without the count the row is an unexplained FAIL."""
    text = render_console(EvalReport(model="m", gate="power", items=[_flaky_item()]))

    assert "pass^3 failed" in text
    assert "2/3 runs passed" in text
    assert "did not pass strict checks" not in text


# --------------------------------------------------------------------------- #
# ungated kinds — gate_passed must stay None so it keeps meaning "a gate ran"
# --------------------------------------------------------------------------- #
def _run_one(test_kind: str, **dispatch):
    """One item through run_agentic_items with _dispatch_agentic stubbed.

    Stubbed at the dispatch seam rather than at an evaluator: the kinds differ in what they
    load from the item, and what is under test is how _process_item records the verdict.
    """
    with patch("gooddata_eval.cli.agentic_runner._dispatch_agentic", **dispatch):
        report = run_agentic_items(
            [_item(test_kind, "i1")],
            host="http://h",
            token="tok",
            workspace_id="ws",
            k=2,
            run_ts="2026-01-01",
            gate="power",
        )
    return report.items[0]


def test_an_ungated_kind_records_no_gate_verdict():
    """_dispatch_agentic passes agentic_conversation no gate, so a Boolean here would claim
    a gate decided the item and make an ungated result indistinguishable from a gated one."""
    outcome = AgenticEvalOutcome(reasoning_steps=[], conversation_id="c-1", response_id="r-1", detail={})
    item = _run_one("agentic_conversation", return_value=outcome)

    assert item.error is None
    assert item.gate_passed is None
    assert (item.pass_at_k, item.passed) == (True, True)  # passed falls back to pass@K


def test_an_ungated_kind_records_no_gate_verdict_on_failure_either():
    item = _run_one("agentic_conversation", side_effect=AssertionError("nope"))

    assert item.gate_passed is None
    assert (item.pass_at_k, item.passed) == (False, False)


def test_a_gated_kind_records_the_verdict_the_gate_produced():
    exc = AlertSkillAssertionError("nope")
    exc.runs_passed = 1
    exc.detail = {"alert_created": True}
    item = _run_one("agentic_alert_skill", side_effect=exc)

    assert item.gate_passed is False
    assert item.pass_at_k is True  # 1 of 2 runs passed: pass^2 failed, pass@2 did not
    assert item.passed is False
