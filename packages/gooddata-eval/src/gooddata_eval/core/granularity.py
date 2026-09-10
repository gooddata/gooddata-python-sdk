# (C) 2026 GoodData Corporation
"""Date granularities: a closed platform enum, shared by dataset generation and scoring."""

# Date granularities are a closed platform enum (`gooddata_api_client`), identical in
# every workspace, so unlike metric and label names they can be described once and for
# all. Each entry is (title, phrase): the title names the label, the phrase says what the
# breakdown actually does. The phrase matters because a granularity has a cyclical twin --
# MONTH walks consecutive calendar months, MONTH_OF_YEAR stacks every January together --
# and a question saying only "by month" does not choose between them. gpt-5.6-luna built
# `monthOfYear` where the insight used `month`, which is a defensible reading of the words.
GRANULARITIES = {
    "MINUTE": ("Minute", "by minute, consecutive minutes over time (not minute-of-hour)"),
    "HOUR": ("Hour", "by hour, consecutive hours over time (not hour-of-day)"),
    "DAY": ("Day", "by day, one point per calendar day over time (not day-of-week)"),
    "WEEK": ("Week", "by week, consecutive calendar weeks over time (not week-of-year)"),
    "MONTH": ("Month", "by month, one point per calendar month over time (not month-of-year)"),
    "QUARTER": ("Quarter", "by quarter, consecutive calendar quarters over time (not quarter-of-year)"),
    "YEAR": ("Year", "by year, one point per calendar year"),
    "MINUTE_OF_HOUR": ("Minute of Hour", "by minute of the hour (0-59), combining every hour"),
    "MINUTE_OF_DAY": ("Minute of Day", "by minute of the day, combining every day"),
    "HOUR_OF_DAY": ("Hour of Day", "by hour of the day (0-23), combining every day"),
    "DAY_OF_WEEK": ("Day of Week", "by day of the week (Monday to Sunday), combining every week"),
    "DAY_OF_MONTH": ("Day of Month", "by day of the month (1-31), combining every month"),
    "DAY_OF_QUARTER": ("Day of Quarter", "by day of the quarter, combining every quarter"),
    "DAY_OF_YEAR": ("Day of Year", "by day of the year (1-366), combining every year"),
    "WEEK_OF_YEAR": ("Week of Year", "by week of the year (1-53), combining every year"),
    "MONTH_OF_YEAR": ("Month of Year", "by month of the year (January to December), combining every year"),
    "QUARTER_OF_YEAR": ("Quarter of Year", "by quarter of the year (Q1 to Q4), combining every year"),
}


def _camel(granularity: str) -> str:
    """MONTH_OF_YEAR -> monthOfYear, the spelling the platform's label ids actually use."""
    head, *rest = granularity.lower().split("_")
    return head + "".join(part.title() for part in rest)


# Both spellings resolve: label ids come back camelCase from the API, while the
# declarative LDM lists the granularity as the upper-snake enum member.
GRANULARITY_BY_ID = {spelling: enum for enum in GRANULARITIES for spelling in (_camel(enum), enum.lower(), enum)}


def granularity_of(uri: str) -> str | None:
    """The granularity `uri` ends in, as an enum member, or None if it is not a date ref."""
    stem = uri.split("/", 1)[-1]
    if "." not in stem:
        return None
    return GRANULARITY_BY_ID.get(stem.rpartition(".")[2])


def canonical_date_uri(uri: str) -> str:
    """One spelling for a date granularity, whichever the platform happened to return.

    A date dataset exposes each granularity as an attribute whose only label carries the
    same id, so `attribute/order_created_at.month` and `label/order_created_at.month`
    denote the same breakdown. Both come back from the API depending on how the agent
    built the chart, and comparing the raw strings failed a chart that was correct. The
    granularity itself is folded to one spelling too: the API returns `monthOfYear` where
    the declarative LDM says `MONTH_OF_YEAR`, and the two are one breakdown, not two.
    """
    enum = granularity_of(uri)
    if enum is None:
        return uri
    dataset = uri.split("/", 1)[-1].rpartition(".")[0]
    return f"label/{dataset}.{_camel(enum)}"
