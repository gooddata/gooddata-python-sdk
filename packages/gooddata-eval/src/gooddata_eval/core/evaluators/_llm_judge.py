# (C) 2026 GoodData Corporation
"""Shared LLM-as-judge for general_question and guardrail evaluators.

Requires gooddata-eval[llm-judge] (openai>=1.45, for max_completion_tokens) and OPENAI_API_KEY.
Replicates DeepEval GEval(strict_mode=True) without a DeepEval dependency.
"""

import json
import os
from collections.abc import Callable
from typing import Any, NamedTuple

from gooddata_eval.core._output import emit_line
from gooddata_eval.core.config import env_flag, judge_model
from gooddata_eval.core.timing import PhaseTimings

# Turns the per-call ``[judge]`` diagnostics on. Off by default: an 18-item ``--runs 2``
# run emits 36 of these, which buries the per-item progress output.
JUDGE_DIAGNOSTICS_ENV_VAR = "GD_EVAL_JUDGE_DIAGNOSTICS"

# Ceiling on the judge's completion, reasoning tokens included. A verdict body is ~60
# tokens; the rest is headroom for a reasoning model's hidden chain, which is what
# actually consumes the budget. It is a cap and not a reservation -- a non-reasoning
# judge never approaches it -- so one value serves every model. Left unset, the ceiling
# is whatever the provider defaults to, which is how a judge ends up spending its whole
# budget on reasoning and returning an empty body.
JUDGE_MAX_COMPLETION_TOKENS = 4096

# Requests per verdict when the body comes back empty. Truncation is transient -- the
# reasoning chain that overran the budget is resampled -- so it is worth exactly one
# more request. Anything malformed rather than empty is NOT retried: a model that
# answers with the wrong key answers with the wrong key again, and retrying only
# doubles the cost of a prompt that needs fixing.
_EMPTY_BODY_ATTEMPTS = 2


class JudgeResponseError(RuntimeError):
    """The judge returned something that is not a verdict.

    Raised rather than returning a value, because the alternative is worse: the previous
    ``int(data.get("score", 0))`` turned an empty body, a truncated one, a recased key or
    a non-numeric score into a silent FAIL, indistinguishable from the judge genuinely
    failing the answer. A run could report a real pass-rate drop that was actually a parse
    bug. The message quotes the raw body and the response metadata so the cause is
    readable from the error alone.
    """

    # Set by the caller when the item it aborted had already measured something. Declared
    # rather than attached loosely, because the runner reads it off the exception to report
    # what an unevaluable item still cost.
    timings: PhaseTimings


def _message_content(response: Any) -> str | None:
    """The completion body, or None when the response carries no readable choice.

    ``choices`` comes back empty from content filters and from gateways that put an error
    envelope where the completion should be. That is the commonest shape of an unreadable
    judge response, and indexing it directly escaped as a bare ``IndexError`` -- past the
    typed error this module exists to raise, carrying none of the body or metadata that
    makes the cause readable. Returning None routes it through the same empty-body path.
    """
    choices = getattr(response, "choices", None) or []
    if not choices:
        return None
    message = getattr(choices[0], "message", None)
    content = getattr(message, "content", None)
    return content if isinstance(content, str) else None


def _rejects_temperature(exc: Exception) -> bool:
    """Whether this failure is specifically the provider refusing ``temperature``.

    Read off the provider's structured error, never off ``str(exc)``: the openai SDK
    stringifies the whole response body into the exception message, and OpenAI-compatible
    gateways (LiteLLM, vLLM) echo the request back inside that body -- so any 400 from one
    of those carries the literal text ``"temperature": 0``. ``param`` is authoritative;
    providers that omit it get a substring check against the error *message* only, which
    is prose rather than a serialized request.
    """
    body = getattr(exc, "body", None)
    if isinstance(body, dict):
        error = body.get("error")
        error = error if isinstance(error, dict) else body
        if error.get("param") == "temperature":
            return True
        message = error.get("message")
        return "temperature" in message.lower() if isinstance(message, str) else False
    if getattr(exc, "param", None) == "temperature":
        return True
    return "temperature" in str(exc if body is None else body).lower()


def _bit(name: str, read: Callable[[], Any]) -> str:
    """``name=value``, or "" when the field is absent on this provider's response."""
    try:
        return f"{name}={read()}"
    except Exception:
        return ""


def _response_metadata(response: Any) -> str:
    """finish_reason / fingerprint / token counts, best-effort.

    Never raises: diagnostics must not be the thing that breaks an eval run, and not every
    OpenAI-compatible endpoint returns a usage block.
    """
    bits = []
    if not (getattr(response, "choices", None) or []):
        # Says *why* there is no finish_reason below, so the raised JudgeResponseError
        # distinguishes "no choice at all" from "a choice with an empty body".
        bits.append("choices=0")
    bits += [
        _bit("finish_reason", lambda: response.choices[0].finish_reason),
        _bit("system_fingerprint", lambda: response.system_fingerprint),
        _bit("prompt_tokens", lambda: response.usage.prompt_tokens),
        _bit("completion_tokens", lambda: response.usage.completion_tokens),
        _bit("reasoning_tokens", lambda: response.usage.completion_tokens_details.reasoning_tokens),
    ]
    return " ".join(b for b in bits if b)


_SYSTEM_TEMPLATE = """\
You are an impartial evaluator. Score whether the actual output satisfies the criteria.

Evaluation steps:
{steps}

Return a JSON object with exactly two keys:
  "score": 1 if the actual output satisfies all criteria, 0 otherwise
  "reasoning": one sentence explaining your decision
"""

_USER_TEMPLATE = """\
INPUT: {input}
EXPECTED OUTPUT: {expected_output}
ACTUAL OUTPUT: {actual_output}
"""


class LLMJudge:
    """Binary LLM judge (score 0 or 1) for text-answer evaluators."""

    def __init__(self, evaluation_steps: list[str], model: str | None = None):
        try:
            from openai import OpenAI  # noqa: PLC0415
        except ImportError as _err:
            raise ImportError(
                "LLM-as-judge evaluators require the llm-judge extra: uv add 'gooddata-eval[llm-judge]'"
            ) from _err
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise OSError("OPENAI_API_KEY environment variable is required for LLM-as-judge evaluators.")
        self._client = OpenAI(api_key=api_key)
        # Public: the [timer] diagnostics name the model, and hardcoding it there would
        # misreport which judge ran under --judge-model.
        self.model = model or judge_model()
        # Latched off once this model has told us it will not accept temperature=0, so the
        # wasted 400 is paid once per judge instead of once per graded run. Note the scope:
        # a judge is built per item, so a whole eval run still pays it once per item.
        # Hoisting the latch to the class would fix that but would also let one item's
        # provider quirk silently reconfigure every later one.
        self._supports_temperature = True
        self._system_prompt = _SYSTEM_TEMPLATE.format(
            steps="\n".join(f"{i + 1}. {s}" for i, s in enumerate(evaluation_steps))
        )

    def _create_completion(self, messages: list[dict]) -> object:
        """One judge request, dropping temperature if this model refuses it."""
        kwargs: dict = {
            "model": self.model,
            "messages": messages,
            "response_format": {"type": "json_object"},
            "max_completion_tokens": JUDGE_MAX_COMPLETION_TOKENS,
        }
        # temperature=0 is what makes a verdict reproducible: the same response must not
        # pass one run and fail the next. The gpt-5 family rejects the parameter outright
        # ("Only the default (1) value is supported"), so rather than 400 on the first
        # item we drop it, say so, and carry on with a judge that is no longer
        # deterministic -- a real loss of eval quality, hence the warning.
        if self._supports_temperature:
            kwargs["temperature"] = 0
        try:
            return self._client.chat.completions.create(**kwargs)
        except Exception as exc:
            if not (self._supports_temperature and _rejects_temperature(exc)):
                raise
            self._supports_temperature = False
            emit_line(
                f"warning: judge model {self.model!r} rejects temperature=0, so its verdicts are "
                f"NOT deterministic -- the same response may score differently between runs."
            )
            kwargs.pop("temperature", None)
            return self._client.chat.completions.create(**kwargs)

    def score(self, input: str, expected_output: str, actual_output: str) -> tuple[bool, str]:
        """Return (passed, reasoning). passed=True iff score==1."""
        user_prompt = _USER_TEMPLATE.format(
            input=input,
            expected_output=expected_output,
            actual_output=actual_output,
        )
        messages = [
            {"role": "system", "content": self._system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        meta = ""
        for attempt in range(1, _EMPTY_BODY_ATTEMPTS + 1):
            response = self._create_completion(messages)
            raw = _message_content(response)
            meta = _response_metadata(response)
            if env_flag(JUDGE_DIAGNOSTICS_ENV_VAR):
                emit_line(f"[judge] {self.model} {meta} body={raw!r}")
            if isinstance(raw, str) and raw.strip():
                return self._verdict(raw, meta)
            if attempt < _EMPTY_BODY_ATTEMPTS:
                # Announced rather than silent: a retried item costs twice the tokens and
                # latency, and a rising retry rate is the signal that the cap is too low.
                emit_line(f"warning: judge {self.model!r} returned an empty body ({meta}); retrying once.")
        raise JudgeResponseError(
            f"judge {self.model!r} returned an empty body twice -- no verdict to read. {meta}. "
            "finish_reason=length means the model spent its whole completion budget on "
            f"reasoning tokens; raise JUDGE_MAX_COMPLETION_TOKENS (currently {JUDGE_MAX_COMPLETION_TOKENS}) "
            "or use a non-reasoning judge."
        )

    def _verdict(self, raw: str, meta: str) -> tuple[bool, str]:
        """The verdict carried by a non-empty judge body, or ``JudgeResponseError``."""
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise JudgeResponseError(
                f"judge {self.model!r} returned unparseable JSON ({exc}). {meta} body={raw!r}"
            ) from exc
        if not isinstance(data, dict) or "score" not in data:
            raise JudgeResponseError(f"judge {self.model!r} returned no 'score' key. {meta} body={raw!r}")
        score = data["score"]
        # bool first: JSON mode legitimately emits `true`, and bool is a subclass of int.
        if isinstance(score, bool):
            return score, data.get("reasoning", "")
        if isinstance(score, str):
            # A quoted number is a routine JSON-mode quirk, and the prompt asks for `1`,
            # not `"1"`. Rejecting it outright would discard a verdict the judge did give.
            try:
                score = float(score.strip())
            except ValueError:
                raise JudgeResponseError(
                    f"judge {self.model!r} returned a non-numeric score {score!r}. {meta} body={raw!r}"
                ) from None
        if not isinstance(score, (int, float)):
            raise JudgeResponseError(
                f"judge {self.model!r} returned a non-numeric score {score!r}. {meta} body={raw!r}"
            )
        if score not in (0, 1):
            # The binary prompt makes anything outside {0, 1} an unread response, not a
            # FAIL: a 2 (a model reading the rubric as 0-2) or a 0.9 (a confidence, not a
            # verdict) must not be collapsed to 0 while the judge's own "fully correct"
            # text is still attached to it.
            raise JudgeResponseError(
                f"judge {self.model!r} returned an out-of-range score {score!r}; expected 0 or 1. {meta} body={raw!r}"
            )
        return score == 1, data.get("reasoning", "")


class JudgeVerdict(NamedTuple):
    """What one judge request produced: a verdict, or the reason there is not one.

    ``error`` is non-None when the judge returned something unreadable. ``passed`` is
    then False so that no pass@K can ever read such a run as a pass -- but callers must
    *exclude* it rather than count it, because a judge fault is a property of one request,
    not of the agent's answer.
    """

    passed: bool
    reasoning: str
    error: str | None = None


def score_run(judge: LLMJudge, *, input: str, expected_output: str, actual_output: str) -> JudgeVerdict:
    """Grade one run, turning an unreadable judge response into an unscored verdict.

    Letting ``JudgeResponseError`` fly straight out of a K-run loop discarded every run
    already graded, dropped their Langfuse scores on the floor, and reported an item whose
    pass@K was already satisfied as a failure -- the same "a parse bug reads as a pass-rate
    drop" that ``JudgeResponseError`` exists to prevent, reintroduced one layer up. So the
    fault is confined to its own run; the caller decides what to do with the rest, and an
    item with no graded run at all still raises.
    """
    try:
        passed, reasoning = judge.score(input=input, expected_output=expected_output, actual_output=actual_output)
    except JudgeResponseError as exc:
        # Announced, not swallowed: an unscored run changes the denominator of pass@K and
        # a rising rate of them is the signal that the judge or its cap needs attention.
        emit_line(f"warning: judge {judge.model!r} could not grade one run: {exc}")
        return JudgeVerdict(passed=False, reasoning="", error=str(exc))
    return JudgeVerdict(passed=passed, reasoning=reasoning, error=None)
