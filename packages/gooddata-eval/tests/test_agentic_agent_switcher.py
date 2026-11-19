# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
import contextlib
import json
from typing import Any
from unittest.mock import MagicMock, call, patch

import httpx
import pytest
from gooddata_eval.cli.agentic_runner import AGENTIC_TEST_KINDS, _dispatch_agentic
from gooddata_eval.core.agentic.agent_switcher import (
    AgentSwitcherAssertionError,
    evaluate_agentic_agent_switcher,
    run_agentic_agent_switcher,
)
from gooddata_eval.core.chat.sse_client import ChatError
from gooddata_eval.core.dataset.langfuse_source import _item_from_raw
from gooddata_eval.core.interaction import MULTI_TURN_KINDS
from gooddata_eval.core.models import AgentSwitcherInput, ChatResult, DatasetItem
from pydantic import ValidationError

_MODULE = "gooddata_eval.core.agentic.agent_switcher"

_TWO_TURNS: dict[str, Any] = {
    "agent_id": "planner",
    "turns": [
        {"message": "Plan: watch revenue by region weekly."},
        {"message": "Now set it up.", "switch_to": "builder"},
    ],
}


def _item(spec: dict[str, Any] | None = None, **extra: Any) -> dict[str, Any]:
    return {
        "id": "switch-1",
        "question": "Plan with one agent, build with another",
        "agent_switcher_input": spec or _TWO_TURNS,
        **extra,
    }


def _chat(
    text: str = "ok",
    *,
    skills: list[str] | None = None,
    proposals: list[dict] | None = None,
    viz: dict | None = None,
) -> ChatResult:
    events: list[dict[str, Any]] = (
        [{"functionName": "set_skills", "functionArguments": json.dumps({"skill_names": skills})}]
        if skills is not None
        else []
    )
    return ChatResult.model_validate(
        {
            "textResponse": text,
            "toolCallEvents": events,
            "alertProposals": proposals or [],
            "createdVisualizations": {"objects": [viz]} if viz else None,
        }
    )


def _tool_call(agent: str, name: str, skills: list[str]) -> dict[str, Any]:
    refs = [{"name": s, "title": s.title()} for s in skills]
    return {"role": "assistant", "agentId": agent, "content": {"type": "toolCall", "name": name}, "skillsInUse": refs}


def _items(*turns: tuple[Any, ...]) -> list[dict[str, Any]]:
    """Stored items for turns given as (marker agent or None, answering agent[, skills whose tools ran])."""
    items: list[dict[str, Any]] = []
    for marker, agent, *rest in turns:
        if marker is not None:
            items.append({"role": "system", "agentId": marker, "newAgentId": marker, "trigger": "agent_switched"})
        items.append({"role": "user", "agentId": agent, "skillsInUse": None})
        items.append(_tool_call(agent, "set_skills", []))
        for skill in rest[0] if rest else []:
            items.append(_tool_call(agent, f"{skill}_tool", [skill]))
            items.append({"role": "tool", "agentId": agent, "content": {"type": "toolResult"}})
        items.append({"role": "assistant", "agentId": agent, "content": {"type": "text"}, "skillsInUse": None})
    return items


def _client(answers: list[ChatResult], items: list[dict[str, Any]], *, conversations: int = 1) -> MagicMock:
    client = MagicMock()
    client.create_conversation.side_effect = [f"conv-{i}" for i in range(1, conversations + 1)]
    client.send_message.side_effect = answers
    client.switch_agent.side_effect = lambda _conv, agent: {"conversationId": _conv, "agentId": agent}
    client.list_items.return_value = items
    return client


def _judge(verdict: bool = True) -> MagicMock:
    judge = MagicMock()
    judge.model = "gpt-4o"
    judge.score.return_value = (verdict, "because")
    return judge


@contextlib.contextmanager
def _patched(client: MagicMock, positive: MagicMock | None = None):
    """The positive judge passes unless given; the violation judge finds nothing."""
    judges = [positive or _judge(), _judge(verdict=False)]
    with (
        patch(f"{_MODULE}.ChatClient", return_value=client),
        patch(f"{_MODULE}.LLMJudge", side_effect=judges) as mock_judge,
    ):
        yield mock_judge


def _evaluate(client: MagicMock, item: dict[str, Any] | None = None, positive: MagicMock | None = None, **kwargs: Any):
    with _patched(client, positive):
        return evaluate_agentic_agent_switcher("https://h", "tok", "ws1", item or _item(), **kwargs)


def _failed_check_names(exc: AgentSwitcherAssertionError) -> list[str]:
    return [c["name"] for run in exc.failed_runs for c in run["failed_checks"]]


# --------------------------------------------------------------------------- #
# item validation
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "spec",
    [
        {"agent_id": "a", "turns": []},
        {"agent_id": "", "turns": [{"message": "hi"}]},
        {"turns": [{"message": "hi"}]},
        {"agent_id": "a", "turns": [{"message": "hi", "switch_too": "b"}]},
        {"agent_id": "a", "turns": [{"message": "hi", "checks": {"must_includes": ["x"]}}]},
        {"agent_id": "a", "turns": [{"message": "hi", "checks": {"visualization": {"metric": ["x"]}}}]},
        {"agent_id": "a", "turns": [{"message": "hi", "switch_to": ""}]},
        {"agent_id": "a", "extra": 1, "turns": [{"message": "hi"}]},
    ],
)
def test_an_invalid_input_is_rejected_when_the_item_loads(spec):
    with pytest.raises(ValidationError):
        DatasetItem.model_validate({"id": "i", "dataset_name": "d", "test_kind": "t", "question": "q", **_item(spec)})


def test_an_item_without_input_fails_before_any_request():
    client = _client([], [])
    with pytest.raises(ValueError, match="agent_switcher_input"), _patched(client):
        evaluate_agentic_agent_switcher("https://h", "tok", "ws1", {"id": "i", "question": "q"})
    client.create_conversation.assert_not_called()


def test_the_langfuse_loader_reads_the_input_and_infers_the_kind():
    raw = {"id": "lf-1", "input": {"question": "q"}, "metadata": {"agent_switcher_input": _TWO_TURNS}}
    item = _item_from_raw(raw, dataset_name="ds", test_kind="visualization")
    assert item.test_kind == "agentic_agent_switcher"
    assert item.agent_switcher_input == AgentSwitcherInput.model_validate(_TWO_TURNS)


def test_the_kind_is_registered_and_multi_turn():
    assert "agentic_agent_switcher" in AGENTIC_TEST_KINDS
    assert "agentic_agent_switcher" in MULTI_TURN_KINDS


def test_dispatch_hands_the_whole_item_over():
    item = DatasetItem.model_validate(
        {"dataset_name": "d", "test_kind": "agentic_agent_switcher", "expected_output": {}, **_item()}
    )
    with patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_agent_switcher") as mock_eval:
        _dispatch_agentic(item, "https://h", "tok", "ws1", 3, None, "ts", None, gate="power")
    kwargs = mock_eval.call_args.kwargs
    assert kwargs["dataset_item"] is item
    assert (kwargs["k"], kwargs["gate"], kwargs["dataset_item_id"]) == (3, "power", "switch-1")


# --------------------------------------------------------------------------- #
# switching and the item checks
# --------------------------------------------------------------------------- #
def test_switches_before_the_turn_that_asks_for_it():
    client = _client([_chat(), _chat()], _items((None, "planner"), ("builder", "builder")))
    outcome = _evaluate(client)

    calls = [c for c in client.mock_calls if c[0] in ("create_conversation", "send_message", "switch_agent")]
    assert calls == [
        call.create_conversation(),
        call.send_message("conv-1", "Plan: watch revenue by region weekly."),
        call.switch_agent("conv-1", "builder"),
        call.send_message("conv-1", "Now set it up."),
    ]
    client.list_items.assert_called_once_with("conv-1")
    client.delete_conversation.assert_called_once_with("conv-1")
    assert outcome.runs_passed == 1
    assert outcome.detail["agent_stamped"] is True
    assert outcome.detail["switch_marker"] is True
    assert [t["answering_agents"] for t in outcome.detail["turns"]] == [["planner"], ["builder"]]


def test_the_client_starts_on_the_item_agent_with_its_context():
    client = _client([_chat(), _chat()], _items((None, "planner"), ("builder", "builder")))
    with patch(f"{_MODULE}.ChatClient", return_value=client) as mock_client:
        evaluate_agentic_agent_switcher("https://h", "tok", "ws1", _item(user_context={"view": {}}))
    assert mock_client.call_args.kwargs["agent_id"] == "planner"
    assert mock_client.call_args.kwargs["user_context"] == {"view": {}}


def test_an_answer_stamped_with_the_previous_agent_fails_agent_stamped():
    client = _client([_chat(), _chat()], _items((None, "planner"), ("builder", "planner")))
    with pytest.raises(AgentSwitcherAssertionError) as exc:
        _evaluate(client)
    assert _failed_check_names(exc.value) == ["agent_stamped"]
    assert "turn 2" in str(exc.value)


def test_a_missing_marker_fails_switch_marker():
    client = _client([_chat(), _chat()], _items((None, "planner"), (None, "builder")))
    with pytest.raises(AgentSwitcherAssertionError) as exc:
        _evaluate(client)
    assert _failed_check_names(exc.value) == ["switch_marker"]


def test_a_marker_carrying_the_old_agent_fails_switch_marker():
    client = _client([_chat(), _chat()], _items((None, "planner"), ("planner", "builder")))
    with pytest.raises(AgentSwitcherAssertionError) as exc:
        _evaluate(client)
    assert _failed_check_names(exc.value) == ["switch_marker"]


def test_a_system_item_without_the_switch_trigger_is_not_a_marker():
    items = _items((None, "planner"), ("builder", "builder"))
    items.insert(1, {"role": "system", "agentId": "planner"})
    client = _client([_chat(), _chat()], items)
    assert _evaluate(client).runs_passed == 1


def test_a_drift_marker_is_not_counted_as_a_switch():
    items = _items((None, "planner"), ("builder", "builder"))
    items.insert(0, {"role": "system", "agentId": "planner", "trigger": "agent_updated"})
    client = _client([_chat(), _chat()], items)
    assert _evaluate(client).runs_passed == 1


def test_a_switch_to_the_bound_agent_expects_no_marker():
    spec = {"agent_id": "planner", "turns": [{"message": "a"}, {"message": "b", "switch_to": "planner"}]}
    client = _client([_chat(), _chat()], _items((None, "planner"), (None, "planner")))
    assert _evaluate(client, _item(spec)).runs_passed == 1


def test_a_404_on_switch_fails_the_run_and_names_the_flag():
    client = _client([_chat()], [])
    request = httpx.Request("POST", "https://h/switchAgent")
    client.switch_agent.side_effect = httpx.HTTPStatusError(
        "404", request=request, response=httpx.Response(404, request=request)
    )
    with pytest.raises(AgentSwitcherAssertionError) as exc:
        _evaluate(client)
    assert "flag may be off" in str(exc.value)
    assert _failed_check_names(exc.value) == ["turn2_switched"]
    assert client.send_message.call_count == 1
    client.list_items.assert_not_called()


def test_a_chat_error_stops_the_run():
    client = _client([ChatError("gen-ai fell over")], [])
    with pytest.raises(AgentSwitcherAssertionError) as exc:
        _evaluate(client)
    assert _failed_check_names(exc.value) == ["turn1_answered"]
    client.switch_agent.assert_not_called()


# --------------------------------------------------------------------------- #
# per-turn code checks
# --------------------------------------------------------------------------- #
def _one_turn(checks: dict[str, Any]) -> dict[str, Any]:
    return _item({"agent_id": "a", "turns": [{"message": "m", "checks": checks}]})


@pytest.mark.parametrize(
    ("checks", "used", "failed"),
    [
        ({"skills_used": ["alert"]}, ["alert", "metric"], []),
        ({"skills_used": ["alert"]}, ["metric"], ["turn1_skills_used"]),
        ({"skills_used": ["alert"]}, [], ["turn1_skills_used"]),
        ({"skills_not_used": ["visualization"]}, ["alert"], []),
        ({"skills_not_used": ["visualization"]}, ["visualization"], ["turn1_skills_not_used"]),
    ],
)
def test_skills_checks_read_the_turn_s_tool_calls(checks, used, failed):
    client = _client([_chat()], _items((None, "a", used)))
    if not failed:
        assert _evaluate(client, _one_turn(checks)).runs_passed == 1
        return
    with pytest.raises(AgentSwitcherAssertionError) as exc:
        _evaluate(client, _one_turn(checks))
    assert _failed_check_names(exc.value) == failed


def test_a_carried_over_skill_used_without_set_skills_passes_skills_used():
    spec = {
        "agent_id": "planner",
        "turns": [{"message": "a"}, {"message": "b", "switch_to": "builder", "checks": {"skills_used": ["alert"]}}],
    }
    # set_skills only in turn 1; turn 2 runs an alert tool with no set_skills call
    client = _client(
        [_chat(skills=["alert"]), _chat()],
        _items((None, "planner", ["alert"]), ("builder", "builder", ["alert"])),
    )
    outcome = _evaluate(client, _item(spec))
    assert outcome.runs_passed == 1
    assert [t["skills"] for t in outcome.detail["turns"]] == [["alert"], ["alert"]]


def test_a_requested_skill_whose_tools_never_ran_passes_skills_not_used():
    client = _client([_chat(skills=["key_driver_analysis"])], _items((None, "a", [])))
    assert _evaluate(client, _one_turn({"skills_not_used": ["key_driver_analysis"]})).runs_passed == 1


def test_skills_of_one_turn_do_not_leak_into_the_next():
    spec = {"agent_id": "a", "turns": [{"message": "a"}, {"message": "b", "checks": {"skills_not_used": ["alert"]}}]}
    client = _client([_chat(), _chat()], _items((None, "a", ["alert"]), (None, "a", ["visualization"])))
    assert _evaluate(client, _item(spec)).runs_passed == 1


def test_unreadable_items_fail_every_skills_check():
    spec = {
        "agent_id": "a",
        "turns": [
            {"message": "a", "checks": {"skills_used": ["alert"]}},
            {"message": "b", "checks": {"skills_not_used": ["visualization"]}},
        ],
    }
    client = _client([_chat(), _chat()], [])
    request = httpx.Request("GET", "https://h/items")
    client.list_items.side_effect = httpx.HTTPStatusError(
        "500", request=request, response=httpx.Response(500, request=request)
    )
    with pytest.raises(AgentSwitcherAssertionError) as exc:
        _evaluate(client, _item(spec))
    checks = exc.value.failed_runs[0]["failed_checks"]
    assert [c["name"] for c in checks] == ["items_read", "turn1_skills_used", "turn2_skills_not_used"]
    assert checks[1]["actual"] == "items unreadable"
    assert exc.value.failed_runs[0]["exit_reason"] == "chat_error"


def _proposal(*metric_ids: str) -> dict[str, Any]:
    measures = [
        {"localIdentifier": f"m{i}", "definition": {"measure": {"item": {"identifier": {"id": m}}}}}
        for i, m in enumerate(metric_ids, start=1)
    ]
    return {"cta": "Create?", "alert": {"execution": {"measures": measures}}}


@pytest.mark.parametrize(
    ("expected", "proposals", "ok"),
    [
        ("revenue", [_proposal("revenue")], True),
        ("metric/revenue", [_proposal("revenue")], True),
        ("revenue", [_proposal("orders")], False),
        # revenue is only the comparison side
        ("revenue", [_proposal("orders", "revenue")], False),
        ("revenue", [], False),
    ],
)
def test_alert_metric_reads_the_proposal_measure(expected, proposals, ok):
    client = _client([_chat(proposals=proposals)], _items((None, "a")))
    item = _one_turn({"alert_metric": expected})
    if ok:
        assert _evaluate(client, item).runs_passed == 1
        return
    with pytest.raises(AgentSwitcherAssertionError) as exc:
        _evaluate(client, item)
    assert _failed_check_names(exc.value) == ["turn1_alert_metric"]


_VIZ = {
    "type": "bar_chart",
    "query": {"fields": {"m": {"using": "metric/revenue"}, "o": {"using": "metric/orders"}, "r": "label/region"}},
    "metrics": ["m", "o"],
    "view_by": ["r"],
}


@pytest.mark.parametrize(
    ("expected", "viz", "ok"),
    [
        ({"metrics": ["revenue"], "attributes": ["region"]}, _VIZ, True),
        ({"metrics": ["metric/revenue"], "attributes": ["label/region"]}, _VIZ, True),
        ({"metrics": ["revenue"], "attributes": ["country"]}, _VIZ, False),
        ({"metrics": ["revenue"]}, None, False),
    ],
)
def test_visualization_is_a_subset_match(expected, viz, ok):
    client = _client([_chat(viz=viz)], _items((None, "a")))
    item = _one_turn({"visualization": expected})
    if ok:
        assert _evaluate(client, item).runs_passed == 1
        return
    with pytest.raises(AgentSwitcherAssertionError) as exc:
        _evaluate(client, item)
    assert _failed_check_names(exc.value) == ["turn1_visualization"]


# --------------------------------------------------------------------------- #
# judge
# --------------------------------------------------------------------------- #
def _judged_spec() -> dict[str, Any]:
    return {
        "agent_id": "planner",
        "turns": [
            {"message": "Plan: watch revenue by region weekly."},
            {
                "message": "Now set it up.",
                "switch_to": "builder",
                "checks": {"must_include": ["Restates the plan"], "must_not_include": ["Asks for the plan again"]},
            },
        ],
    }


def test_the_judge_sees_the_transcript_labelled_by_agent():
    client = _client(
        [_chat("Here is the plan"), _chat("Setting up")], _items((None, "planner"), ("builder", "builder"))
    )
    positive = _judge()
    outcome = _evaluate(client, _item(_judged_spec()), positive)
    score_calls = positive.score.call_args_list

    assert len(score_calls) == 1
    for c in score_calls:
        text = c.kwargs["input"]
        assert "USER: Plan: watch revenue by region weekly." in text
        assert "ASSISTANT (agent planner): Here is the plan" in text
        assert "LATEST MESSAGE: Now set it up." in text
        assert "ANSWERED BY: agent builder" in text
        assert c.kwargs["actual_output"] == "Setting up"
    assert outcome.detail["turn2_include_0"] is True
    # The violation judge found nothing, so the exclude criterion holds.
    assert outcome.detail["turn2_exclude_0"] is True


def test_a_failed_criterion_is_named_with_the_judge_reason():
    client = _client([_chat(), _chat()], _items((None, "planner"), ("builder", "builder")))
    with pytest.raises(AgentSwitcherAssertionError) as exc:
        _evaluate(client, _item(_judged_spec()), positive=_judge(verdict=False))
    checks = exc.value.failed_runs[0]["failed_checks"]
    assert [c["name"] for c in checks] == ["turn2_include_0"]
    assert checks[0]["part"] == "judge"


def test_no_judge_is_built_for_an_item_without_criteria():
    client = _client([_chat(), _chat()], _items((None, "planner"), ("builder", "builder")))
    with _patched(client) as mock_judge:
        evaluate_agentic_agent_switcher("https://h", "tok", "ws1", _item())
    mock_judge.assert_not_called()


# --------------------------------------------------------------------------- #
# K runs
# --------------------------------------------------------------------------- #
def test_each_run_replays_on_a_new_conversation():
    answers = [_chat(), _chat(), _chat(), _chat()]
    client = _client(answers, _items((None, "planner"), ("builder", "builder")), conversations=2)
    outcome = _evaluate(client, k=2, gate="power")

    assert client.create_conversation.call_count == 2
    assert [c.args[0] for c in client.send_message.call_args_list] == ["conv-1", "conv-1", "conv-2", "conv-2"]
    assert [c.args for c in client.switch_agent.call_args_list] == [("conv-1", "builder"), ("conv-2", "builder")]
    assert [c.args[0] for c in client.delete_conversation.call_args_list] == ["conv-1", "conv-2"]
    assert (outcome.runs_passed, outcome.runs_effective) == (2, 2)


def test_pass_power_k_fails_when_one_run_fails():
    good = _items((None, "planner"), ("builder", "builder"))
    bad = _items((None, "planner"), ("builder", "planner"))
    client = _client([_chat()] * 4, good, conversations=2)
    client.list_items.side_effect = [good, bad]
    with pytest.raises(AgentSwitcherAssertionError) as exc:
        _evaluate(client, k=2, gate="power")
    assert exc.value.runs_passed == 1
    assert [r["run_index"] for r in exc.value.failed_runs] == [2]


def test_k_below_one_is_refused():
    with pytest.raises(ValueError, match="k must be at least 1"):
        run_agentic_agent_switcher("https://h", "tok", "ws1", AgentSwitcherInput.model_validate(_TWO_TURNS), k=0)


# --------------------------------------------------------------------------- #
# Langfuse scores
# --------------------------------------------------------------------------- #
class _ScoreCtx:
    def __init__(self) -> None:
        self.run_metadata: dict[str, Any] = {}
        self.scores: list[tuple[int, str, Any]] = []

    def trace(self, _conversation_id: str) -> None:
        return None

    @contextlib.contextmanager
    def observe(self, _trace: object, run_idx: int, **_kwargs: Any):
        yield run_idx

    def score(self, trace_id: int, *, name: str, value: Any, data_type: str, comment: str | None = None) -> None:
        self.scores.append((trace_id, name, value))

    def quality(self, trace_id: int, **_kwargs: Any) -> None:
        self.scores.append((trace_id, "quality_score", None))


def test_each_run_is_scored_with_the_switch_checks():
    captured: dict[str, Any] = {}

    def _capture(_submit: object, _identity: object, **kwargs: Any) -> None:
        captured.update(kwargs)

    spec = {
        "agent_id": "planner",
        "turns": [{"message": "a"}, {"message": "b", "switch_to": "builder", "checks": {"skills_used": ["alert"]}}],
    }
    client = _client([_chat(), _chat()], _items((None, "planner"), ("builder", "builder", ["alert"])))
    with patch(f"{_MODULE}.submit_trace_scoring", _capture):
        _evaluate(client, _item(spec), langfuse=MagicMock(), gate="power")
    ctx = _ScoreCtx()
    captured["write_scores"](ctx)

    assert captured["conversation_ids"] == ["conv-1"]
    scores = {name: value for _, name, value in ctx.scores}
    assert scores["agent_switcher_pass"] == 1.0
    assert scores["agent_stamped"] == 1.0
    assert scores["switch_marker"] == 1.0
    assert scores["turn_checks_pass"] == 1.0
    assert ctx.run_metadata == {"eval_k": 1, "eval_gate": "power"}
