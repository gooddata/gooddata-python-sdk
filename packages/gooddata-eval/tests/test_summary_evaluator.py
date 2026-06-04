# (C) 2026 GoodData Corporation
from unittest.mock import MagicMock, patch

from gooddata_eval.core.evaluators.summary import DashboardSummaryEvaluator
from gooddata_eval.core.models import ChatResult, DatasetItem


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
    ev._negative_judge.score = MagicMock(return_value=(True, "avoided"))

    item = _item({"must_include": ["a", "b"], "must_not_include": ["x"], "rubric": ["r"]})
    res = ev.evaluate(item, _chat())

    assert res.passed is True
    # 4 bool checks, all True -> quality 1.0
    assert res.rank_key == (1, 1.0)


def test_fails_when_must_not_include_violated():
    ev = _make_evaluator()
    ev._positive_judge.score = MagicMock(return_value=(True, "ok"))
    ev._negative_judge.score = MagicMock(return_value=(False, "hallucinated a number"))

    item = _item({"must_include": ["a"], "must_not_include": ["x"]})
    res = ev.evaluate(item, _chat())

    assert res.passed is False
    # include_0 True, exclude_0 False -> quality 0.5
    assert res.rank_key == (0, 0.5)


def test_fails_when_a_must_include_is_missing():
    ev = _make_evaluator()
    ev._positive_judge.score = MagicMock(side_effect=[(True, "ok"), (False, "missing")])
    ev._negative_judge.score = MagicMock(return_value=(True, "avoided"))

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
