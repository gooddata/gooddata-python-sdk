# (C) 2026 GoodData Corporation
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.evaluators import get_evaluator, supported_test_kinds
from gooddata_eval.core.evaluators.takeaway import (
    DEFAULT_MUST_INCLUDE,
    DEFAULT_MUST_NOT_INCLUDE,
    DocumentTakeawayEvaluator,
    _sentences,
)
from gooddata_eval.core.models import ChatResult, DatasetItem, TakeawayInput

_GOOD = "**Growth now comes from new markets.** Sales rose again this period, led by the Nordics, while core markets held flat."


def _make_evaluator(*, judge_passes: bool = True) -> DocumentTakeawayEvaluator:
    """An evaluator whose judges grade every criterion as satisfied (or every one as not)."""
    with patch("openai.OpenAI"), patch.dict("os.environ", {"OPENAI_API_KEY": "sk-test"}):
        ev = DocumentTakeawayEvaluator()
    ev._positive_judge.score = MagicMock(return_value=(judge_passes, "positive"))
    ev._violation_judge.score = MagicMock(return_value=(not judge_passes, "violation"))
    return ev


def _item(expected_output: Any = None, *, max_characters: int | None = None) -> DatasetItem:
    return DatasetItem(
        id="t1",
        dataset_name="d",
        test_kind="document_takeaway",
        question="P01 default format, Sales page",
        expected_output=expected_output if expected_output is not None else {},
        takeaway_input=TakeawayInput(visualizations=["v1"], max_characters=max_characters),
    )


def _chat(text: str | None = _GOOD, *, no_data: bool = False) -> ChatResult:
    raw = {"takeaway": text, "noData": no_data, "agentId": "a", "contextOmitted": []}
    return ChatResult(text_response=text or "", raw_response=raw)


def _judge_calls(ev: DocumentTakeawayEvaluator) -> int:
    return ev._positive_judge.score.call_count + ev._violation_judge.score.call_count


def test_good_takeaway_passes_every_check() -> None:
    res = _make_evaluator().evaluate(_item(), _chat())

    assert res.passed is True
    assert res.error is None
    for key in (
        "word_budget",
        "headline_words",
        "max_sentences",
        "single_paragraph",
        "bold_headline",
        "no_headings",
        "no_lists",
        "no_ids",
        "no_meta",
    ):
        assert res.detail[key] is True, key


def test_word_count_scores_reported() -> None:
    res = _make_evaluator().evaluate(_item(), _chat())

    assert res.detail["word_count"] == 20
    assert res.detail["headline_word_count"] == 6


def test_word_budget_ignores_large_max_characters() -> None:
    text = "**Sales grew.** " + " ".join(["word"] * 53) + "."

    res = _make_evaluator().evaluate(_item(max_characters=1000), _chat(text))

    assert res.detail["word_count"] == 55
    assert res.detail["word_budget"] is False
    assert res.detail["length"] is True
    assert res.passed is False


def test_headline_over_ten_words_fails() -> None:
    text = "**Sales in every region grew faster than any other metric this time.** Margins held."

    res = _make_evaluator().evaluate(_item(), _chat(text))

    assert res.detail["headline_word_count"] == 12
    assert res.detail["headline_words"] is False
    assert res.passed is False


@pytest.mark.parametrize(
    ("body", "count"),
    [
        ("Sales rose 3% vs. last period. Nordics led.", 2),
        ("U.S. sales grew. Europe held flat.", 2),
        ("Prodeje rostly, např. v Praze. Brno stagnovalo.", 2),
        ("Prodeje rostly. Živé kanály stagnovaly.", 2),
        ("Sales rose **sharply.** Orders fell. Returns grew.", 3),
        ('Sales are "flat." Orders rose.', 2),
        ("Margins held at 3.5% overall.", 1),
        ("Sales grew. 2 regions lead.", 2),
        ("Sales grew", 1),
        ("Online outgrew retail vs. Europe in 2024.", 1),
        ("Sales stay below vs. 2024 levels.", 1),
        ("Growth came from new markets, e.g. Nordics. Core held.", 2),
        ("Tržby rostly, tj. Praha vedla. Brno stagnovalo.", 2),
        ("Sales grew (cca. 5 regions). Core held.", 2),
        ("... Sales grew.", 2),
        ("", 0),
        ("  ** **  ", 0),
    ],
)
def test_sentence_count(body: str, count: int) -> None:
    assert _sentences(body) == count


def test_bold_inside_the_body_still_counts_as_a_break() -> None:
    res = _make_evaluator().evaluate(
        _item(), _chat("**Sales grew.** Sales rose **sharply.** Orders fell. Returns grew.")
    )

    assert res.detail["max_sentences"] is False


@pytest.mark.parametrize(
    ("text", "ok"),
    [
        ("**Sales grew.** Margins held. Costs fell.", True),
        ("**Sales grew.** Margins held. Costs fell. Returns rose.", False),
        ("**Total is $4.2M.** Margins held at 3.5% overall.", True),
    ],
)
def test_max_sentences_counts_after_the_headline(text: str, ok: bool) -> None:
    res = _make_evaluator().evaluate(_item(), _chat(text))

    assert res.detail["max_sentences"] is ok


def test_max_sentences_counts_whole_text_without_headline() -> None:
    res = _make_evaluator().evaluate(
        _item({"format": {"bold_headline": False, "max_sentences": 1}}), _chat("Sales grew. Margins held.")
    )

    assert res.detail["max_sentences"] is False
    assert "bold_headline" not in res.detail
    assert "headline_words" not in res.detail
    assert res.detail["headline_word_count"] == 0


@pytest.mark.parametrize(
    ("text", "ok"),
    [
        (_GOOD, True),
        ("**Sales grew.**\nMargins held.", True),
        ("**Sales grew.**\n\nMargins held.", False),
        ("**Sales grew.**\nMargins held.\nCosts fell.", False),
    ],
)
def test_single_paragraph(text: str, ok: bool) -> None:
    res = _make_evaluator().evaluate(_item(), _chat(text))

    assert res.detail["single_paragraph"] is ok


@pytest.mark.parametrize(("limit", "ok"), [(len(_GOOD), True), (len(_GOOD) - 1, False)])
def test_length_within_max_characters(limit: int, ok: bool) -> None:
    res = _make_evaluator().evaluate(_item(max_characters=limit), _chat())

    assert res.detail["length"] is ok


def test_length_not_checked_without_max_characters() -> None:
    res = _make_evaluator().evaluate(_item(), _chat())

    assert "length" not in res.detail


@pytest.mark.parametrize(
    ("text", "ok"),
    [
        (_GOOD, True),
        ("  **Sales grew.** Margins held.", True),
        ("Sales grew. **Margins held.**", False),
        ("Sales grew and margins held.", False),
    ],
)
def test_bold_headline(text: str, ok: bool) -> None:
    res = _make_evaluator().evaluate(_item(), _chat(text))

    assert res.detail["bold_headline"] is ok


@pytest.mark.parametrize(
    ("text", "ok"),
    [
        (_GOOD, True),
        ("## Sales grew\nMargins held.", False),
        ("# Sales grew\nMargins held.", False),
        ("#1 seller holds the lead.", True),
        ("**Sales grew.**\n#2 brand closes the gap.", True),
    ],
)
def test_no_headings(text: str, ok: bool) -> None:
    res = _make_evaluator().evaluate(_item(), _chat(text))

    assert res.detail["no_headings"] is ok


@pytest.mark.parametrize(
    ("text", "ok"),
    [
        (_GOOD, True),
        ("**Sales grew.**\n- Margins held.", False),
        ("**Sales grew.**\n• Margins held.", False),
        ("**Sales grew.**\n1. Margins held.", False),
        ("**Sales grew.**\n2) Margins held.", False),
    ],
)
def test_no_lists(text: str, ok: bool) -> None:
    res = _make_evaluator().evaluate(_item(), _chat(text))

    assert res.detail["no_lists"] is ok


def test_format_override_allows_lists() -> None:
    text = "- Sales grew.\n- Margins held.\n- Costs fell."
    fmt = {"no_lists": False, "bold_headline": False, "max_sentences": None, "single_paragraph": False}

    res = _make_evaluator().evaluate(_item({"format": fmt}), _chat(text))

    assert "no_lists" not in res.detail
    assert "max_sentences" not in res.detail
    assert "single_paragraph" not in res.detail
    assert res.detail["word_budget"] is True
    assert res.passed is True


@pytest.mark.parametrize(
    ("limit", "check"),
    [("max_words", "word_budget"), ("max_headline_words", "headline_words"), ("max_sentences", "max_sentences")],
)
@pytest.mark.parametrize("off", [None, False])
def test_format_limit_switched_off(limit: str, check: str, off: bool | None) -> None:
    res = _make_evaluator().evaluate(_item({"format": {limit: off}}), _chat())

    assert check not in res.detail
    assert res.passed is True


@pytest.mark.parametrize(
    ("text", "ok"),
    [
        (_GOOD, True),
        ("**Sales grew.** Driven by 25bdccd8-ef39-40a5-a224-6031d0ab470c.", False),
        ("**Sales grew.** Driven by {metric/revenue}.", False),
        ("**Sales grew.** Led by label.region.name values.", False),
        ("**Sales grew.** The label. Margins held.", True),
    ],
)
def test_no_ids(text: str, ok: bool) -> None:
    res = _make_evaluator().evaluate(_item(), _chat(text))

    assert res.detail["no_ids"] is ok


@pytest.mark.parametrize(
    ("text", "ok"),
    [
        (_GOOD, True),
        ("**Summary:** Sales grew.", False),
        ("**Key takeaways** Sales grew.", False),
        ("**Sales grew.** Based on the data, margins held.", False),
        ("This chart shows sales growing.", False),
        ("**Sales grew.**\nVisualization metadata says margins held.", False),
        ("**Sales grew.** The quarterly summary confirms it.", True),
    ],
)
def test_no_meta(text: str, ok: bool) -> None:
    res = _make_evaluator().evaluate(_item(), _chat(text))

    assert res.detail["no_meta"] is ok


def test_no_data_expected_and_returned_passes_without_judge() -> None:
    ev = _make_evaluator()

    res = ev.evaluate(_item({"no_data": True}), _chat(None, no_data=True))

    assert res.passed is True
    assert res.detail["no_data"] is True
    assert _judge_calls(ev) == 0
    assert "word_budget" not in res.detail


@pytest.mark.parametrize(
    ("expected", "text", "no_data"),
    [(False, None, True), (True, _GOOD, False), (True, _GOOD, True)],
)
def test_no_data_mismatch_fails(expected: bool, text: str | None, no_data: bool) -> None:
    ev = _make_evaluator()

    res = ev.evaluate(_item({"no_data": expected}), _chat(text, no_data=no_data))

    assert res.passed is False
    assert res.detail["no_data"] is False
    assert _judge_calls(ev) == 0


def test_deterministic_failure_still_grades_the_judge_criteria() -> None:
    ev = _make_evaluator()

    res = ev.evaluate(_item(), _chat("Sales grew and margins held."))

    assert res.passed is False
    assert _judge_calls(ev) == len(DEFAULT_MUST_INCLUDE) + len(DEFAULT_MUST_NOT_INCLUDE)


def test_judge_violation_fails_the_item() -> None:
    res = _make_evaluator(judge_passes=False).evaluate(_item(), _chat())

    assert res.passed is False
    assert res.detail["default_exclude_exact_figure"] is False
    assert res.detail["default_include_one_finding"] is False


def test_default_rules_added_unless_disabled() -> None:
    ev = _make_evaluator()
    res = ev.evaluate(_item({"must_include": ["is about returning customers"]}), _chat())

    assert ev._positive_judge.score.call_count == len(DEFAULT_MUST_INCLUDE) + 1
    assert ev._violation_judge.score.call_count == len(DEFAULT_MUST_NOT_INCLUDE)
    assert res.detail["include_0"] is True
    assert all(f"default_exclude_{key}" in res.detail for key in DEFAULT_MUST_NOT_INCLUDE)

    ev = _make_evaluator()
    res = ev.evaluate(_item({"default_rules": False, "must_not_include": ["mentions a campaign"]}), _chat())

    assert _judge_calls(ev) == 1
    assert res.detail["exclude_0"] is True
    assert not any(key.startswith("default_") for key in res.detail)


def test_item_criteria_are_judged_against_the_takeaway() -> None:
    ev = _make_evaluator()
    ev.evaluate(_item({"default_rules": False, "rubric": ["plain language"]}), _chat())

    ev._positive_judge.score.assert_called_once_with(
        input="P01 default format, Sales page", expected_output="plain language", actual_output=_GOOD
    )


def test_title_number_criterion_text_present() -> None:
    criterion = DEFAULT_MUST_NOT_INCLUDE["exact_figure"]

    assert "Top 10" in criterion
    assert "in digits" in criterion
    assert "'about $270M'" in criterion
    assert "'about a third'" in criterion
    assert "'roughly doubled'" in criterion


def test_calibrated_criterion_wording() -> None:
    assert set(DEFAULT_MUST_NOT_INCLUDE) == {
        "executive_summary",
        "chart_walkthrough",
        "background_opener",
        "exact_figure",
        "date_or_period",
        "unshown_cause",
        "chart_description",
    }
    assert "Things to watch" in DEFAULT_MUST_NOT_INCLUDE["executive_summary"]
    assert "led by" in DEFAULT_MUST_NOT_INCLUDE["unshown_cause"]
    assert set(DEFAULT_MUST_INCLUDE) == {"one_finding"}


def test_registered_as_lazy_llm_judge_kind() -> None:
    assert "document_takeaway" in supported_test_kinds()
    with patch("openai.OpenAI"), patch.dict("os.environ", {"OPENAI_API_KEY": "sk-test"}):
        assert isinstance(get_evaluator("document_takeaway"), DocumentTakeawayEvaluator)


def test_no_data_not_stored_as_a_bool_when_a_takeaway_is_expected() -> None:
    res = _make_evaluator().evaluate(_item(), _chat())

    assert not isinstance(res.detail.get("no_data"), bool)


def test_unknown_format_key_is_rejected() -> None:
    with pytest.raises(ValueError, match="max_sentence"):
        _make_evaluator().evaluate(_item({"format": {"max_sentence": 1}}), _chat())


def test_validate_rejects_an_unknown_format_key_without_a_judge_call() -> None:
    ev = _make_evaluator()

    with pytest.raises(ValueError, match="'t1'.*max_sentence"):
        ev.validate(_item({"format": {"max_sentence": 1}}))

    assert _judge_calls(ev) == 0


def test_validate_rejects_a_format_that_is_not_an_object() -> None:
    with pytest.raises(ValueError, match="'t1'.*format must be a JSON object"):
        _make_evaluator().validate(_item({"format": ["no_lists"]}))


@pytest.mark.parametrize("key", ["must_include", "must_not_include", "rubric"])
@pytest.mark.parametrize("value", [None, "one criterion", {"a": "b"}])
def test_validate_rejects_criteria_that_are_not_a_list(key: str, value: Any) -> None:
    with pytest.raises(ValueError, match=f"'t1'.*{key} must be a JSON array"):
        _make_evaluator().validate(_item({key: value}))


def test_validate_accepts_absent_and_empty_criteria() -> None:
    ev = _make_evaluator()
    ev.validate(_item({}))
    ev.validate(_item({"must_include": [], "must_not_include": [], "rubric": []}))


def test_validate_accepts_a_valid_item() -> None:
    _make_evaluator().validate(_item({"format": {"no_lists": False}, "must_include": ["x"]}))
