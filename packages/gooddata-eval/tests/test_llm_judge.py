# (C) 2026 GoodData Corporation
import json
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.config import JUDGE_MODEL_ENV_VAR, judge_model
from gooddata_eval.core.evaluators._llm_judge import (
    JUDGE_DIAGNOSTICS_ENV_VAR,
    JUDGE_MAX_COMPLETION_TOKENS,
    JudgeResponseError,
    LLMJudge,
    score_run,
)


@pytest.fixture(autouse=True)
def _openai_api_key(monkeypatch):
    """Every judge here talks to a stubbed client, but LLMJudge still refuses to build
    without the key -- so supply it once rather than at each construction site."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")


def _make_judge(*, model: str | None = None) -> LLMJudge:
    """A judge whose openai client is a MagicMock.

    ``LLMJudge.__init__`` never calls the API, so every caller stubs the response
    afterwards on ``judge._client.chat.completions.create``.
    """
    with patch("openai.OpenAI"):
        return LLMJudge(evaluation_steps=["Step 1: check the answer is correct."], model=model)


def _mock_raw_response(
    content: str | None,
    *,
    finish_reason: str = "stop",
    prompt_tokens: int = 700,
    completion_tokens: int = 60,
    reasoning_tokens: int = 0,
    fingerprint: str = "fp_test",
):
    """A chat completion whose body is exactly ``content``, metadata and all."""
    resp = MagicMock()
    resp.choices[0].message.content = content
    resp.choices[0].finish_reason = finish_reason
    resp.system_fingerprint = fingerprint
    resp.usage.prompt_tokens = prompt_tokens
    resp.usage.completion_tokens = completion_tokens
    resp.usage.completion_tokens_details.reasoning_tokens = reasoning_tokens
    return resp


def _mock_response(score: int, reasoning: str = "ok"):
    return _mock_raw_response(json.dumps({"score": score, "reasoning": reasoning}))


def test_llm_judge_returns_true_on_score_1():
    judge = _make_judge()
    judge._client.chat.completions.create = MagicMock(return_value=_mock_response(1))
    passed, reasoning = judge.score("q", "expected answer", "actual answer")
    assert passed is True
    assert reasoning == "ok"


def test_llm_judge_returns_false_on_score_0():
    judge = _make_judge()
    judge._client.chat.completions.create = MagicMock(return_value=_mock_response(0, "wrong"))
    passed, _ = judge.score("q", "expected answer", "wrong answer")
    assert passed is False


def test_llm_judge_raises_without_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with patch("openai.OpenAI"), pytest.raises(OSError, match="OPENAI_API_KEY"):
        LLMJudge(evaluation_steps=["s"])


def test_default_judge_model_is_gpt_4o(monkeypatch):
    # Deterministic (temperature=0) and independent of the agent under test. Both matter:
    # a judge sharing the agent's model family grades its own output.
    monkeypatch.delenv(JUDGE_MODEL_ENV_VAR, raising=False)
    assert judge_model() == "gpt-4o"
    assert _make_judge().model == "gpt-4o"


def test_judge_model_can_be_overridden_by_env(monkeypatch):
    monkeypatch.setenv(JUDGE_MODEL_ENV_VAR, "gpt-5.6-luna")
    assert judge_model() == "gpt-5.6-luna"
    assert _make_judge().model == "gpt-5.6-luna"


def test_blank_judge_model_env_falls_back_to_the_default(monkeypatch):
    monkeypatch.setenv(JUDGE_MODEL_ENV_VAR, "   ")
    assert judge_model() == "gpt-4o"


def test_judge_scores_at_temperature_zero_by_default():
    judge = _make_judge()
    judge._client.chat.completions.create = MagicMock(return_value=_mock_response(1))

    judge.score(input="q", expected_output="e", actual_output="a")

    assert judge._client.chat.completions.create.call_args.kwargs["temperature"] == 0


def test_judge_retries_without_temperature_when_the_model_rejects_it(capsys):
    """gpt-5-family models reject temperature=0 outright:

        "Unsupported value: 'temperature' does not support 0 with this model.
         Only the default (1) value is supported."

    Without this fallback --judge-model gpt-5.6-luna is a trap that 400s on the first
    item. With it, the run proceeds -- but the judge is no longer deterministic, so it
    has to say so loudly rather than silently degrade the eval.
    """
    judge = _make_judge()
    calls = []

    def _create(**kwargs):
        calls.append(kwargs)
        if "temperature" in kwargs:
            raise Exception(
                "Error code: 400 - Unsupported value: 'temperature' does not support 0 "
                "with this model. Only the default (1) value is supported."
            )
        return _mock_response(1)

    judge._client.chat.completions.create = _create
    passed, _ = judge.score(input="q", expected_output="e", actual_output="a")

    assert passed is True
    assert len(calls) == 2
    assert "temperature" in calls[0] and "temperature" not in calls[1]
    warned = capsys.readouterr().out
    assert "not deterministic" in warned.lower()


def test_judge_remembers_the_model_rejects_temperature_and_stops_retrying():
    # One wasted 400 per run, not one per item.
    judge = _make_judge()
    calls = []

    def _create(**kwargs):
        calls.append(kwargs)
        if "temperature" in kwargs:
            raise Exception("Unsupported value: 'temperature' does not support 0 with this model.")
        return _mock_response(1)

    judge._client.chat.completions.create = _create
    for _ in range(3):
        judge.score(input="q", expected_output="e", actual_output="a")

    assert sum(1 for c in calls if "temperature" in c) == 1


def test_judge_reraises_errors_unrelated_to_temperature():
    judge = _make_judge()
    judge._client.chat.completions.create = MagicMock(side_effect=Exception("rate limit exceeded"))

    with pytest.raises(Exception, match="rate limit"):
        judge.score(input="q", expected_output="e", actual_output="a")


# --- Malformed judge responses must fail loudly, never score 0 -------------------------
#
# Every case below used to return ``(False, "")`` -- a confident "the agent was wrong"
# manufactured out of a response that carried no verdict at all. The failure mode is
# one-sided: it can only invent a 0, never a 1, so it biases every score downwards and
# is invisible in the report, which shows a plain failing item.


def test_judge_raises_when_the_model_returns_empty_content():
    """A reasoning model that burns its whole budget on reasoning tokens returns
    ``content=""`` with ``finish_reason="length"``. That is a truncated call, not a
    failing answer."""
    judge = _make_judge()
    judge._client.chat.completions.create = MagicMock(
        return_value=_mock_raw_response("", finish_reason="length", reasoning_tokens=2048)
    )

    with pytest.raises(JudgeResponseError) as err:
        judge.score(input="q", expected_output="42", actual_output="The answer is 42.")

    assert "empty" in str(err.value).lower()
    assert "finish_reason=length" in str(err.value)
    assert "reasoning_tokens=2048" in str(err.value)


def test_judge_raises_when_the_model_returns_no_content():
    judge = _make_judge()
    judge._client.chat.completions.create = MagicMock(return_value=_mock_raw_response(None))

    with pytest.raises(JudgeResponseError):
        judge.score(input="q", expected_output="e", actual_output="a")


def test_judge_raises_when_the_response_has_no_score_key():
    """Valid JSON, wrong schema -- ``{"verdict": 1}`` or a recased ``"Score"`` used to
    fall through to the default and score 0."""
    judge = _make_judge()
    judge._client.chat.completions.create = MagicMock(
        return_value=_mock_raw_response(json.dumps({"verdict": 1, "reasoning": "correct"}))
    )

    with pytest.raises(JudgeResponseError) as err:
        judge.score(input="q", expected_output="e", actual_output="a")

    assert "score" in str(err.value)
    assert "verdict" in str(err.value)  # the raw body is quoted back for diagnosis


def test_judge_raises_a_diagnosable_error_when_the_json_is_truncated():
    judge = _make_judge()
    judge._client.chat.completions.create = MagicMock(
        return_value=_mock_raw_response('{"score": 1, "reason', finish_reason="length")
    )

    with pytest.raises(JudgeResponseError) as err:
        judge.score(input="q", expected_output="e", actual_output="a")

    assert "finish_reason=length" in str(err.value)


# --- Diagnostics ----------------------------------------------------------------------


def test_judge_diagnostics_are_off_by_default(monkeypatch, capsys):
    # 18 items x 2 runs is 36 of these lines; they would bury the progress output.
    monkeypatch.delenv(JUDGE_DIAGNOSTICS_ENV_VAR, raising=False)
    judge = _make_judge()
    judge._client.chat.completions.create = MagicMock(return_value=_mock_response(1))

    judge.score(input="q", expected_output="e", actual_output="a")

    assert "[judge]" not in capsys.readouterr().out


def test_judge_logs_response_metadata_when_diagnostics_are_enabled(monkeypatch, capsys):
    """The forensic record for a flipped verdict: which endpoint answered, whether it
    was truncated, how many reasoning tokens it spent, and what it actually said."""
    monkeypatch.setenv(JUDGE_DIAGNOSTICS_ENV_VAR, "1")
    judge = _make_judge()
    judge._client.chat.completions.create = MagicMock(
        return_value=_mock_raw_response(
            json.dumps({"score": 1, "reasoning": "matches"}),
            finish_reason="stop",
            reasoning_tokens=128,
            fingerprint="fp_abc123",
        )
    )

    judge.score(input="q", expected_output="e", actual_output="a")

    out = capsys.readouterr().out
    assert "[judge]" in out
    assert "finish_reason=stop" in out
    assert "system_fingerprint=fp_abc123" in out
    assert "reasoning_tokens=128" in out
    assert "matches" in out  # the raw body, so a flipped verdict can be read back


def test_judge_diagnostics_survive_a_response_without_usage(monkeypatch, capsys):
    """Not every endpoint returns a usage block; diagnostics must not be the thing that
    breaks the run."""
    monkeypatch.setenv(JUDGE_DIAGNOSTICS_ENV_VAR, "1")
    judge = _make_judge()
    resp = _mock_raw_response(json.dumps({"score": 1, "reasoning": "ok"}))
    resp.usage = None

    judge._client.chat.completions.create = MagicMock(return_value=resp)
    passed, _ = judge.score(input="q", expected_output="e", actual_output="a")

    assert passed is True
    assert "[judge]" in capsys.readouterr().out


# --- The completion cap ---------------------------------------------------------------


def test_judge_caps_completion_tokens():
    """Unset, the cap is whatever the provider defaults to. A reasoning judge can spend
    that entire budget on hidden reasoning tokens and return an empty body, which is the
    truncation this cap exists to make deliberate rather than accidental."""
    judge = _make_judge()
    judge._client.chat.completions.create = MagicMock(return_value=_mock_response(1))

    judge.score(input="q", expected_output="e", actual_output="a")

    kwargs = judge._client.chat.completions.create.call_args.kwargs
    assert kwargs["max_completion_tokens"] == JUDGE_MAX_COMPLETION_TOKENS
    # max_tokens is the deprecated spelling and the gpt-5 family rejects it outright.
    assert "max_tokens" not in kwargs


def test_the_completion_cap_survives_the_temperature_fallback():
    """The retry that drops temperature must not also drop the cap."""
    judge = _make_judge()
    calls = []

    def _create(**kwargs):
        calls.append(kwargs)
        if "temperature" in kwargs:
            raise Exception("Unsupported value: 'temperature' does not support 0 with this model.")
        return _mock_response(1)

    judge._client.chat.completions.create = _create
    judge.score(input="q", expected_output="e", actual_output="a")

    assert calls[-1]["max_completion_tokens"] == JUDGE_MAX_COMPLETION_TOKENS


# --- Retrying an empty body -----------------------------------------------------------
#
# An empty body is a truncated call, not a verdict, and truncation is transient: the
# reasoning chain that overran the budget is resampled on the next attempt. Failing the
# whole item for it costs the item's remaining runs (runner.py returns early on error),
# so it is worth exactly one more request. Schema errors are NOT retried -- a model that
# answers with the wrong key answers with the wrong key again, and the retry would only
# double the cost of a prompt that needs fixing.


def test_judge_retries_once_when_the_body_comes_back_empty():
    judge = _make_judge()
    responses = [
        _mock_raw_response("", finish_reason="length", reasoning_tokens=4096),
        _mock_raw_response(json.dumps({"score": 1, "reasoning": "correct"})),
    ]
    judge._client.chat.completions.create = MagicMock(side_effect=responses)

    passed, reasoning = judge.score(input="q", expected_output="42", actual_output="The answer is 42.")

    assert passed is True
    assert reasoning == "correct"
    assert judge._client.chat.completions.create.call_count == 2


def test_judge_raises_when_the_retry_is_also_empty():
    judge = _make_judge()
    judge._client.chat.completions.create = MagicMock(
        return_value=_mock_raw_response("", finish_reason="length", reasoning_tokens=4096)
    )

    with pytest.raises(JudgeResponseError):
        judge.score(input="q", expected_output="e", actual_output="a")

    assert judge._client.chat.completions.create.call_count == 2


def test_judge_does_not_retry_a_schema_error():
    judge = _make_judge()
    judge._client.chat.completions.create = MagicMock(
        return_value=_mock_raw_response(json.dumps({"verdict": 1, "reasoning": "correct"}))
    )

    with pytest.raises(JudgeResponseError):
        judge.score(input="q", expected_output="e", actual_output="a")

    assert judge._client.chat.completions.create.call_count == 1


def test_judge_announces_the_retry(capsys):
    """A silently retried item is an item whose cost and latency doubled for no visible
    reason -- and a rising retry rate is the signal that the cap is too low."""
    judge = _make_judge()
    judge._client.chat.completions.create = MagicMock(
        side_effect=[
            _mock_raw_response("", finish_reason="length", reasoning_tokens=4096),
            _mock_response(1),
        ]
    )

    judge.score(input="q", expected_output="e", actual_output="a")

    out = capsys.readouterr().out
    assert "empty body" in out
    assert "retrying" in out.lower()


# --- an unreadable response must not escape as an untyped error (H4) ---


def _api_error(message: str, *, body: object) -> Exception:
    """An exception shaped like the openai SDK's APIStatusError.

    The SDK stringifies the whole response body into ``message`` (see
    ``_make_status_error_from_response``), which is exactly why the temperature check
    below cannot read ``str(exc)``.
    """

    class _APIError(Exception):
        pass

    exc = _APIError(f"Error code: 400 - {body}")
    exc.body = body  # type: ignore[attr-defined]
    exc.message = message  # type: ignore[attr-defined]
    return exc


def test_an_empty_choices_list_raises_a_judge_error_not_an_index_error():
    """Content filters and gateway error envelopes return `choices: []`.

    That is the commonest shape of an unreadable judge response, and `choices[0]` used to
    escape as a bare IndexError -- past the typed error this module exists to raise, with
    none of the body or metadata that makes the cause readable.
    """
    judge = _make_judge()
    judge._client.chat.completions.create.return_value = MagicMock(choices=[])

    with pytest.raises(JudgeResponseError) as err:
        judge.score(input="i", expected_output="e", actual_output="a")

    # The metadata has to say *why* there was no verdict, or the error is unactionable.
    assert "choices=0" in str(err.value)


def test_a_missing_message_content_raises_a_judge_error():
    judge = _make_judge()
    judge._client.chat.completions.create.return_value = MagicMock(choices=[MagicMock(message=MagicMock(content=None))])

    with pytest.raises(JudgeResponseError):
        judge.score(input="i", expected_output="e", actual_output="a")


# --- the temperature fallback must fire on temperature and nothing else (H3) ---


def test_a_structured_temperature_rejection_drops_the_parameter():
    """The real gpt-5 400 carries param="temperature". That is the signal we act on."""
    calls: list[dict] = []
    body = {
        "error": {
            "message": "Unsupported value: 'temperature' does not support 0 with this model.",
            "type": "invalid_request_error",
            "param": "temperature",
            "code": "unsupported_value",
        }
    }

    def create(**kwargs):
        calls.append(dict(kwargs))
        if "temperature" in kwargs:
            raise _api_error("Unsupported value: 'temperature' ...", body=body)
        return MagicMock(choices=[MagicMock(message=MagicMock(content='{"score": 1, "reasoning": "ok"}'))])

    judge = _make_judge(model="gpt-5.2")
    judge._client.chat.completions.create.side_effect = create
    passed, _ = judge.score(input="i", expected_output="e", actual_output="a")

    assert passed is True
    assert "temperature" in calls[0] and "temperature" not in calls[1]
    assert judge._supports_temperature is False


def test_a_400_that_echoes_the_request_is_not_read_as_a_temperature_rejection():
    """LiteLLM / vLLM style: the error body quotes the request that failed.

    That body contains the literal text `"temperature": 0`, so a substring check against
    `str(exc)` read a context-length overflow as a temperature rejection -- reporting the
    wrong cause, and then silently dropping temperature=0 from every later verdict, which
    is the one property that makes a judge reproducible.
    """
    body = {
        "error": {
            "message": "This model's maximum context length is 8192 tokens.",
            "type": "invalid_request_error",
            "code": "context_length_exceeded",
            "request": {"model": "gpt-4o", "temperature": 0, "max_completion_tokens": 4096},
        }
    }
    calls: list[dict] = []

    def create(**kwargs):
        calls.append(dict(kwargs))
        raise _api_error("This model's maximum context length is 8192 tokens.", body=body)

    judge = _make_judge()
    judge._client.chat.completions.create.side_effect = create

    with pytest.raises(Exception, match="context length"):
        judge.score(input="i", expected_output="e", actual_output="a")

    # The real error surfaced, exactly one request was spent, and determinism is intact.
    assert len(calls) == 1
    assert judge._supports_temperature is True


def test_the_eval_text_cannot_trigger_the_temperature_fallback():
    """A BI agent grading "average temperature by city" is an ordinary fixture.

    The word appearing in the graded content must not reconfigure the judge.
    """
    body = {"error": {"message": "Rate limit reached for gpt-4o.", "code": "rate_limit_exceeded"}}

    judge = _make_judge()
    judge._client.chat.completions.create.side_effect = _api_error("Rate limit reached for gpt-4o.", body=body)

    with pytest.raises(Exception, match="Rate limit"):
        judge.score(
            input="What is the average temperature by city?",
            expected_output="A temperature per city",
            actual_output="Prague averages 9.4 degrees",
        )

    assert judge._supports_temperature is True


# --- score_run: one run's judge fault is not the item's problem (H1) ---


def test_score_run_passes_a_readable_verdict_straight_through():
    judge = MagicMock()
    judge.model = "gpt-4o"
    judge.score.return_value = (True, "looks right")

    verdict = score_run(judge, input="i", expected_output="e", actual_output="a")

    assert (verdict.passed, verdict.reasoning, verdict.error) == (True, "looks right", None)


def test_score_run_turns_an_unreadable_verdict_into_an_unscored_run(capsys):
    """Not re-raised, and not scored 0 either.

    Raising discards every run already graded; scoring 0 is the silent FAIL
    JudgeResponseError exists to stop. The run is marked ungraded and the caller excludes
    it from pass@K.
    """
    judge = MagicMock()
    judge.model = "gpt-4o"
    judge.score.side_effect = JudgeResponseError("empty body twice")

    verdict = score_run(judge, input="i", expected_output="e", actual_output="a")

    assert verdict.passed is False
    assert verdict.error is not None and "empty body twice" in verdict.error
    # Announced: a rising rate of ungraded runs is the signal the judge needs attention.
    assert "could not grade one run" in capsys.readouterr().out


def test_score_run_does_not_swallow_errors_that_are_not_judge_faults():
    judge = MagicMock()
    judge.model = "gpt-4o"
    judge.score.side_effect = RuntimeError("network down")

    with pytest.raises(RuntimeError, match="network down"):
        score_run(judge, input="i", expected_output="e", actual_output="a")


# --- the score contract: only 0 and 1 are verdicts (H4's last gap) ---


def _score_body(body: str):
    judge = _make_judge()
    judge._client.chat.completions.create.return_value = MagicMock(choices=[MagicMock(message=MagicMock(content=body))])
    return judge.score(input="i", expected_output="e", actual_output="a")


@pytest.mark.parametrize("body", ['{"score": 2, "reasoning": "fully correct"}', '{"score": 0.9}', '{"score": -1}'])
def test_an_out_of_range_score_raises_instead_of_reporting_a_failure(body):
    """`int(score) == 1` was the last place an invented 0 survived: a model reading the
    rubric as 0-2, or answering with a confidence, landed here."""
    with pytest.raises(JudgeResponseError, match="out-of-range"):
        _score_body(body)


@pytest.mark.parametrize(("body", "expected"), [('{"score": "1"}', True), ('{"score": "0"}', False)])
def test_a_quoted_number_is_still_a_verdict(body, expected):
    """JSON mode quotes numbers routinely, and the pre-JudgeResponseError code accepted
    that via int() -- rejecting it now would throw away a verdict the judge did give."""
    passed, _ = _score_body(body)
    assert passed is expected


@pytest.mark.parametrize("score", ["1 (correct)", "probably correct"])
def test_judge_raises_when_the_score_is_not_a_number(score):
    """A score that float() cannot read is not a verdict, whether it merely decorates the
    number or replaces it outright."""
    with pytest.raises(JudgeResponseError, match="non-numeric") as err:
        _score_body(json.dumps({"score": score, "reasoning": "ok"}))

    assert score in str(err.value)  # the raw value is quoted back for diagnosis


@pytest.mark.parametrize(
    ("body", "expected"),
    [
        ('{"score": 1, "reasoning": "ok"}', True),
        ('{"score": 0, "reasoning": "no"}', False),
        # Booleans are verdicts too, not schema violations: JSON mode emits them.
        ('{"score": true}', True),
        ('{"score": false}', False),
    ],
)
def test_the_zero_and_one_verdicts_are_unchanged(body, expected):
    assert _score_body(body)[0] is expected
