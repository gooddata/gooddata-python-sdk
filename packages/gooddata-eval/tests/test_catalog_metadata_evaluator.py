# (C) 2026 GoodData Corporation
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.evaluators.catalog_metadata import CatalogMetadataEvaluator
from gooddata_eval.core.models import CatalogInput, ChatResult, DatasetItem


def _make_evaluator() -> CatalogMetadataEvaluator:
    with patch("openai.OpenAI"), patch.dict("os.environ", {"OPENAI_API_KEY": "sk-test"}):
        return CatalogMetadataEvaluator()


def _item(expected_output: dict, output: str = "description") -> DatasetItem:
    return DatasetItem(
        id="c1",
        dataset_name="d",
        test_kind="catalog_metadata",
        question="Description for the metric 'ARPU' (Net Sales / Active Customers)",
        expected_output=expected_output,
        catalog_input=CatalogInput.model_validate({"object_type": "Metric", "object_id": "arpu", "output": output}),
    )


def _chat(text: str, note: str | None = None) -> ChatResult:
    return ChatResult(text_response=text, raw_response={"note": note, "unusable_retries": 0})


def _judges(ev: CatalogMetadataEvaluator, positive: bool = True, violation: bool = False) -> MagicMock:
    """Script both judges; returns the positive judge's mock."""
    positive_score = MagicMock(return_value=(positive, "ok"))
    ev._positive_judge.score = positive_score
    ev._violation_judge.score = MagicMock(return_value=(violation, "ok"))
    return positive_score


def test_description_passes_format_and_criteria() -> None:
    ev = _make_evaluator()
    _judges(ev)
    res = ev.evaluate(
        _item({"must_include": ["a"], "must_not_include": ["x"]}),
        _chat("Average net sales per active customer. Use it to compare customer value."),
    )
    assert res.passed is True
    assert res.detail["max_sentences"] is True
    assert res.detail["no_ids"] is True


@pytest.mark.parametrize(
    ("text", "check"),
    [
        ("Revenue per customer. " * 30, "max_words"),
        ("Uses {metric/net_sales} divided by customers.", "no_ids"),
        ("Divides net_sales by active_customers.", "no_ids"),
        ("**Average** revenue per customer.", "no_markup"),
        ("The *average* revenue per customer.", "no_markup"),
        ("The _average_ revenue per customer.", "no_markup"),
        ("A. B. C. D. E.", "max_sentences"),
    ],
)
def test_description_format_checks_gate(text: str, check: str) -> None:
    ev = _make_evaluator()
    _judges(ev)
    res = ev.evaluate(_item({}), _chat(text))
    assert res.detail[check] is False
    assert res.passed is False


def test_title_checks() -> None:
    ev = _make_evaluator()
    _judges(ev)
    assert ev.evaluate(_item({}, output="title"), _chat("Average Revenue per Customer")).passed is True
    res = ev.evaluate(_item({}, output="title"), _chat("This metric shows average revenue."))
    assert res.detail["no_end_period"] is False
    assert res.passed is False


def test_format_override_switches_a_check_off() -> None:
    ev = _make_evaluator()
    _judges(ev)
    res = ev.evaluate(_item({"format": {"no_end_period": False}}, output="title"), _chat("Average revenue."))
    assert "no_end_period" not in res.detail
    assert res.passed is True


def test_empty_text_fails_without_judging() -> None:
    ev = _make_evaluator()
    positive_score = _judges(ev)
    res = ev.evaluate(_item({"must_include": ["a"]}), _chat(""))
    assert res.passed is False
    assert res.detail["generated"] is False
    positive_score.assert_not_called()


def test_a_note_next_to_a_text_fails() -> None:
    ev = _make_evaluator()
    _judges(ev)
    res = ev.evaluate(_item({}), _chat("Average revenue per customer.", note="Context was partial"))
    assert res.detail["no_note"] is False
    assert res.passed is False


@pytest.mark.parametrize(("text", "note", "passed"), [("", "Not found", True), ("", None, False), ("Text", "x", False)])
def test_expect_note_decides_alone(text: str, note: str | None, passed: bool) -> None:
    ev = _make_evaluator()
    positive_score = _judges(ev)
    res = ev.evaluate(_item({"expect_note": True, "must_include": ["a"]}), _chat(text, note))
    assert res.passed is passed
    positive_score.assert_not_called()


def test_violation_fails_the_item() -> None:
    ev = _make_evaluator()
    _judges(ev, violation=True)
    res = ev.evaluate(_item({"must_not_include": ["names a currency"]}), _chat("Price per unit in USD."))
    assert res.detail["exclude_0"] is False
    assert res.passed is False


@pytest.mark.parametrize(
    "expected",
    [
        {"format": {"bold_headline": True}},
        {"format": "x"},
        {"must_include": "a"},
        {"format": {"max_words": "10"}},
        {"format": {"max_words": True}},
        {"format": {"no_markup": "yes"}},
    ],
)
def test_validate_rejects_bad_expected_output(expected: dict) -> None:
    ev = _make_evaluator()
    with pytest.raises(ValueError):
        ev.evaluate(_item(expected), _chat("x"))


def test_snake_case_is_an_id_not_emphasis() -> None:
    ev = _make_evaluator()
    _judges(ev)
    res = ev.evaluate(_item({}), _chat("Uses net_sales over 2 * 3 periods."))
    assert res.detail["no_markup"] is True
    assert res.detail["no_ids"] is False
