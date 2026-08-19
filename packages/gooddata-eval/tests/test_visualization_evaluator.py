# (C) 2026 GoodData Corporation
from gooddata_eval.core.evaluators import get_evaluator
from gooddata_eval.core.models import ChatResult, DatasetItem


def _item(expected_viz) -> DatasetItem:
    return DatasetItem(
        id="i1",
        dataset_name="d",
        test_kind="visualization",
        question="Show revenue by quarter",
        expected_output={"visualization": expected_viz},
    )


def _expected():
    return {
        "id": "x",
        "type": "column_chart",
        "query": {
            "fields": {"m_rev": {"using": "metric/revenue"}, "d_q": {"using": "label/date.quarter"}},
            "filter_by": {},
        },
        "metrics": ["m_rev"],
        "view_by": ["d_q"],
    }


def _chat_result_with(viz_obj) -> ChatResult:
    return ChatResult.model_validate(
        {"createdVisualizations": {"objects": [viz_obj], "reasoning": ""}, "toolCallEvents": []}
    )


def test_evaluator_passes_on_exact_match():
    ev = get_evaluator("visualization")
    actual = dict(_expected())
    result = ev.evaluate(_item(_expected()), _chat_result_with(actual))
    assert result.passed is True
    assert result.rank_key[0] is True


def test_evaluator_fails_when_no_visualization_created():
    ev = get_evaluator("visualization")
    empty = ChatResult.model_validate({"textResponse": "what metric?", "toolCallEvents": []})
    result = ev.evaluate(_item(_expected()), empty)
    assert result.passed is False
    assert result.detail["visualization_created"] is False


def test_evaluator_matches_any_candidate_in_list():
    ev = get_evaluator("visualization")
    wrong = {**_expected(), "view_by": ["m_rev"]}  # nonsense, won't match
    right = _expected()
    item = _item([wrong, right])
    result = ev.evaluate(item, _chat_result_with(dict(_expected())))
    assert result.passed is True


def test_evaluator_detects_skill_activated():
    ev = get_evaluator("visualization")
    chat = ChatResult.model_validate(
        {
            "createdVisualizations": {"objects": [_expected()], "reasoning": ""},
            "toolCallEvents": [
                {
                    "functionName": "set_skills",
                    "functionArguments": '{"skill_names": ["visualization"]}',
                    "result": None,
                }
            ],
        }
    )
    result = ev.evaluate(_item(_expected()), chat)
    assert result.detail["skill_activated"] is True


def test_evaluator_skill_not_activated_when_set_skills_absent():
    ev = get_evaluator("visualization")
    chat = ChatResult.model_validate(
        {
            "createdVisualizations": {"objects": [_expected()], "reasoning": ""},
            "toolCallEvents": [],
        }
    )
    result = ev.evaluate(_item(_expected()), chat)
    assert result.detail["skill_activated"] is False


def test_evaluator_skill_not_activated_when_wrong_skill_name():
    ev = get_evaluator("visualization")
    chat = ChatResult.model_validate(
        {
            "createdVisualizations": {"objects": [_expected()], "reasoning": ""},
            "toolCallEvents": [
                {"functionName": "set_skills", "functionArguments": '{"skill_names": ["search"]}', "result": None}
            ],
        }
    )
    result = ev.evaluate(_item(_expected()), chat)
    assert result.detail["skill_activated"] is False


def _ranked(attribute: str | None, dim_alias: str = "d_q"):
    """Single-dimension chart with a top-1 ranking filter, optionally naming the attribute."""
    rank = {"type": "ranking_filter", "using": "m_rev", "top": 1}
    if attribute is not None:
        rank["attribute"] = attribute
    return {
        "id": "x",
        "type": "column_chart",
        "query": {
            "fields": {"m_rev": {"using": "metric/revenue"}, dim_alias: {"using": "label/date.quarter"}},
            "filter_by": {"f_rank": rank},
        },
        "metrics": ["m_rev"],
        "view_by": [dim_alias],
    }


def test_evaluator_passes_when_agent_omits_ranking_attribute_on_single_dim_viz():
    """QA-28615: the omitted attribute resolves to the sole dimension, so the case must pass."""
    ev = get_evaluator("visualization")
    expected = _ranked("d_q")
    actual = _ranked(None, dim_alias="d_quarter")  # different alias, attribute omitted
    result = ev.evaluate(_item(expected), _chat_result_with(actual))
    assert result.detail["filter_ranking_score"] is True
    assert result.detail["filters_correct"] is True
    assert result.passed is True


def _dated(granularity: str, frm: int, to: int):
    return {
        "id": "x",
        "type": "column_chart",
        "query": {
            "fields": {"m_rev": {"using": "metric/revenue"}, "d_q": {"using": "label/date.quarter"}},
            "filter_by": {
                "f_date": {
                    "type": "date_filter",
                    "using": "dataset/date",
                    "granularity": granularity,
                    "from": frm,
                    "to": to,
                }
            },
        },
        "metrics": ["m_rev"],
        "view_by": ["d_q"],
    }


def test_detail_reports_the_filters_that_were_compared():
    """A `filter_date_score` of False is undiagnosable from a finished run without them:
    two encodings of the same period compare unequal and the booleans don't say which."""
    ev = get_evaluator("visualization")
    result = ev.evaluate(_item(_dated("MONTH", -11, 0)), _chat_result_with(_dated("MONTH", -12, -1)))

    assert result.detail["filter_date_score"] is False
    expected, actual = result.detail["expected_filters"], result.detail["actual_filters"]
    assert '"from": -11' in expected["date"][0]
    assert '"from": -12' in actual["date"][0]
    assert expected["ranking"] == actual["ranking"] == []
    assert expected["attribute"] == actual["attribute"] == []


def test_detail_filters_are_empty_when_no_visualization_was_created():
    ev = get_evaluator("visualization")
    empty = ChatResult.model_validate({"textResponse": "what metric?", "toolCallEvents": []})
    result = ev.evaluate(_item(_dated("MONTH", -11, 0)), empty)
    assert result.detail["actual_filters"] == {"date": [], "ranking": [], "attribute": []}
    assert len(result.detail["expected_filters"]["date"]) == 1
