# (C) 2026 GoodData Corporation. All rights reserved.
"""Agentic search-tool evaluation runner (one scored turn, after any setup turns)."""

from __future__ import annotations

import time
from dataclasses import dataclass, field, replace
from typing import Any

import httpx

from gooddata_eval.core.agentic._failed_runs import build_failed_runs
from gooddata_eval.core.agentic._failure_message import FailedCheck, failed_check_records
from gooddata_eval.core.agentic._gate import (
    DEFAULT_GATE,
    EvalGate,
    gate_passed,
    log_gate_scores,
    stamp_gate_metadata,
)
from gooddata_eval.core.agentic._outcome import (
    JudgeErrorOf,
    agentic_detail,
    agentic_success,
    chat_failure_exit,
    failure_message_head,
    label_runs,
    log_eval_error_score,
    raise_agentic_failure,
)
from gooddata_eval.core.agentic._search_expectation import (
    SEARCH_TOOL,
    SearchExpectation,
    call_args,
    check_arguments,
    deterministic_checks,
    parse_expectation,
    search_calls,
)
from gooddata_eval.core.agentic._trace_linker import (
    RunIdentity,
    RunTraceContext,
    SubmitTraceLink,
    open_item_trace,
    run_trace_link_inline,
    submit_trace_scoring,
    utc_now,
)
from gooddata_eval.core.chat.render import render_answer_text
from gooddata_eval.core.chat.sse_client import ChatClient, ChatError
from gooddata_eval.core.config import ReasoningEffort
from gooddata_eval.core.evaluators._llm_judge import JudgeVerdict, LLMJudge, score_run
from gooddata_eval.core.langfuse.item_scope import item_scope
from gooddata_eval.core.models import (
    AgenticAssertionError,
    AgenticEvalOutcome,
    ChatResult,
    LoopExit,
    ReasoningStepEvent,
    ToolCallEvent,
    build_latency_breakdown,
)

_TRANSPORT_ERRORS: tuple[type[BaseException], ...] = (httpx.HTTPError, TimeoutError, ConnectionError)
# What a chat turn raises when it fails: ChatClient re-raises an HTTP status that outlasts its retries, and a
# transport fault, as the httpx error itself. Anything else is a bug in this package and is left to surface.
_TURN_ERRORS: tuple[type[BaseException], ...] = (ChatError, httpx.HTTPError)


def _judge_provider_errors() -> tuple[type[BaseException], ...]:
    """The errors of a judge request that fails at the provider (timeout, outage, rate limit).

    Such a request leaves the run unscored, not failed. ``openai`` is the optional llm-judge extra, so its
    errors join only when it is installed.
    """
    try:
        from openai import OpenAIError  # noqa: PLC0415
    except ImportError:
        return _TRANSPORT_ERRORS
    return (OpenAIError, *_TRANSPORT_ERRORS)


_DEFAULT_K = 1

# Every check score an item can publish beside tool_selection and tool_correctness. Each is published only for an
# item that opts into it, and search_answer not for a run the judge could not grade.
SEARCH_CONDITIONAL_SCORES = (
    "search_expected_objects",
    "search_widget",
    "search_routing",
    "search_answer",
    "search_limit",
    "search_no_raw_ids",
    "search_user_requested",
    "search_widget_objects",
    "search_forbidden_parts",
    "search_no_object_urls",
)
# The names a score takes where it does not gate the item: every check of a report_only item, and tool_selection of
# an item with search_required false. A score name then means the same on every item.
_DIAGNOSTIC_SUFFIX = "_diagnostic"
SEARCH_DIAGNOSTIC_SCORES = tuple(
    f"{name}{_DIAGNOSTIC_SUFFIX}" for name in ("tool_selection", *SEARCH_CONDITIONAL_SCORES)
)

_RUBRIC_STEPS = [
    "EXPECTED OUTPUT lists the criteria, one per line, that the assistant's LAST reply must meet.",
    "ACTUAL OUTPUT holds the conversation in order. Earlier turns are context only.",
    "A {type/id} chip in a reply is shown to the user as that object's title.",
    "Pass only when the last reply meets every criterion. Fail when it breaks any.",
]


def _tool_selection(tool_call_events: list[ToolCallEvent]) -> bool:
    """Return True if search_objects was called."""
    return any(tc.function_name == SEARCH_TOOL for tc in tool_call_events)


# Arguments that do not determine search quality, so a fixture naming them must not
# fail the call. `limit` has a server-side default the agent is free to choose;
# `emit_widget` was renamed to `user_requested_search` in the tool schema. The
# single-shot evaluator (core/evaluators/search_tool.py) has ignored these since the
# rename -- this path did not, so every fixture written against the older signature
# scored tool_correctness=False while still passing on tool_selection alone.
_IGNORED_SEARCH_ARGS = frozenset({"limit", "emit_widget", "user_requested_search"})


def _loosely_contains(expected: str, actual: str) -> bool:
    """Case-insensitive containment in either direction; an empty string matches nothing."""
    if not expected.strip() or not actual.strip():
        return False
    return expected.lower() in actual.lower() or actual.lower() in expected.lower()


def _list_matches(expected: list, actual: list, *, loose: bool) -> bool:
    """Every expected element must appear in some actual element, and vice versa is not required.

    ``loose`` is substring rather than equality, because free text legitimately tokenizes
    differently on the two sides: a fixture says ["abandonment", "rate", "3ds"] while the agent
    searches the object's title as one phrase, ["Abandonment Rate - 3DS"]. Both name the same
    object, and exact element equality calls that a failure. A list of controlled values
    (``object_types``) is not free text, so it is compared exactly and case-sensitively, as the
    single-shot evaluator does: "METRIC" is not "metric".
    """
    if loose:
        return all(
            any(isinstance(a, str) and isinstance(e, str) and _loosely_contains(e, a) for a in actual) for e in expected
        )
    return all(e in actual for e in expected)


def _afm_matches(expected: dict, actual: Any) -> bool:
    """Every expected measure and attribute is in the call's AFM; a null field in the fixture matches anything.

    The agent states ``aggregation: null`` for a metric and may add objects to the AFM, so neither fails it.
    """
    if not isinstance(actual, dict):
        return False
    if any(actual.get(key) is not None and not isinstance(actual.get(key), list) for key in ("measures", "attributes")):
        return False
    for key in ("measures", "attributes"):
        listed = actual.get(key)
        actual_items = [item for item in listed if isinstance(item, dict)] if isinstance(listed, list) else []
        for exp in expected.get(key) or []:
            if not isinstance(exp, dict):
                return False
            if not any(all(v is None or act.get(k) == v for k, v in exp.items()) for act in actual_items):
                return False
    return True


def _call_matches(args: dict, expected_tool_call: dict) -> bool:
    for key, exp_val in expected_tool_call.items():
        if key in _IGNORED_SEARCH_ARGS:
            continue
        act_val = args.get(key)
        if key == "compatible_with_afm" and isinstance(exp_val, dict):
            if not _afm_matches(exp_val, act_val):
                return False
        elif isinstance(exp_val, list) and isinstance(act_val, list):
            if not _list_matches(exp_val, act_val, loose=key == "keywords"):
                return False
        elif isinstance(exp_val, str) and isinstance(act_val, str):
            if not _loosely_contains(exp_val, act_val):
                return False
        elif exp_val != act_val:
            return False
    return True


def _tool_correctness(tool_call_events: list[ToolCallEvent], expected_tool_call: dict) -> bool:
    """Return True if a search_objects call's arguments match expected.

    List fields (keywords, object_types) use subset matching: every expected value must
    appear in the actual call and the agent may include extras. ``keywords`` match by
    substring; every other list is compared exactly. Any call of the turn may match: the
    agent often looks the measure up first and asks for compatible attributes after.
    """
    return any(_call_matches(call_args(tc), expected_tool_call) for tc in search_calls(tool_call_events))


@dataclass
class SearchResult:
    """Outcome of one K-run search-tool evaluation."""

    conversation_id: str
    tool_selected: bool
    tool_correct: bool
    tool_call_names: list[str]
    reasoning_steps: list[str] = field(default_factory=list)
    response_id: str | None = None
    tool_call_events: list[ToolCallEvent] = field(default_factory=list)
    reasoning_step_events: list[ReasoningStepEvent] = field(default_factory=list)
    # This run's own wall time -- mirrors the single-shot path's best_run_latency_s
    # (see core/runner.py's _run_one_item).
    run_latency_s: float = 0.0
    # The item's opt-in checks of this run, and why each failed one failed.
    checks: dict[str, bool] = field(default_factory=dict)
    check_details: dict[str, Any] = field(default_factory=dict)
    # Why the judge could not grade the answer; the run is then labelled ERROR unless another check failed it.
    harness_error: str | None = None
    # The checks that read False only because of harness_error. Their scores are not published.
    harness_checks: tuple[str, ...] = ()
    # Set when a setup turn failed, so the question was never sent.
    exit_reason: LoopExit | None = None
    passed: bool = False

    @property
    def judge_error(self) -> str | None:
        """The name ``build_failed_runs`` reads a run's ungraded verdict under."""
        return self.harness_error


@dataclass
class AgenticSearchSummary:
    """Aggregated outcome of K runs for search-tool evaluation."""

    run_results: list[SearchResult]
    pass_at_k: bool
    pass_power_k: bool
    best: SearchResult


def _judge_rubric(judge: LLMJudge, rubric: tuple[str, ...], transcript: list[tuple[str, str]]) -> JudgeVerdict:
    """Grade the last reply against the rubric, with the turns before it as context."""
    conversation = "\n\n".join(f"{role}: {text}" for role, text in transcript)
    criteria = "\n".join(f"- {criterion}" for criterion in rubric)
    question = next((text for role, text in reversed(transcript) if role == "User"), "")
    return score_run(judge, input=question, expected_output=criteria, actual_output=conversation)


def _turn_failed(
    conversation_id: str,
    turn: str,
    exit_reason: LoopExit,
    reason: str,
    latency_s: float,
    partial: ChatResult | None = None,
) -> SearchResult:
    """A run whose ``turn`` (``setup_turn`` or ``question_turn``) failed: the agent's FAIL, as a chat failure is for
    every kind.

    Nothing of it is scored. Its latency is the failed turn's own, and the setup turns' when the question was never
    sent. What the agent did before a turn failed is kept for diagnosis only.
    """
    if partial is None:
        partial = ChatResult()
    events = list(partial.tool_call_events or [])
    return SearchResult(
        conversation_id=conversation_id,
        tool_selected=False,
        tool_correct=False,
        tool_call_names=[tc.function_name for tc in events],
        reasoning_steps=list(partial.reasoning_steps or []),
        response_id=partial.response_id,
        tool_call_events=events,
        reasoning_step_events=list(partial.reasoning_step_events or []),
        check_details={turn: reason},
        exit_reason=exit_reason,
        run_latency_s=latency_s,
    )


def _execute_run(
    client: ChatClient,
    conversation_id: str,
    question: str,
    spec: SearchExpectation,
    judge: LLMJudge | None,
) -> SearchResult:
    """Send the item's setup turns, then the question, and score the question's turn alone."""
    transcript: list[tuple[str, str]] = []
    setup_started = time.monotonic()
    for number, turn in enumerate(spec.setup_turns, start=1):
        try:
            setup = client.send_message(conversation_id, turn)
        except _TURN_ERRORS as exc:
            reason = f"setup turn {number} failed: {exc}"
            elapsed = time.monotonic() - setup_started
            partial = getattr(exc, "partial_result", None)
            return _turn_failed(conversation_id, "setup_turn", chat_failure_exit(exc), reason, elapsed, partial)
        setup_text = render_answer_text(setup)
        if not setup_text and not setup.tool_call_events:
            reason = f"setup turn {number} got no answer"
            elapsed = time.monotonic() - setup_started
            return _turn_failed(conversation_id, "setup_turn", LoopExit.AGENT_SILENT, reason, elapsed)
        transcript += [("User", turn), ("Assistant", setup_text)]

    run_started = time.monotonic()
    try:
        chat_result = client.send_message(conversation_id, question)
    except _TURN_ERRORS as exc:
        # Recorded, not raised: an escaping error would discard the runs already completed.
        reason = f"question turn failed: {exc}"
        elapsed = time.monotonic() - run_started
        partial = getattr(exc, "partial_result", None)
        return _turn_failed(conversation_id, "question_turn", chat_failure_exit(exc), reason, elapsed, partial)
    run_latency = time.monotonic() - run_started
    tcs = chat_result.tool_call_events or []
    selected = _tool_selection(tcs)
    run = SearchResult(
        conversation_id=conversation_id,
        tool_selected=selected,
        tool_correct=selected and _tool_correctness(tcs, spec.tool_args),
        tool_call_names=[tc.function_name for tc in tcs],
        reasoning_steps=list(chat_result.reasoning_steps or []),
        response_id=chat_result.response_id,
        tool_call_events=list(chat_result.tool_call_events or []),
        reasoning_step_events=list(chat_result.reasoning_step_events or []),
        run_latency_s=run_latency,
    )
    if spec.has_turn_checks:
        run.checks, run.check_details = deterministic_checks(spec, chat_result)
        if spec.answer_rubric:
            _score_answer(run, spec, judge, transcript, question, chat_result)
    run.passed = (selected or not spec.search_required) and (spec.report_only or all(run.checks.values()))
    return run


def _score_answer(
    run: SearchResult,
    spec: SearchExpectation,
    judge: LLMJudge | None,
    transcript: list[tuple[str, str]],
    question: str,
    chat_result: ChatResult,
) -> None:
    """Grade the reply's text against the rubric. A turn without text fails without asking the judge."""
    answer = (chat_result.text_response or "").strip()
    if not answer:
        run.checks["search_answer"] = False
        run.check_details["search_answer"] = "empty answer: the turn has no text"
        return
    if judge is None:
        raise RuntimeError("answer_rubric needs the LLM judge, which was not built")
    try:
        verdict = _judge_rubric(judge, spec.answer_rubric, [*transcript, ("User", question), ("Assistant", answer)])
    except _judge_provider_errors() as exc:
        verdict = JudgeVerdict(passed=False, reasoning="", error=f"{type(exc).__name__}: {exc}")
    run.checks["search_answer"] = verdict.passed if verdict.error is None else False
    if verdict.error is not None:
        reason = f"judge gave no verdict: {verdict.error}"
        run.check_details["search_answer"] = f"harness: {reason}"
        run.harness_error = reason
        run.harness_checks = ("search_answer",)
    elif not verdict.passed:
        run.check_details["search_answer"] = verdict.reasoning


def _open_harness_error(spec: SearchExpectation) -> JudgeErrorOf:
    """How labels read a run's harness error: only when nothing but the harness-scored checks failed it.

    A run that also failed a check the harness did score is the agent's FAIL, whatever the judge would have said.
    """

    def _read(run: Any) -> str | None:
        if run.harness_error is None:
            return None
        gate_ok = run.tool_selected or not spec.search_required
        failing = {name for name, ok in run.checks.items() if not ok}
        return run.harness_error if gate_ok and failing <= set(run.harness_checks) else None

    return _read


def run_agentic_search_tool(
    host: str,
    token: str,
    workspace_id: str,
    question: str,
    expected_tool_call: dict | None = None,
    k: int = _DEFAULT_K,
    initial_conversation_id: str | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    agent_id: str | None = None,
    user_context: dict | None = None,
    expected_output: dict | None = None,
) -> AgenticSearchSummary:
    """Run the search-tool agentic evaluation K times.

    ``expected_tool_call`` is the bare ``search_objects`` arguments. ``expected_output`` is the item's whole expected output (``tool_call`` plus the checks of
    ``_search_expectation``); when it has no ``tool_call``, ``expected_tool_call`` supplies the arguments.

    Raises:
        ValueError: ``expected_output`` or ``expected_tool_call`` is malformed. Raised before any request.
        ImportError, OSError: The item has an answer rubric and the LLM judge cannot be built (the llm-judge
            extra or OPENAI_API_KEY is missing). Raised before any request.
    """
    spec = _expectation(expected_tool_call, expected_output)
    # Built before the first request: a missing judge is a setup error to report at once.
    judge = LLMJudge(_RUBRIC_STEPS) if spec.answer_rubric else None
    run_results: list[SearchResult] = []

    client = ChatClient(
        host=host,
        token=token,
        workspace_id=workspace_id,
        reasoning_effort=reasoning_effort,
        agent_id=agent_id,
        user_context=user_context,
    )
    try:
        conv_id_0 = initial_conversation_id if initial_conversation_id is not None else client.create_conversation()
        try:
            run_results.append(_execute_run(client, conv_id_0, question, spec, judge))
        finally:
            if initial_conversation_id is None:
                client.delete_conversation(conv_id_0)

        for _ in range(1, k):
            conv_id = client.create_conversation()
            try:
                run_results.append(_execute_run(client, conv_id, question, spec, judge))
            finally:
                client.delete_conversation(conv_id)
    finally:
        client.close()

    pass_at_k = any(r.passed for r in run_results)
    pass_power_k = all(r.passed for r in run_results)
    # A run whose open verdict is the judge's has none, so it ranks below every graded run, as JudgeVerdict.rank does.
    open_error = _open_harness_error(spec)
    best = max(
        run_results,
        key=lambda r: (r.passed, open_error(r) is None, sum(r.checks.values()), r.tool_correct, r.tool_selected),
    )
    return AgenticSearchSummary(
        run_results=run_results,
        pass_at_k=pass_at_k,
        pass_power_k=pass_power_k,
        best=best,
    )


def _expectation(expected_tool_call: dict | None, expected_output: dict | None) -> SearchExpectation:
    """The item's expectation from either calling convention.

    Raises:
        ValueError: ``expected_output`` or ``expected_tool_call`` is malformed.
    """
    if expected_output is None:
        return SearchExpectation(tool_args=check_arguments({} if expected_tool_call is None else expected_tool_call))
    spec = parse_expectation(expected_output)
    if "tool_call" in expected_output or expected_tool_call is None:
        return spec
    return replace(spec, tool_args=check_arguments(expected_tool_call))


class SearchToolAssertionError(AgenticAssertionError):
    """Raised when a search-tool evaluation fails."""


def _gating_checks(run: SearchResult, spec: SearchExpectation) -> dict[str, bool]:
    """The run's checks that decide it: none for a report-only item, and never one the judge could not grade."""
    if spec.report_only:
        return {}
    return {name: ok for name, ok in run.checks.items() if name not in run.harness_checks}


def _check_scores(run: SearchResult, spec: SearchExpectation) -> dict[str, bool]:
    """The run's check scores by published name, ``<name>_diagnostic`` for a check that does not gate the item.

    tool_correctness informs on every item, so it keeps its name. A check the judge could not grade is left out,
    and so is every score of a run whose turn failed: it measured nothing.
    """
    if run.exit_reason is not None:
        return {}
    selection = "tool_selection" if spec.search_required else f"tool_selection{_DIAGNOSTIC_SUFFIX}"
    suffix = _DIAGNOSTIC_SUFFIX if spec.report_only else ""
    scores = {selection: run.tool_selected}
    if spec.tool_args:
        scores["tool_correctness"] = run.tool_correct
    scores.update({f"{name}{suffix}": ok for name, ok in run.checks.items() if name not in run.harness_checks})
    return scores


def _verdict_fields(run: SearchResult, spec: SearchExpectation) -> dict[str, Any]:
    """The run's gating verdicts as top-level booleans of its detail, which the report's quality score counts.

    What does not gate sits under ``diagnostics``: the search verdicts of an item that needs no search, and
    the checks of a report-only item. A run whose turn failed has no search verdicts, as nothing was measured.
    """
    searched = (
        {} if run.exit_reason is not None else {"tool_selected": run.tool_selected, "tool_correct": run.tool_correct}
    )
    fields: dict[str, Any] = dict(searched) if spec.search_required else {}
    fields.update(_gating_checks(run, spec))
    diagnostics: dict[str, bool] = {} if spec.search_required else dict(searched)
    if spec.report_only:
        diagnostics.update({name: ok for name, ok in run.checks.items() if name not in run.harness_checks})
    if diagnostics:
        fields["diagnostics"] = diagnostics
    if run.check_details:
        fields["check_details"] = run.check_details
    if run.harness_error:
        fields["harness_error"] = run.harness_error
    if run.exit_reason is not None:
        fields["exit_reason"] = run.exit_reason.value
    return fields


def evaluate_agentic_search_tool(
    host: str,
    token: str,
    workspace_id: str,
    question: str,
    expected_tool_call: dict | None = None,
    k: int = _DEFAULT_K,
    initial_conversation_id: str | None = None,
    agent_id: str | None = None,
    langfuse: object | None = None,
    dataset_item_id: str = "",
    dataset_name: str = "search",
    run_timestamp: str | None = None,
    model_version_override: str | None = None,
    run_metadata_extra: dict | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    submit_trace_link: SubmitTraceLink = run_trace_link_inline,
    user_context: dict | None = None,
    expected_output: dict | None = None,
    gate: EvalGate = DEFAULT_GATE,
) -> AgenticEvalOutcome:
    """Run search-tool evaluation, log to Langfuse, and raise SearchToolAssertionError on failure.

    Returns the best run's outcome (reasoning_steps, conversation_id, response_id) as an
    AgenticEvalOutcome on success; on failure the same three values are attached to the
    raised exception as ``.reasoning_steps``/``.conversation_id``/``.response_id``.
    ``expected_tool_call`` and ``expected_output`` are read as in ``run_agentic_search_tool``.

    Raises:
        ValueError: ``expected_output`` or ``expected_tool_call`` is malformed. Raised before any request.
    """
    spec = _expectation(expected_tool_call, expected_output)
    identity = RunIdentity(
        host,
        token,
        workspace_id,
        dataset_name,
        run_timestamp,
        model_version_override,
        run_metadata_extra,
        reasoning_effort,
    )
    langfuse, window_start, scope = open_item_trace(langfuse, identity, dataset_item_id, suffix_runs=k > 1)
    with item_scope(scope):
        summary = run_agentic_search_tool(
            host=host,
            token=token,
            workspace_id=workspace_id,
            question=question,
            expected_tool_call=expected_tool_call,
            k=k,
            initial_conversation_id=initial_conversation_id,
            reasoning_effort=reasoning_effort,
            agent_id=agent_id,
            user_context=user_context,
            expected_output=expected_output,
        )

    # Before the Langfuse scores, so an ERROR run gets its marker beside its usual scores.
    open_error = _open_harness_error(spec)
    run_labels = label_runs(summary.run_results, passed=lambda r: r.passed, judge_error=open_error)
    # The runs left without a verdict because the judge's was the one still open. A passing run is not one.
    ungraded = sum(1 for r in summary.run_results if not r.passed and open_error(r) is not None)

    def _strict(run: SearchResult) -> dict[str, bool]:
        # A run whose turn failed measured nothing, so its quality rests on the run's own verdict.
        measured = spec.search_required and run.exit_reason is None
        strict = {"tool_selection": run.tool_selected} if measured else {}
        strict.update(_gating_checks(run, spec))
        return strict or {"passed": run.passed}

    def _run_detail(run: SearchResult) -> dict:
        """The diagnostic fields for ONE run, shared by the best run and every failing one."""
        return {
            **_verdict_fields(run, spec),
            "tool_call_names": run.tool_call_names,
            "latency_breakdown": build_latency_breakdown(run.tool_call_events, run.reasoning_step_events),
        }

    if langfuse is not None and dataset_item_id:
        # Pinned on the calling thread: a deferred poll must not widen its query window.
        window_end = utc_now()

        def _write_scores(ctx: RunTraceContext) -> None:
            stamp_gate_metadata(ctx.run_metadata, k=len(summary.run_results), gate=gate)

            for run_idx, run in enumerate(summary.run_results):
                pt = ctx.trace(run.conversation_id)
                with ctx.observe(
                    pt, run_idx, conversation_id=run.conversation_id, output={"tool_selection": run.tool_selected}
                ) as tid:
                    if (run_error := run_labels.error_label(run_idx)) is not None:
                        log_eval_error_score(ctx, tid, run_error)
                    for name, ok in _check_scores(run, spec).items():
                        ctx.score(tid, name=name, value=float(ok), data_type="BOOLEAN")
                    log_gate_scores(ctx, tid, gate=gate, pass_at_k=summary.pass_at_k, pass_power_k=summary.pass_power_k)
                    ctx.quality(
                        tid,
                        strict_checks=_strict(run),
                        latency_sec=pt.latency if pt else None,
                        cost_usd=pt.total_cost if pt else None,
                    )

        # Before the pass@K raise: a failing item's scores are the ones worth having.
        submit_trace_scoring(
            submit_trace_link,
            identity,
            langfuse=langfuse,
            dataset_item_id=dataset_item_id,
            conversation_ids=[r.conversation_id for r in summary.run_results],
            window_start=window_start,
            window_end=window_end,
            suffix_runs=k > 1,
            write_scores=_write_scores,
            scope=scope,
            item_input=question,
        )

    runs_passed = sum(1 for r in summary.run_results if r.passed)
    runs_effective = len(summary.run_results)

    def _failed_checks(run: SearchResult) -> list[dict]:
        if run.exit_reason is not None:
            # The failed turn, setup_turn or question_turn: no check ran.
            return failed_check_records([FailedCheck(turn, actual=why) for turn, why in run.check_details.items()])
        checks: list[FailedCheck] = []
        if spec.search_required and not run.tool_selected:
            checks.append(FailedCheck("tool_selection", expected=True, actual=run.tool_call_names))
        # An ungraded check is listed only where it gates: a report-only item's checks never fail its run.
        open_checks = {} if spec.report_only else {name: run.checks[name] for name in run.harness_checks}
        checks += [
            FailedCheck(name, expected=True, actual=run.check_details.get(name, False))
            for name, ok in {**_gating_checks(run, spec), **open_checks}.items()
            if not ok
        ]
        return failed_check_records(checks)

    best = summary.best
    detail = agentic_detail(
        best.tool_call_events,
        best.reasoning_step_events,
        **_verdict_fields(best, spec),
        tool_call_names=best.tool_call_names,
        # Only present when it happened, so the usual detail is unchanged. The CLI reports it as runs_ungraded.
        **({"unscored_runs": ungraded} if ungraded else {}),
    )
    # Same predicate pass@K and runs_passed are taken over, so an item's failed_runs and its
    # counts cannot disagree about which runs failed.
    failed_runs = build_failed_runs(
        summary.run_results,
        labels=run_labels,
        detail=_run_detail,
        failed_checks=_failed_checks,
    )

    if not gate_passed(gate, pass_at_k=summary.pass_at_k, pass_power_k=summary.pass_power_k):
        gate_note = failure_message_head(gate, run_labels, runs_passed, failed_runs, ungraded)
        failing = [record["name"] for record in _failed_checks(best)]
        checks_str = f" Failed checks: {', '.join(failing)}; details: {best.check_details}." if failing else ""
        raise_agentic_failure(
            SearchToolAssertionError,
            f"Search tool assertion failed. {gate_note} "
            f"tool_selected={best.tool_selected}, tool_correct={best.tool_correct}. "
            f"Tool calls made: {best.tool_call_names}.{checks_str}",
            harness_error=run_labels.harness_error_record,
            shadow=run_labels.shadow(gate),
            reasoning_steps=best.reasoning_steps,
            conversation_id=best.conversation_id,
            response_id=best.response_id,
            detail=detail,
            runs_passed=runs_passed,
            runs_effective=runs_effective,
            best_run_latency_s=best.run_latency_s,
            failed_runs=failed_runs,
            run_latencies_s=[r.run_latency_s for r in summary.run_results],
        )
    return agentic_success(
        shadow=run_labels.shadow(gate),
        reasoning_steps=best.reasoning_steps,
        conversation_id=best.conversation_id,
        response_id=best.response_id,
        detail=detail,
        runs_passed=runs_passed,
        runs_effective=runs_effective,
        failed_runs=failed_runs,
        run_latencies_s=[r.run_latency_s for r in summary.run_results],
        best_run_latency_s=best.run_latency_s,
    )
