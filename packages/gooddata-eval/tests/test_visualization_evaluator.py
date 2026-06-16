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
