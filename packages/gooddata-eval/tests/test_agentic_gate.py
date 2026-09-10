# (C) 2026 GoodData Corporation
"""The K gate: which of pass@K / pass^K decides an item, and what reaches Langfuse."""

import contextlib
import importlib
import inspect
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.cli.main import _reject_power_gate_on_non_agentic_items
from gooddata_eval.core.agentic._gate import (
    DEFAULT_GATE,
    gate_failure_note,
    gate_label,
    gate_passed,
    log_gate_scores,
    stamp_gate_metadata,
)
from gooddata_eval.core.agentic.general_question import (
    GeneralQuestionAssertionError,
    evaluate_agentic_general_question,
)
from gooddata_eval.core.config import RunConfig, normalize_gate
from gooddata_eval.core.models import ChatResult, DatasetItem


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
    with pytest.raises(ValueError, match="applies to agentic kinds only"):
        _reject_power_gate_on_non_agentic_items(_config("power"), [_item("visualization")])


def test_the_refusal_names_the_kinds_to_split_out():
    with pytest.raises(ValueError) as exc:
        _reject_power_gate_on_non_agentic_items(_config("power"), [_item("visualization", "i1"), _item("search", "i2")])
    assert "2 item(s)" in str(exc.value)
    assert "['search', 'visualization']" in str(exc.value)


def test_a_purely_agentic_dataset_is_accepted_under_the_power_gate():
    _reject_power_gate_on_non_agentic_items(_config("power"), [])


def test_the_default_gate_accepts_a_mixed_dataset():
    """pass@K is what the non-agentic path already does, so nothing is misrepresented."""
    _reject_power_gate_on_non_agentic_items(_config("any"), [_item("visualization")])
