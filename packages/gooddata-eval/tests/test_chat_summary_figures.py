# (C) 2026 GoodData Corporation
from __future__ import annotations

import json
from typing import Any

import pytest
from gooddata_eval.core.agentic import chat_summary as kind
from gooddata_eval.core.evaluators.chat_summary_figures import (
    check_figures,
    tables_from_tool_calls,
    tables_from_tool_result,
)
from gooddata_eval.core.models import ChatResult, ToolCallEvent

MONEY = "[>=1000000]$#,,.0 M;[>=1000]$#,.0 K;$#,##0"


def _xtab(columns: list[tuple[str, str]], labels: list[list[str]], data: list[list[float]], **extra: Any) -> str:
    """A tool result as `execute_existing_visualizations` returns it."""
    cols = [{"name": n, "type": t, **({"format": MONEY} if t == "metric" else {})} for n, t in columns]
    body = {"output_format": "xtab", "columns": cols, "row_labels": labels, "data": data, "row_count": len(data)}
    return json.dumps({"success": True, "results": [{"visualization_id": "v", "data": {**body, **extra}}]})


BREAKDOWN = tables_from_tool_result(
    _xtab(
        [("Total Discounts", "metric"), ("Total Returns", "metric"), ("COGS", "metric"), ("Gross Profit", "metric")],
        [],
        [[2770402.0, 1103551.0, 33081914.0, 30512880.0]],
    )
)
SPENDERS = tables_from_tool_result(
    _xtab(
        [("Customer name", "attribute"), ("Net Sales", "metric")],
        [["Michael Baker"], ["Michael Parsons"], ["Rebecca Webb"]],
        [[76900.0], [73700.0], [71400.0]],
    )
)

# A real answer to "Summarize the visualization Total sales breakdown" (2024).
REAL = (
    "## Summary\nFor **2024**, COGS was the largest value at **$33.1 M**, exceeding gross profit by approximately "
    "**$2.6 M**. Gross profit reached **$30.5 M**.\n\n## Key Findings\n- Discounts were roughly **2.5×** returns, "
    "with **$2.8 M** versus **$1.1 M**.\n- COGS was **49.0%** of the four values."
)


def test_a_real_answer_is_grounded() -> None:
    result = check_figures(REAL, BREAKDOWN, filter_years=[2024])
    assert result.passed
    assert "figures grounded" in result.reason()


def test_one_invented_figure_fails_and_says_where() -> None:
    result = check_figures(REAL.replace("$33.1 M", "$35.0 M"), BREAKDOWN, filter_years=[2024])
    assert not result.passed
    assert [f.raw for f in result.ungrounded] == ["$35.0 M"]
    reason = result.reason()
    assert "1 of" in reason
    assert "COGS was the largest value at $35.0 M" in reason
    assert "nearest:" in reason
    assert "33.08 M" in reason


@pytest.mark.parametrize(
    ("text", "kind_"),
    [
        ("Discounts were 4× returns.", "ratio"),
        ("COGS was 75% of the values.", "percent"),
        ("Returns were 1,500.", "amount"),
    ],
)
def test_each_kind_is_matched_to_fitting_values(text: str, kind_: str) -> None:
    result = check_figures(text, BREAKDOWN)
    assert [(f.raw.split()[0], f.kind) for f in result.ungrounded][0][1] == kind_


def test_labels_dates_and_names_are_never_figures() -> None:
    text = (
        "In the Top 10 Spenders chart for Q4 2024, Michael Baker leads at $76.9 K on October 23, ahead of the "
        "1-3M age group; daily data from 2024-10-01 covers the top 3 customers."
    )
    result = check_figures(text, SPENDERS, filter_years=[2024], known_text=["Top 10 Spenders", "1-3M"])
    assert result.passed, result.reason()
    assert {f.raw for f in result.figures} == {"2024", "$76.9 K", "3"}


def test_shares_differences_and_first_rows_are_allowed() -> None:
    text = "The top two spent $150.6 K, 67.8% of the three; the leader is $3.2 K ahead of the second."
    assert check_figures(text, SPENDERS).passed


def test_a_year_outside_the_filters_fails() -> None:
    assert check_figures("Sales in 2024 rose versus 2023.", BREAKDOWN, filter_years=[2024]).passed
    wrong = check_figures("Sales in 2020 were flat.", BREAKDOWN, filter_years=[2024])
    assert [f.raw for f in wrong.ungrounded] == ["2020"]


def test_without_a_table_nothing_is_judged() -> None:
    result = check_figures(REAL, [])
    assert result.passed
    assert all(f.status == "unverified" for f in result.figures)


def test_a_percentage_column_counts_as_percent() -> None:
    margin = tables_from_tool_result(
        json.dumps(
            {
                "results": [
                    {
                        "data": {
                            "columns": [{"name": "Gross Profit Margin", "type": "metric", "format": "#,##0.0%"}],
                            "row_labels": [],
                            "data": [[0.4794]],
                            "row_count": 1,
                        }
                    }
                ]
            }
        )
    )
    assert check_figures("The margin was 47.9%.", margin).passed


def test_a_range_takes_the_unit_of_its_end() -> None:
    assert check_figures("The top three spent $71.4–$76.9 K each.", SPENDERS).passed
    wrong = check_figures("The top three spent $1.0–$76.9 K each.", SPENDERS)
    assert [f.raw for f in wrong.ungrounded] == ["$1.0"]


def test_czech_scale_words_and_a_decimal_comma_count() -> None:
    text = "Vede Michael Baker s 76,9 tis. USD, třetí je Rebecca Webb se 71,4 tis."
    assert check_figures(text, SPENDERS).passed
    assert not check_figures("Vede Michael Baker s 96,9 tis. USD.", SPENDERS).passed
    assert check_figures("Všichni tři utratili nad 70 tis. USD.", SPENDERS).passed  # "nad" = above: a bound


def test_a_round_figure_is_read_as_rounded() -> None:
    assert check_figures("Each of the three spent about $70K or more.", SPENDERS).passed
    assert not check_figures("Each of the three spent about $90K.", SPENDERS).passed


def test_a_value_derived_from_rounded_figures_is_allowed() -> None:
    # 33.1 M - 30.5 M from the rounded display values = 2.6 M; the exact gap is 2.57 M
    assert check_figures("COGS exceeded gross profit by $2.6 M.", BREAKDOWN).passed
    # discounts + returns as a share of COGS: (2.77 M + 1.10 M) / 33.08 M
    assert check_figures("Discounts and returns, $3.9 M together, were 11.7% of COGS.", BREAKDOWN).passed


def test_another_data_tools_numbers_and_labels_count() -> None:
    analysis = json.dumps({"drivers": [{"attribute": "Customer age", "value": "7M+", "before": 508, "after": 543}]})
    events = [ToolCallEvent(functionName="analyze_change", functionArguments="{}", result=analysis)]
    tables = tables_from_tool_calls(events)
    text = "Active customers aged 7M+ grew from 508 to 543, up 6.9%."
    assert check_figures(text, tables).passed
    assert not check_figures("Active customers aged 7M+ grew from 508 to 600.", tables).passed


GEO = tables_from_tool_result(
    _xtab(
        [("Country", "attribute"), ("State", "attribute"), ("Active Customers", "metric")],
        [["United States", "California"], ["United States", "Texas"], ["Canada", "Ontario"]],
        [[106.0], [44.0], [60.0]],
    )
)


def test_rows_that_share_a_label_add_up() -> None:
    assert check_figures("The United States has 150 active customers, 71.4% of the total.", GEO).passed


def test_a_bound_and_a_count_of_rows_are_no_values() -> None:
    assert check_figures("All three customers spent more than $70 K; 2 of 3 spent over $73 K.", SPENDERS).passed


def test_any_two_rows_compare_only_when_the_sentence_names_both() -> None:
    five = tables_from_tool_result(
        _xtab(
            [("Customer name", "attribute"), ("Net Sales", "metric")],
            [["Ann Lee"], ["Bob Ray"], ["Cy Fox"], ["Dee Orr"], ["Eve Poe"]],
            [[76900.0], [73700.0], [71400.0], [70000.0], [65000.0]],
        )
    )
    assert check_figures("Bob Ray spent $3.7 K more than Dee Orr.", five).passed
    assert not check_figures("One customer spent $3.7 K more than another.", five).passed


def test_a_daily_series_sums_by_month_and_points_between_percentages() -> None:
    daily = tables_from_tool_result(
        _xtab(
            [("Date", "attribute"), ("Net Sales", "metric")],
            [["2024-10-01"], ["2024-10-02"], ["2024-11-01"], ["2024-11-02"]],
            [[100000.0], [150000.0], [200000.0], [100000.0]],
            row_count=92,
        )
    )
    assert check_figures("October brought $250.0 K and November $300.0 K; 88 days were not read.", daily).passed
    margin = tables_from_tool_result(
        json.dumps(
            {
                "results": [
                    {
                        "data": {
                            "columns": [
                                {"name": "Margin", "type": "metric", "format": "#,##0.0%"},
                                {"name": "Margin - previous period", "type": "metric", "format": "#,##0.0%"},
                            ],
                            "row_labels": [],
                            "data": [[0.4791, 0.4826]],
                            "row_count": 1,
                        }
                    }
                ]
            }
        )
    )
    assert check_figures("The margin fell from 48.3% to 47.9%, about 0.35 percentage points.", margin).passed
    orders = tables_from_tool_result(
        _xtab(
            [("Brand", "attribute"), ("Net Orders", "metric"), ("Net Sales", "metric")],
            [["Corsair"]],
            [[8329.0, 24591441.88]],
        )
    )
    assert check_figures("Corsair averages about $2,952 per order.", orders).passed


STATUS = tables_from_tool_result(
    _xtab(
        [("Order status", "attribute"), ("# of Orders", "metric")],
        [["Processed"], ["In Cart"], ["Canceled"]],
        [[32483.0], [2002.0], [1496.0]],
    )
)
TITLED = tables_from_tool_result(
    _xtab(
        [("Customer name", "attribute"), ("Net Sales", "metric")],
        [["Tracy Carter"], ["Tammy Long"], ["Mrs. Crystal Murray"], ["Jennifer Mejia"]],
        [[1317241.93], [1301535.20], [1277207.42], [1226626.87]],
    )
)


def test_a_value_named_with_the_wrong_row_fails() -> None:
    assert check_figures("Michael Baker leads with $76.9 K, ahead of Michael Parsons at $73.7 K.", SPENDERS).passed
    swapped = check_figures("Michael Parsons leads with $76.9 K.", SPENDERS)
    assert [f.raw for f in swapped.ungrounded] == ["$76.9 K"]
    assert "named next to it" in swapped.reason()


def test_small_words_between_a_name_and_its_figure_keep_them_tied() -> None:
    assert check_figures("Michael Baker leads with a total of $76.9 K.", SPENDERS).passed
    for text in (
        "Michael Parsons leads with a total of $76.9 K.",
        "Sales of Michael Parsons rose to $76.9 K.",
    ):
        wrong = check_figures(text, SPENDERS)
        assert [f.raw for f in wrong.ungrounded] == ["$76.9 K"], text
    # a bare "to" between a name and a figure ends a range: the figure belongs to what follows
    assert check_figures("Net sales fall from $76.9 K for Michael Baker to $71.4 K for Rebecca Webb.", SPENDERS).passed


def test_a_one_digit_amount_is_no_wider_than_a_tenth_of_its_value() -> None:
    table = tables_from_tool_result(
        _xtab([("Net Sales", "metric"), ("Net Orders", "metric")], [], [[1300000.0, 6600000.0]])
    )
    assert not check_figures("Net sales are about $1 M.", table).passed
    assert check_figures("Net orders are about $7 M.", table).passed


def test_names_in_lists_before_or_glued_after_a_figure_count() -> None:
    assert check_figures("Michael Baker and Michael Parsons spent $76.9 K and $73.7 K.", SPENDERS).passed
    assert check_figures(
        "The breakdown shows 32,483 processed, 2,002 in-cart, and 1,496 canceled orders.", STATUS
    ).passed
    assert check_figures("Processed orders dominate at 32,483, while 2,002 are in cart.", STATUS).passed


def test_a_name_without_its_title_names_the_row() -> None:
    assert check_figures("Crystal Murray is third at $1.28 M.", TITLED).passed
    assert check_figures("Mrs. Crystal Murray and Jennifer Mejia follow at $1.3 M and $1.2 M.", TITLED).passed
    assert not check_figures("Crystal Murray is third at $1.23 M.", TITLED).passed


def test_a_derived_value_may_use_rows_the_sentence_names() -> None:
    assert check_figures("Michael Baker leads, $5.5 K more than Rebecca Webb.", SPENDERS).passed


def test_an_invented_figure_named_with_its_row_fails_on_a_long_table() -> None:
    days = [f"2024-{m:02d}-{d:02d}" for m in (10, 11) for d in range(1, 31)][:60]
    values = [100000.0 + 1000.0 * i for i in range(60)]
    long = tables_from_tool_result(
        _xtab([("Date", "attribute"), ("Net Sales", "metric")], [[d] for d in days], [[v] for v in values])
    )
    assert check_figures("Net sales reached $106.0 K on October 7.", long).passed
    assert not check_figures("Net sales reached $120.0 K on October 7.", long).passed
    # two named days of a long series compare on the fly; the month averages too
    assert check_figures("November 10 was $33.0 K above October 7.", long).passed
    assert check_figures("October averaged about $114.5 K per day.", long).passed


def test_a_rows_format_result_names_its_rows_too() -> None:
    rows = tables_from_tool_result(
        json.dumps(
            {
                "results": [
                    {
                        "data": {
                            "columns": [
                                {"name": "Customer", "type": "attribute"},
                                {"name": "Net Sales", "type": "metric"},
                            ],
                            "rows": [
                                {"Customer": "Alice Smith", "Net Sales": 700},
                                {"Customer": "Bob Jones", "Net Sales": 900},
                            ],
                        }
                    }
                ]
            }
        )
    )
    assert check_figures("Bob Jones leads with 900.", rows).passed
    assert not check_figures("Alice Smith leads with 900.", rows).passed


class _Judge:
    def score(self, input: str, expected_output: str, actual_output: str) -> tuple[bool, str]:
        return True, "stub"


def test_a_follow_up_is_checked_against_the_tables_read_earlier(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(kind, "make_judges", lambda model=None: (_Judge(), _Judge()))
    table = _xtab(
        [("Customer name", "attribute"), ("Net Sales", "metric")],
        [["Michael Baker"], ["Michael Parsons"]],
        [[76900.0], [73700.0]],
    )
    summary = ChatResult.model_validate(
        {
            "textResponse": "Michael Baker leads with $76.9 K.",
            "toolCallEvents": [
                {"functionName": "execute_existing_visualizations", "functionArguments": "{}", "result": table}
            ],
        }
    )
    run = kind.SummaryConversation(
        "c",
        turns=[
            kind.SummaryTurn("Summarize", result=summary),
            kind.SummaryTurn("By how much?", result=ChatResult.model_validate({"textResponse": "By $3.2 K."})),
            kind.SummaryTurn("And the total?", result=ChatResult.model_validate({"textResponse": "About $200.0 K."})),
        ],
        scope=None,
    )
    kind.grade_conversation(run, scenario="[widget] Top Spenders", expected_outputs=[{}, {}, {}])
    assert [e.detail["figures_grounded"] for e in run.evaluations] == [True, True, False]
    assert "$200.0 K" in run.evaluations[2].detail["figures_grounded_reason"]
