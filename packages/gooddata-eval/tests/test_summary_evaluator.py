# (C) 2026 GoodData Corporation
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.evaluators._llm_judge import JudgeResponseError
from gooddata_eval.core.evaluators.summary import DashboardSummaryEvaluator
from gooddata_eval.core.models import ChatResult, DatasetItem


def _next_verdict(it):
    """Next scripted judge result, raising it if it is an exception."""
    v = next(it)
    if isinstance(v, Exception):
        raise v
    return v


def _make_evaluator():
    with patch("openai.OpenAI"), patch.dict("os.environ", {"OPENAI_API_KEY": "sk-test"}):
        return DashboardSummaryEvaluator()


def _item(expected_output) -> DatasetItem:
    return DatasetItem(
        id="s1",
        dataset_name="d",
        test_kind="dashboard_summary",
        question="Summarize the dashboard",
        expected_output=expected_output,
    )


def _chat(text: str = "Revenue grew QoQ; West is the top region.") -> ChatResult:
    return ChatResult.model_validate({"textResponse": text})


def test_passes_when_all_criteria_satisfied():
    ev = _make_evaluator()
    ev._positive_judge.score = MagicMock(return_value=(True, "ok"))
    ev._violation_judge.score = MagicMock(return_value=(False, "characteristic absent"))

    item = _item({"must_include": ["a", "b"], "must_not_include": ["x"], "rubric": ["r"]})
    res = ev.evaluate(item, _chat())

    assert res.passed is True
    # 4 bool checks, all True -> quality 1.0
    assert res.rank_key == (1, 1.0)


def test_fails_when_must_not_include_violated():
    ev = _make_evaluator()
    ev._positive_judge.score = MagicMock(return_value=(True, "ok"))
    # violation judge detects the forbidden characteristic is present -> avoided=False
    ev._violation_judge.score = MagicMock(return_value=(True, "has a separate filter section"))

    item = _item({"must_include": ["a"], "must_not_include": ["x"]})
    res = ev.evaluate(item, _chat())

    assert res.passed is False
    # include_0 True, exclude_0 False -> quality 0.5
    assert res.rank_key == (0, 0.5)


def test_fails_when_a_must_include_is_missing():
    ev = _make_evaluator()
    ev._positive_judge.score = MagicMock(side_effect=[(True, "ok"), (False, "missing")])
    ev._violation_judge.score = MagicMock(return_value=(False, "characteristic absent"))

    item = _item({"must_include": ["a", "b"]})
    res = ev.evaluate(item, _chat())

    assert res.passed is False
    assert res.rank_key == (0, 0.5)


def test_rubric_does_not_gate_pass_but_lowers_quality():
    ev = _make_evaluator()
    # must_include passes; rubric fails.
    ev._positive_judge.score = MagicMock(side_effect=[(True, "ok"), (False, "weak")])

    item = _item({"must_include": ["a"], "rubric": ["nice prose"]})
    res = ev.evaluate(item, _chat())

    assert res.passed is True  # rubric failure does not fail the item
    assert res.rank_key == (1, 0.5)  # but quality reflects it


def test_non_dict_expected_output_is_single_rubric_criterion():
    ev = _make_evaluator()
    ev._positive_judge.score = MagicMock(return_value=(True, "ok"))

    item = _item("A good summary mentions the overall revenue trend.")
    res = ev.evaluate(item, _chat())

    assert res.passed is True
    assert res.rank_key == (1, 1.0)
    ev._positive_judge.score.assert_called_once()


# --- one unreadable judge body must not cost every other criterion ---


def test_one_ungraded_criterion_does_not_discard_the_ones_already_graded():
    """dashboard_summary makes ONE judge request PER CRITERION.

    Letting JudgeResponseError raise out of the loop discarded every criterion already
    graded and abandoned the ones after it -- a 4-criterion item losing all 4 to one bad
    body, ending as runs=0 with an empty best_detail, and dropping out of
    avg_quality_score's denominator entirely while the CLI still exited 0.
    """
    ev = _make_evaluator()
    verdicts = iter([(True, "ok"), JudgeResponseError("empty body twice"), (True, "ok")])
    ev._positive_judge.score = MagicMock(side_effect=lambda *a, **k: _next_verdict(verdicts))
    ev._violation_judge.score = MagicMock(return_value=(False, "characteristic absent"))

    item = _item({"must_include": ["a", "b"], "must_not_include": ["x"], "rubric": ["r"]})
    res = ev.evaluate(item, _chat())

    # include_0 graded True, include_1 ungraded, exclude_0 graded True, rubric_0 graded True.
    assert res.detail["include_0"] is True
    assert "include_1" not in res.detail, "an ungraded criterion must not be stored as a bool"
    assert "UNGRADED" in res.detail["include_1_reason"]
    assert res.detail["exclude_0"] is True
    assert res.detail["rubric_0"] is True
    assert res.detail["ungraded_criteria"] == 1
    # An ungraded criterion is not a failed one, so it neither fails the item nor lands in
    # the quality denominator: 3 graded checks, all True.
    assert res.passed is True
    assert res.rank_key == (1, 1.0)


def test_an_ungraded_criterion_still_cannot_mask_a_real_failure():
    ev = _make_evaluator()
    verdicts = iter([(False, "missing"), JudgeResponseError("unparseable JSON")])
    ev._positive_judge.score = MagicMock(side_effect=lambda *a, **k: _next_verdict(verdicts))

    item = _item({"must_include": ["a", "b"]})
    res = ev.evaluate(item, _chat())

    assert res.passed is False
    assert res.rank_key == (0, 0.0)


def test_an_item_with_no_gradeable_criterion_raises():
    # Nothing was assessed, so `passed` would still be its initial True -- a pass nobody
    # made. That is an error, not a result.
    ev = _make_evaluator()
    ev._positive_judge.score = MagicMock(side_effect=JudgeResponseError("empty body twice"))

    item = _item({"must_include": ["a", "b"]})

    with pytest.raises(JudgeResponseError, match="no readable verdict for any of the 2 criterion"):
        ev.evaluate(item, _chat())
