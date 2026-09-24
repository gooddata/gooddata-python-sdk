# (C) 2026 GoodData Corporation. All rights reserved.
"""Agentic data-obfuscation evaluation runner.

gen-ai masks sensitive values out of the copy it stores and the copy it exports to
Langfuse; what the model and the user's stream see stays as typed. So this kind does not
grade the answer for masking. It plants synthetic canaries in one or more user turns, reads
back the stored conversation and every Langfuse trace of the session, and decides by exact
substring (``_obfuscation_check``) -- no LLM decides whether a value leaked.

``expected_output``:
  canaries            [{nonce, value, class, absent_from, present_in, mask_marker_present,
                        record_only_paths, ...}] -- see ``_obfuscation_check``
  status              "enforced" | "known_limitation"
  expected_turn_rejected  {status_code, reason} when the first turn must be refused
  observe             optional record-only checks, see ``_obfuscation_observe``
  anchors             optional; one non-sensitive fragment per turn, derived when absent

A leak in any run fails the item whatever the gate: one stored secret is one too many. Every
other failure -- a missing trace, a blind sink, an over-masked value -- is a failed run the gate
decides on, as for every other kind.

Before the first item of a workspace a preflight probe proves the environment can show a
result at all -- the database leg masks, the Langfuse leg masks, and both read-backs see
the probe. Without it an item could only pass by not looking.
"""

from __future__ import annotations

import json
import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any

import httpx

from gooddata_eval.core._output import emit_line
from gooddata_eval.core.agentic._gate import (
    DEFAULT_GATE,
    EvalGate,
    gate_failure_note,
    gate_passed,
    log_gate_scores,
    stamp_gate_metadata,
)
from gooddata_eval.core.agentic._obfuscation_check import (
    SINK_CONVERSATION_DB,
    SINK_LANGFUSE_TRACE,
    canary_needles,
    derive_anchor,
    evaluate_case,
)
from gooddata_eval.core.agentic._obfuscation_observe import WorkspaceEntities, observe_and_clean, snapshot
from gooddata_eval.core.agentic._obfuscation_sinks import (
    SinkUnavailableError,
    read_conversation_db,
    read_langfuse_session,
)
from gooddata_eval.core.agentic._trace_linker import (
    RunIdentity,
    RunTraceContext,
    SubmitTraceLink,
    open_trace_window,
    run_trace_link_inline,
    submit_trace_scoring,
    utc_now,
)
from gooddata_eval.core.chat.render import render_answer_text
from gooddata_eval.core.chat.sse_client import ChatClient, ChatError
from gooddata_eval.core.config import ReasoningEffort
from gooddata_eval.core.models import AgenticAssertionError, AgenticEvalOutcome, ChatResult

_DEFAULT_K = 1
_LOG = "[obfuscation]"
_PREFLIGHT_ATTEMPTS = 3
_PREFLIGHT_RETRY_SEC = 10.0
# User ids this short and common are scrubbed out of traces as plain words, which breaks up
# a canary such as "...@northwind-demo.invalid" before the detector sees it.
_SCRUB_PRONE_USER_IDS = frozenset({"demo", "test", "admin", "user"})
_COMMENT_LIMIT = 2000

_preflight_lock = threading.Lock()
_preflight_results: dict[tuple[str, str], str | None] = {}


class ObfuscationAssertionError(AgenticAssertionError):
    """Raised when an obfuscation evaluation fails: a leak, an over-masked value, or a blind sink."""


@dataclass
class ObfuscationRun:
    """One conversation of an obfuscation item: what was sent, what came back, the verdict."""

    conversation_id: str
    anchors: list[str]
    # Per turn: None when answered, else {"status_code", "reason"} of the refusal.
    errors: list[dict[str, Any] | None] = field(default_factory=list)
    answers: list[str] = field(default_factory=list)
    # Per turn: streamed text and visualizations, for record-only stream markers.
    streams: list[str] = field(default_factory=list)
    failures: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    last_result: ChatResult | None = None
    # Sinks whose read-back came back (a rejected turn's empty Langfuse leg counts): a verdict
    # about a sink says nothing unless the sink is here.
    sinks_read: set[str] = field(default_factory=set)

    @property
    def trace_found(self) -> bool:
        return SINK_LANGFUSE_TRACE in self.sinks_read

    @property
    def leak_free(self) -> bool:
        return bool(self.sinks_read) and not any(f.startswith("LEAK") for f in self.failures)

    @property
    def passed(self) -> bool:
        return not self.failures


@dataclass
class AgenticObfuscationSummary:
    run_results: list[ObfuscationRun]
    pass_at_k: bool
    pass_power_k: bool
    best: ObfuscationRun


def _anchors(expected: dict[str, Any], turns: list[str]) -> list[str]:
    declared = expected.get("anchors")
    if declared is not None:
        return list(declared)
    canaries = expected.get("canaries", [])
    anchors = []
    for index, turn in enumerate(turns):
        anchor = derive_anchor(turn, canaries)
        if anchor is None:
            raise ValueError(
                f"turn {index}: no non-sensitive fragment of 12+ word characters to anchor the read-back on; "
                "declare expected_output.anchors"
            )
        anchors.append(anchor)
    return anchors


def _send_turn(client: ChatClient, conversation_id: str, turn: str) -> tuple[ChatResult | None, dict[str, Any] | None]:
    """One turn; a refused turn is returned, not raised, because some items expect it."""
    try:
        return client.send_message(conversation_id, turn), None
    except ChatError as exc:
        return exc.partial_result, {"status_code": exc.status_code, "reason": exc.reason}


def _stream_of(result: ChatResult | None) -> str:
    """What the turn streamed to the user: text, visualizations and alert proposals."""
    if result is None:
        return ""
    shown = result.model_dump(include={"text_response", "created_visualizations", "alert_proposals"})
    return json.dumps(shown, default=str)


def run_obfuscation_case(
    client: ChatClient,
    http: httpx.Client,
    langfuse: Any,
    conversations_url: str,
    conversation_id: str,
    turns: list[str],
    expected: dict[str, Any],
    entities: WorkspaceEntities | None = None,
) -> ObfuscationRun:
    """Drive the turns, read back both sinks and judge them; report and clean up ``observe``."""
    spec = expected.get("observe") or {}
    before = snapshot(entities, spec) if entities is not None and spec else None
    run: ObfuscationRun | None = None
    try:
        run = _drive_and_judge(client, http, langfuse, conversations_url, conversation_id, turns, expected)
        return run
    finally:
        # Also on failure: a persistent workspace must not keep what a failed run created.
        if entities is not None and before is not None:
            notes = observe_and_clean(entities, spec, before, run.streams[-1] if run and run.streams else "")
            if run is not None:
                run.notes.extend(notes)


def _drive_and_judge(
    client: ChatClient,
    http: httpx.Client,
    langfuse: Any,
    conversations_url: str,
    conversation_id: str,
    turns: list[str],
    expected: dict[str, Any],
) -> ObfuscationRun:
    rejection = expected.get("expected_turn_rejected")
    run = ObfuscationRun(conversation_id, [] if rejection else _anchors(expected, turns))

    for index, turn in enumerate(turns):
        result, error = _send_turn(client, conversation_id, turn)
        run.last_result = result or run.last_result
        run.errors.append(error)
        run.answers.append(render_answer_text(result) if result is not None else "")
        run.streams.append(_stream_of(result))
        if error is not None:
            break
        if rejection:
            run.failures.append(f"turn {index} was expected to be refused with {rejection} but was answered")
            return run

    error = run.errors[-1]
    if error is not None and not rejection:
        hint = (
            " (503 DATA_OBFUSCATION_UNAVAILABLE: the inference gateway was not reachable)"
            if error.get("reason") == "DATA_OBFUSCATION_UNAVAILABLE"
            else ""
        )
        run.failures.append(
            f"turn {len(run.errors) - 1} failed with {error}, so the item says nothing about masking{hint}"
        )
        return run
    if rejection and (
        (error or {}).get("status_code") != rejection.get("status_code")
        or (error or {}).get("reason") != rejection.get("reason")
    ):
        run.failures.append(f"turn refused with {error}, expected {rejection}")

    judge_sinks(run, http, langfuse, conversations_url, expected, rejected=bool(rejection))
    return run


def judge_sinks(
    run: ObfuscationRun,
    http: httpx.Client,
    langfuse: Any,
    conversations_url: str,
    expected: dict[str, Any],
    *,
    rejected: bool = False,
) -> None:
    """Read back both sinks of ``run``'s conversation and add their verdict to ``run``."""
    sinks: dict[str, Any] = {}
    try:
        sinks[SINK_CONVERSATION_DB] = read_conversation_db(http, conversations_url, run.conversation_id, run.anchors)
        run.sinks_read.add(SINK_CONVERSATION_DB)
    except SinkUnavailableError as exc:
        sinks[SINK_CONVERSATION_DB] = None
        run.failures.append(str(exc))
    try:
        sinks[SINK_LANGFUSE_TRACE] = read_langfuse_session(
            langfuse, run.conversation_id, run.anchors, allow_empty=rejected
        )
        run.sinks_read.add(SINK_LANGFUSE_TRACE)
    except SinkUnavailableError as exc:
        sinks[SINK_LANGFUSE_TRACE] = None
        run.failures.append(str(exc))

    verdict = evaluate_case(expected, sinks, run.anchors, turn_rejected=rejected)
    run.failures.extend(f for f in verdict.failures if f not in run.failures)
    run.notes.extend(verdict.notes)


# The probe proves the environment masks at all, not that every stored copy is masked -- the
# items decide that. In the database only the stored message text is gated; a copy the agent
# puts elsewhere (a tool's step detail, conversation state) is reported, so a leak there
# fails the item that finds it instead of stopping every item of the run. Langfuse paths
# start with "$[" and stay gated everywhere.
_PROBE_RECORD_ONLY = [r"^\$\.(?!items\[\d+\]\.content\.text$)"]


def _probe() -> tuple[list[str], dict[str, Any]]:
    nonce = f"preflight{uuid.uuid4().hex[:8]}"
    # Worded so the agent answers without a tool: a value it searches for is copied into the
    # step detail of that call.
    question = (
        "Reply with the single word OK. Do not search, look anything up or use any tools. "
        f"Reference only: qa.{nonce}@example.invalid"
    )
    return [question], {
        "canaries": [
            {
                "nonce": nonce,
                "value": f"qa.{nonce}@example.invalid",
                "class": "EMAIL",
                "absent_from": [SINK_CONVERSATION_DB, SINK_LANGFUSE_TRACE],
                "mask_marker_present": "[EMAIL]",
                "record_only_paths": _PROBE_RECORD_ONLY,
            }
        ],
        "status": "enforced",
    }


def _warn_on_scrub_prone_user(http: httpx.Client, host: str) -> None:
    resp = http.get(f"{host.rstrip('/')}/api/v1/profile")
    if resp.status_code >= 400:
        emit_line(f"{_LOG} warning: /api/v1/profile answered {resp.status_code}; user-id scrub check skipped")
        return
    user_id = str(resp.json().get("userId", ""))
    if user_id.lower() in _SCRUB_PRONE_USER_IDS:
        emit_line(
            f"{_LOG} warning: user id {user_id!r} is a common word; the Langfuse user-id scrub can split canaries "
            "containing it and report leaks that are not the detector's"
        )


def _preflight(client: ChatClient, http: httpx.Client, langfuse: Any, host: str, conversations_url: str) -> str | None:
    """None when the environment can show a masking result, else why it cannot."""
    _warn_on_scrub_prone_user(http, host)
    last: ObfuscationRun | None = None
    for attempt in range(1, _PREFLIGHT_ATTEMPTS + 1):
        turns, expected = _probe()
        conversation_id = client.create_conversation()
        try:
            last = run_obfuscation_case(client, http, langfuse, conversations_url, conversation_id, turns, expected)
        finally:
            client.delete_conversation(conversation_id)
        if last.passed:
            emit_line(f"{_LOG} preflight passed (attempt {attempt})")
            for note in last.notes:
                emit_line(f"{_LOG}   preflight note: {note}")
            return None
        # The workspace setting reaches gen-ai through metadata sync, so a first probe can
        # still run unmasked; a later one decides.
        emit_line(f"{_LOG} preflight attempt {attempt} failed: {last.failures}")
        if attempt < _PREFLIGHT_ATTEMPTS:
            time.sleep(_PREFLIGHT_RETRY_SEC)
    assert last is not None
    return (
        f"obfuscation preflight failed: {last.failures}. Check: inference-gateway deployed; flags "
        "enableGenAiDataObfuscation (database) and enableGenAiTraceObfuscation (Langfuse) on for the org; setting "
        "enableAiDataObfuscation on for the workspace; LANGFUSE_* credentials of the project this environment "
        "exports to."
    )


def require_preflight(
    client: ChatClient, http: httpx.Client, langfuse: Any, host: str, workspace_id: str, conversations_url: str
) -> None:
    key = (host.rstrip("/"), workspace_id)
    with _preflight_lock:
        if key not in _preflight_results:
            _preflight_results[key] = _preflight(client, http, langfuse, host, conversations_url)
        reason = _preflight_results[key]
    if reason is not None:
        raise ObfuscationAssertionError(reason)


def run_agentic_obfuscation(
    host: str,
    token: str,
    workspace_id: str,
    question: str,
    expected_output: dict[str, Any],
    k: int = _DEFAULT_K,
    turns: list[str] | None = None,
    initial_conversation_id: str | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    agent_id: str | None = None,
    langfuse: Any = None,
) -> AgenticObfuscationSummary:
    """Run the obfuscation evaluation K times and return a summary.

    ``turns`` is the scripted conversation; a single-turn item passes only ``question``.
    ``langfuse`` must be an ``HttpxLangfuseClient``: the Langfuse leg is read, not just scored.
    """
    if k < 1:
        raise ValueError(f"an obfuscation item needs at least one run, got k={k}")
    all_turns = list(turns) if turns else [question]
    client = ChatClient(
        host=host, token=token, workspace_id=workspace_id, reasoning_effort=reasoning_effort, agent_id=agent_id
    )
    http = httpx.Client(headers={"Authorization": f"Bearer {token}"}, timeout=60.0)
    conversations_url = f"{host.rstrip('/')}/api/v1/ai/workspaces/{workspace_id}/chat/conversations"
    entities = WorkspaceEntities(http, host, workspace_id)
    run_results: list[ObfuscationRun] = []
    try:
        require_preflight(client, http, langfuse, host, workspace_id, conversations_url)
        for index in range(k):
            owned = not (index == 0 and initial_conversation_id is not None)
            conversation_id = client.create_conversation() if owned else initial_conversation_id
            assert conversation_id is not None
            try:
                run = run_obfuscation_case(
                    client, http, langfuse, conversations_url, conversation_id, all_turns, expected_output, entities
                )
                run_results.append(run)
                emit_run(run, expected_output)
            finally:
                if owned:
                    client.delete_conversation(conversation_id)
    finally:
        client.close()
        http.close()

    pass_at_k = any(r.passed for r in run_results)
    pass_power_k = bool(run_results) and all(r.passed for r in run_results)
    best = next((r for r in run_results if r.passed), run_results[0])
    return AgenticObfuscationSummary(run_results, pass_at_k, pass_power_k, best)


def emit_run(run: ObfuscationRun, expected: dict[str, Any]) -> None:
    """Log one run: its turns, notes and verdict."""
    status = expected.get("status", "enforced")
    emit_line(f"{_LOG} conversation={run.conversation_id} status={status} anchors={run.anchors}")
    for index, (error, answer) in enumerate(zip(run.errors, run.answers)):
        emit_line(f"{_LOG}   turn {index}: " + (f"error={error}" if error else f"answer={answer[:200]!r}"))
    for note in run.notes:
        emit_line(f"{_LOG}   note: {note}")
    emit_line(f"{_LOG}   verdict={'PASS' if run.passed else 'FAIL'}")
    for failure in run.failures:
        emit_line(f"{_LOG}   - {failure}")


def without_canaries(text: str, canaries: list[dict[str, Any]]) -> str:
    """Replace every canary spelling by its class, for text that leaves the evaluation (Langfuse)."""
    for canary in canaries:
        for needle in sorted(canary_needles(canary), key=len, reverse=True):
            text = text.replace(needle, f"<{canary.get('class')}>")
    return text


def evaluate_agentic_obfuscation(
    host: str,
    token: str,
    workspace_id: str,
    question: str,
    expected_output: dict[str, Any],
    k: int = _DEFAULT_K,
    turns: list[str] | None = None,
    initial_conversation_id: str | None = None,
    agent_id: str | None = None,
    langfuse: object | None = None,
    dataset_item_id: str = "",
    dataset_name: str = "obfuscation",
    run_timestamp: str | None = None,
    model_version_override: str | None = None,
    run_metadata_extra: dict | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    submit_trace_link: SubmitTraceLink = run_trace_link_inline,
    gate: EvalGate = DEFAULT_GATE,
) -> AgenticEvalOutcome:
    """Run the obfuscation evaluation, log to Langfuse, and raise ObfuscationAssertionError on failure."""
    if not isinstance(expected_output, dict) or not expected_output.get("canaries"):
        raise ValueError("agentic_obfuscation expected_output must be an object with a non-empty 'canaries' list")
    langfuse, window_start = open_trace_window(langfuse)
    summary = run_agentic_obfuscation(
        host=host,
        token=token,
        workspace_id=workspace_id,
        question=question,
        expected_output=expected_output,
        k=k,
        turns=turns,
        initial_conversation_id=initial_conversation_id,
        reasoning_effort=reasoning_effort,
        agent_id=agent_id,
        langfuse=langfuse,
    )
    canaries = expected_output["canaries"]
    leak_free = all(r.leak_free for r in summary.run_results)
    leaked = any(f.startswith("LEAK") for r in summary.run_results for f in r.failures)
    failures = [f"run {i}: {f}" for i, r in enumerate(summary.run_results) for f in r.failures]
    item_passed = not leaked and gate_passed(gate, pass_at_k=summary.pass_at_k, pass_power_k=summary.pass_power_k)

    if langfuse is not None and dataset_item_id:
        window_end = utc_now()

        def _write_scores(ctx: RunTraceContext) -> None:
            stamp_gate_metadata(ctx.run_metadata, k=len(summary.run_results), gate=gate)
            for run_idx, run in enumerate(summary.run_results):
                pt = ctx.trace(run.conversation_id)
                with ctx.observe(
                    pt, run_idx, conversation_id=run.conversation_id, output={"obfuscation_pass": run.passed}
                ) as tid:
                    # The run's own failures: another run's leak must not annotate a run that passed.
                    comment = without_canaries("; ".join(run.failures), canaries)[:_COMMENT_LIMIT] or "no failure"
                    ctx.score(
                        tid, name="obfuscation_pass", value=float(run.passed), data_type="BOOLEAN", comment=comment
                    )
                    ctx.score(tid, name="obfuscation_no_leak", value=float(run.leak_free), data_type="BOOLEAN")
                    ctx.score(tid, name="obfuscation_trace_found", value=float(run.trace_found), data_type="BOOLEAN")
                    recorded = [n for n in run.notes if n.startswith(("RECORDED", "OBSERVED"))]
                    if recorded:
                        # Record-only: what the SC does not rule on yet, next to the verdict it did not change.
                        ctx.score(
                            tid,
                            name="obfuscation_record_only_hit",
                            value=float(any(n.startswith("RECORDED") for n in recorded)),
                            data_type="BOOLEAN",
                            comment=without_canaries("; ".join(recorded), canaries)[:_COMMENT_LIMIT],
                        )
                    # A leak in any run fails the item whatever the gate, so gate_passed -- the
                    # verdict reports read first -- must not say pass@K passed when one run leaked.
                    log_gate_scores(
                        ctx,
                        tid,
                        gate=gate,
                        pass_at_k=summary.pass_at_k and not leaked,
                        pass_power_k=summary.pass_power_k and not leaked,
                    )
                    ctx.quality(
                        tid,
                        strict_checks={"obfuscation_no_leak": run.leak_free, "obfuscation_pass": run.passed},
                        latency_sec=pt.latency if pt else None,
                        cost_usd=pt.total_cost if pt else None,
                    )

        # Before the raise: a failing item's scores are the ones worth having.
        submit_trace_scoring(
            submit_trace_link,
            RunIdentity(
                host,
                token,
                workspace_id,
                dataset_name,
                run_timestamp,
                model_version_override,
                run_metadata_extra,
                reasoning_effort,
            ),
            langfuse=langfuse,
            dataset_item_id=dataset_item_id,
            conversation_ids=[r.conversation_id for r in summary.run_results],
            window_start=window_start,
            window_end=window_end,
            suffix_runs=len(summary.run_results) > 1,
            write_scores=_write_scores,
            item_input=turns or question,
        )

    best = summary.best
    runs_passed = sum(1 for r in summary.run_results if r.passed)
    runs_effective = len(summary.run_results)
    last = best.last_result
    detail = {
        "leak_free": leak_free,
        # False when the Langfuse leg was never read in some run: a no-leak verdict there would
        # mean nothing. Named for the good outcome, as every boolean in a detail is read as a check.
        "trace_found": all(r.trace_found for r in summary.run_results),
        "failures": failures,
        "notes": [n for r in summary.run_results for n in r.notes],
        "actual_output": best.answers[-1] if best.answers else "",
    }
    reasoning_steps = list(last.reasoning_steps or []) if last else []
    response_id = last.response_id if last else None

    if not item_passed:
        note = gate_failure_note(gate, runs_passed, runs_effective)
        exc = ObfuscationAssertionError(f"Obfuscation assertion failed. {note} " + "; ".join(failures))
        exc.reasoning_steps = reasoning_steps
        exc.conversation_id = best.conversation_id
        exc.response_id = response_id
        exc.detail = detail
        exc.runs_passed = runs_passed
        exc.runs_effective = runs_effective
        raise exc
    return AgenticEvalOutcome(
        runs_passed=runs_passed,
        runs_effective=runs_effective,
        reasoning_steps=reasoning_steps,
        conversation_id=best.conversation_id,
        response_id=response_id,
        detail=detail,
    )
