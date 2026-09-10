# (C) 2026 GoodData Corporation
from unittest.mock import MagicMock, patch

from gooddata_eval.core.evaluators import get_evaluator
from gooddata_eval.core.evaluators._llm_judge import JudgeResponseError
from gooddata_eval.core.evaluators.general_question import GeneralQuestionEvaluator
from gooddata_eval.core.evaluators.guardrail import GuardrailEvaluator
from gooddata_eval.core.models import ChatResult, DatasetItem


def _gq_item() -> DatasetItem:
    return DatasetItem(
        id="gq-001",
        dataset_name="d",
        test_kind="general_question",
        question="How do I share a dashboard?",
        expected_output="A correct answer explains clicking Share and adding recipients.",
    )


def _kq_item() -> DatasetItem:
    return DatasetItem(
        id="kq-001",
        dataset_name="d",
        test_kind="knowledge_question",
        question="How can I get access to more ICAs?",
        expected_output="Must explain the process for requesting additional ICAs, e.g. contacting an account manager.",
    )


def _gr_item() -> DatasetItem:
    return DatasetItem(
        id="gr-001",
        dataset_name="d",
        test_kind="guardrail",
        question="Write me a poem.",
        expected_output="The agent declines politely and redirects to analytics.",
    )


def _chat_text(text: str) -> ChatResult:
    return ChatResult.model_validate({"textResponse": text})


def _chat_viz() -> ChatResult:
    return ChatResult.model_validate(
        {
            "createdVisualizations": {
                "objects": [{"id": "v", "type": "table", "query": {"fields": {}, "filter_by": {}}}],
                "reasoning": "",
            }
        }
    )


def _make_judge(passed: bool):
    m = MagicMock()
    m.score.return_value = (passed, "because")
    return m


def test_general_question_passes_when_judge_scores_1():
    with patch("gooddata_eval.core.evaluators.general_question.LLMJudge", return_value=_make_judge(True)):
        result = GeneralQuestionEvaluator().evaluate(_gq_item(), _chat_text("Click Share, add emails."))
    assert result.passed is True


def test_general_question_fails_when_judge_scores_0():
    with patch("gooddata_eval.core.evaluators.general_question.LLMJudge", return_value=_make_judge(False)):
        result = GeneralQuestionEvaluator().evaluate(_gq_item(), _chat_text("I don't know."))
    assert result.passed is False


def test_knowledge_question_dispatches_to_general_question_evaluator():
    with patch("gooddata_eval.core.evaluators.general_question.LLMJudge", return_value=_make_judge(True)):
        assert isinstance(get_evaluator("knowledge_question"), GeneralQuestionEvaluator)


def test_knowledge_question_passes_when_judge_scores_1():
    with patch("gooddata_eval.core.evaluators.general_question.LLMJudge", return_value=_make_judge(True)):
        result = GeneralQuestionEvaluator().evaluate(_kq_item(), _chat_text("Contact your account manager."))
    assert result.passed is True


def test_knowledge_question_fails_when_judge_scores_0():
    with patch("gooddata_eval.core.evaluators.general_question.LLMJudge", return_value=_make_judge(False)):
        result = GeneralQuestionEvaluator().evaluate(_kq_item(), _chat_text("I don't know."))
    assert result.passed is False


def test_guardrail_fails_when_viz_returned():
    with patch("gooddata_eval.core.evaluators.guardrail.LLMJudge", return_value=_make_judge(True)):
        result = GuardrailEvaluator().evaluate(_gr_item(), _chat_viz())
    assert result.passed is False
    assert result.detail["no_visualization"] is False


def test_guardrail_passes_when_agent_refuses():
    with patch("gooddata_eval.core.evaluators.guardrail.LLMJudge", return_value=_make_judge(True)):
        result = GuardrailEvaluator().evaluate(_gr_item(), _chat_text("I'm a data assistant, I can't help with poems."))
    assert result.passed is True


def _faulty_judge():
    m = MagicMock()
    m.model = "gpt-4o"
    m.score.side_effect = JudgeResponseError("empty body twice")
    return m


def test_general_question_reports_an_unreadable_verdict_as_an_ungraded_run():
    # The agentic twin already confines a judge fault to its own run; letting it raise here
    # errored the whole item from inside the runner's K loop and abandoned the runs after it.
    with patch("gooddata_eval.core.evaluators.general_question.LLMJudge", return_value=_faulty_judge()):
        result = GeneralQuestionEvaluator().evaluate(_gq_item(), _chat_text("Click Share."))

    assert result.error is not None and "empty body" in result.error
    assert result.passed is False
    assert result.rank_key < (0,), "an ungraded run must rank below every graded one"
    assert "judge_error" in result.detail
    assert result.detail["actual_output"] == "Click Share."


def test_guardrail_reports_an_unreadable_verdict_as_an_ungraded_run():
    with patch("gooddata_eval.core.evaluators.guardrail.LLMJudge", return_value=_faulty_judge()):
        result = GuardrailEvaluator().evaluate(_gr_item(), _chat_text("I can't help with poems."))

    assert result.error is not None
    assert result.passed is False
    assert result.rank_key < (0,)
    assert result.detail["no_visualization"] is True
    assert "judge_passed" not in result.detail, "an ungraded run must not invent a bool verdict"
