# (C) 2026 GoodData Corporation
"""`figures_grounded` for `agentic_summary`: every figure in an answer must come from the data.

The data is what the agent read in the conversation: the tables `execute_existing_visualizations`
returned. A figure is grounded when it is close to an allowed value:

- a cell, a column or row total, a column average, a sum of the first rows (largest, smallest or as listed)
- the difference, ratio, change or "A as % of B" between two cells of one column or one row
  (a long column: its neighbours, first vs last and largest vs smallest)
- in a row or a short column (up to 6 cells): the sum of any cells, and its share of the total or of one cell
- a share: a cell, or a sum of the first rows, over its column total or its row total
- a column shown as a percentage (format with `%`), times 100
- a row count, the rows read, any count the result states, a number inside a label or a title
  (`SanDisk 128GB`, `Top 10`), a rating label as its stars (`***` = 3), a position up to the rows read
- the sum of the rows that share a label (the United States in a country/state table), its share
- across one-row results (KPIs): the difference, ratio, "A as % of B" and "A per B" of two values
- any number of another data tool's result (e.g. a change analysis), and its labels

Figure kinds are matched to fitting values only: an amount to amounts and counts, a percentage
to shares, changes and percentage columns, a ratio (`2.5×`) to ratios. A year is checked
against the years of the active filters (plus the year before, for previous-period
comparisons) and of the date labels.

Tolerance follows what the answer wrote: half of its last digit (`$1.3 M` covers 1.25–1.35 M), for an
amount without decimals at most 10 % of the value (a round `$100K` covers 90–110 K, `$1 M` 0.9–1.1 M),
or 0.5 % of the value, whichever is larger; twice that for a derived
value, which the agent may compute from rounded figures. A range takes its end's unit (`$1.0–$1.3 M`,
`10–15%`). Czech and German scale words and a decimal comma count (`985,3 tis.`, `1,3 Mio.`).
A bound (`above $900 K`, `below $350 K`) is not a value: it stays `unverified`.

A figure next to a row's name is tied to that row: "Michael Parsons leads with $76.9 K" fails when
$76.9 K is Michael Baker's value. The name right before the figure counts (several names in a list
all count), and a name right after it ("2,002 in-cart"); a value about the whole data or a derived
value about rows the sentence names stays allowed. Not tied: answers in another language (labels
stay in English). Text that names a row label, a column or a filter
value (`1-3M`, `Q4 2024`) is removed before extraction, so a label is never read as a figure.

A figure that fits no allowed value is `ungrounded` and fails the check. Nothing is
`ungrounded` when the agent read no table: its figures are `unverified`.

Limit: the check is weak on long tables. With some hundred values in a column the 0.5 % slack is
wider than the gaps between them, so a wrong figure without a row's name next to it fits some cell.
On real answers with one figure changed by 8-15 %, about 7 in 10 changes are caught on tables of up
to 10 rows and about 3 in 10 on tables of more than 50 rows; a figure tied to a named row is
checked against that row at any size.
"""

from __future__ import annotations

import bisect
import dataclasses
import itertools
import json
import math
import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from typing import Any

PAIRWISE_LIMIT = 60  # columns longer than this get adjacent pairs only
PREFIX_LIMIT = 10
SUBSET_LIMIT = 6  # rows/short columns up to this many cells get every sum of cells
ROW_PAIR_LIMIT = 8  # cells of one row compared pairwise: current vs previous period, part vs part
_DATALESS_TOOLS = frozenset({"set_skills"})
_RELATIVE_SLACK = 0.005

_SCALE = {
    "k": 1e3,
    "thousand": 1e3,
    "m": 1e6,
    "mn": 1e6,
    "million": 1e6,
    "b": 1e9,
    "bn": 1e9,
    "billion": 1e9,
    "t": 1e12,
    "trillion": 1e12,
    # Czech, German
    "tis": 1e3,
    "tisíc": 1e3,
    "tsd": 1e3,
    "tausend": 1e3,
    "mil": 1e6,
    "milion": 1e6,
    "milionu": 1e6,
    "milionů": 1e6,
    "miliony": 1e6,
    "mio": 1e6,
    "millionen": 1e6,
    "mld": 1e9,
    "miliarda": 1e9,
    "miliardy": 1e9,
    "mrd": 1e9,
    "milliarden": 1e9,
}
# thousands separator | decimal comma (1-2 digits: never a thousands group) | plain
_NUM = r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+,\d{1,2}(?!\d)|\d+(?:\.\d+)?"
_DECIMAL_COMMA = re.compile(r"-?\d+,\d{1,2}")
_SCALE_WORD = (
    r"\s?(?:(?:thousand|million|billion|trillion|mn|bn|tisíc|tausend|millionen|milliarden|milion[uůy]?|"
    r"miliard[ay]|[KMBT])\b|(?:tis|tsd|mil|mio|mld|mrd)\b\.?)"
)
_FIGURE = re.compile(
    rf"(?P<cur>[$€£])\s?(?P<cnum>-?(?:{_NUM}))(?P<cscale>{_SCALE_WORD})?"
    rf"|(?P<pnum>-?(?:{_NUM}))\s?(?P<pct>%|percent\b|percentage points\b|pp\b)"
    rf"|(?P<rnum>\d+(?:\.\d+)?)\s?(?P<ratio>×|x\b|times\b)"
    rf"|(?P<num>(?:(?<![\w.])-)?(?<![\w.,])(?:{_NUM}))(?P<nscale>{_SCALE_WORD})?",
    re.IGNORECASE,
)
_MONTHS = (
    "january|february|march|april|may|june|july|august|september|october|november|december|"
    "jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec"
)
_DAY_AFTER_MONTH = re.compile(  # "October 16", "October 16–23"
    rf"\b(?:{_MONTHS})\.?\s+\d{{1,2}}(?:st|nd|rd|th)?(?:\s?[–-]\s?\d{{1,2}}(?:st|nd|rd|th)?)?\b", re.IGNORECASE
)
_ISO_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
_QUARTER = re.compile(r"\bQ[1-4]\b|\bH[12]\b", re.IGNORECASE)
_TIME = re.compile(r"\b\d{1,2}:\d{2}\b")
_ORDINAL = re.compile(r"\b\d+(?:st|nd|rd|th)\b", re.IGNORECASE)
_BOUND = re.compile(
    r"\b(?:above|over|exceed(?:s|ed|ing)?|(?:more|less|fewer|greater|higher|lower) than|below|under|at least|at most|"
    r"up to|beyond|nad|pod|více než|méně než|über|unter)\s+$",
    re.IGNORECASE,
)
_NUMBER_IN_TEXT = re.compile(r"\d+(?:[.,]\d+)?")
POSITION_LIMIT = 10  # "top 3", "ranks 3 and 4"; a larger count needs "N of <rows>"
WINDOW_LIMIT = 12  # consecutive rows summed: "16:00-22:00", a quarter of months
ANCHOR_GAP = 60  # chars between a row's name and the figure after it
_SEPARATOR = re.compile(r"[,;]|\b(?:and|while|but|followed|than|versus|vs|und)\b", re.IGNORECASE)
_HONORIFIC = re.compile(r"^(?:Mrs|Mr|Ms|Miss|Dr|Prof)\.?\s+", re.IGNORECASE)
ANCHOR_GAP_AFTER = 25  # a name after the figure: "2,002 are in cart"
_COUNT_OF = re.compile(r"\s+of\s+(?:the\s+|all\s+)?(\d[\d,]*)\b")
_YEAR = re.compile(r"(?<![\d,.$€£])\b(19\d{2}|20\d{2})\b(?![\d,.]*\s?(?:%|[KMB]\b))")
_SENTENCE = re.compile(r"[^.!?\n]*")
# "$1.0–$1.3 M", "10–15%": the first number takes the unit of the second
_RANGE = re.compile(
    rf"(?P<a>[$€£]?\s?(?:{_NUM}))\s?(?:–|—|-|to|až|bis)\s?[$€£]?\s?(?:{_NUM})(?P<unit>{_SCALE_WORD}|\s?%)",
    re.IGNORECASE,
)


@dataclass
class Table:
    """One result the agent read: rows of cells, column names and formats."""

    columns: list[str]
    formats: list[str | None]
    rows: list[list[float | None]]  # measure cells only, one list per row
    labels: list[str]  # every label text of the rows
    row_count: int
    title: str = ""
    truncated: bool = False
    row_labels: list[list[str]] = field(default_factory=list)  # label texts per row, when known
    cache: dict[int, list[Allowed]] = field(default_factory=dict, repr=False, compare=False)
    counts: list[float] = field(default_factory=list)  # other counts the result states (columns, totals)


@dataclass(frozen=True)
class Allowed:
    value: float
    kinds: frozenset[str]  # "amount", "percent", "ratio"
    how: str
    rank: int = 2  # 0 cell, 1 total or count, 2 derived: the simplest explanation is reported
    rows: frozenset[tuple[int, int]] = frozenset()  # (table, row) it is about; empty = the whole data
    named: bool = False  # only when the sentence names every one of its rows (any pair of rows)


@dataclass
class Figure:
    raw: str
    value: float
    kind: str  # amount | percent | ratio | year | bound
    tolerance: float
    sentence: str
    status: str = "unverified"  # grounded | ungrounded | unverified
    rounded: bool = False  # written with trailing zeros ("$100K"): its tolerance already covers rounding
    pos: int = 0  # where it starts in the answer
    match: str = ""
    nearest: list[str] = field(default_factory=list)


# ---------- tables ----------


def _num(v: Any) -> float | None:
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v) if math.isfinite(v) else None
    if isinstance(v, str):
        try:
            return float(v.replace(",", ""))
        except ValueError:
            return None
    return None


def tables_from_tool_result(result: Any) -> list[Table]:
    """Tables of one `execute_existing_visualizations` result (xtab or rows format)."""
    if isinstance(result, str):
        try:
            result = json.loads(result)
        except ValueError:
            return []
    if not isinstance(result, dict):
        return []
    out: list[Table] = []
    for entry in result.get("results") or []:
        data = entry.get("data") if isinstance(entry, dict) else None
        if not isinstance(data, dict):
            continue
        cols = [c for c in data.get("columns") or [] if isinstance(c, dict)]
        measures = [c for c in cols if c.get("type") != "attribute"]
        labels: list[str] = []
        row_labels: list[list[str]] = []
        rows: list[list[float | None]] = []
        if isinstance(data.get("data"), list):  # xtab
            for label in data.get("row_labels") or []:
                row_labels.append([str(x) for x in (label if isinstance(label, list) else [label])])
                labels += row_labels[-1]
            rows = [[_num(v) for v in (r if isinstance(r, list) else [r])] for r in data["data"]]
        elif isinstance(data.get("rows"), list):  # rows format
            names = [c.get("name") for c in measures]
            for r in data["rows"]:
                if isinstance(r, dict):
                    rows.append([_num(r.get(n)) for n in names])
                    row_labels.append([str(v) for k, v in r.items() if k not in names and v is not None])
                    labels += row_labels[-1]
        for c in cols:
            if c.get("type") == "attribute":
                labels += [str(v) for v in c.get("values") or []]
        out.append(
            Table(
                columns=[str(c.get("name", "")) for c in measures],
                formats=[c.get("format") for c in measures],
                rows=rows,
                labels=labels,
                row_count=int(_num(data.get("row_count")) or len(rows)),
                title=str(entry.get("visualization_id") or ""),
                truncated=bool(data.get("truncated")),
                row_labels=row_labels if len(row_labels) == len(rows) else [],
                counts=[
                    v for v in (_num(x) for k, x in data.items() if not isinstance(x, (list, dict))) if v is not None
                ],
            )
        )
    return out


def _walk(value: Any, nums: list[float], labels: list[str], depth: int = 0) -> None:
    if depth > 20:
        return
    if isinstance(value, dict):
        for v in value.values():
            _walk(v, nums, labels, depth + 1)
    elif isinstance(value, list):
        for v in value:
            _walk(v, nums, labels, depth + 1)
    elif isinstance(value, str):
        n = _num(value)
        if n is not None:
            nums.append(n)
        elif len(value) <= 80:
            labels.append(value)
    else:
        n = _num(value)
        if n is not None:
            nums.append(n)


def table_from_any_result(result: Any, title: str = "") -> Table | None:
    """Every number of another data tool's result as one column; its texts as labels."""
    if isinstance(result, str):
        try:
            result = json.loads(result)
        except ValueError:
            return None
    nums: list[float] = []
    labels: list[str] = []
    _walk(result, nums, labels)
    if not nums:
        return None
    # a fraction may be written as a percentage: the column is read as one
    return Table(["value"], ["0.0%"], [[n] for n in nums], labels, len(nums), title)


def tables_from_tool_calls(events: Iterable[Any]) -> list[Table]:
    """The tables of one turn's tool results: visualization results, and any other data tool's numbers."""
    tables: list[Table] = []
    for ev in events:
        name, result = getattr(ev, "function_name", ""), getattr(ev, "result", None)
        if not result or name in _DATALESS_TOOLS:
            continue
        if name == "execute_existing_visualizations":
            tables += tables_from_tool_result(result)
        elif table := table_from_any_result(result, name):
            tables.append(table)
    return tables


# ---------- allowed values ----------


def _cell(row: list[float | None], c: int) -> float | None:
    return row[c] if c < len(row) else None


def _is_percent_format(fmt: str | None) -> bool:
    return bool(fmt) and "%" in str(fmt)


def _table_allowed(t: Table, ti: int) -> list[Allowed]:
    """The values one table allows (cached on the table: a conversation re-checks it every turn)."""
    cached = t.cache.get(ti)
    if cached is not None:
        return cached
    out: list[Allowed] = []
    amount, percent = frozenset({"amount"}), frozenset({"percent"})
    tag = f"table {ti + 1}"
    out.append(Allowed(float(t.row_count), amount, f"{tag} row count", 1))
    out.append(Allowed(float(len(t.rows)), amount, f"{tag} rows read", 1))
    out += [Allowed(v, amount, f"{tag} count stated by the result", 1) for v in t.counts]
    out.append(Allowed(float(len(t.columns)), amount, f"{tag} columns", 1))
    if t.row_count > len(t.rows):
        out.append(Allowed(float(t.row_count - len(t.rows)), amount, f"{tag} rows not read", 1))
    width = max(len(t.rows), len(t.columns))
    out += [Allowed(float(k), amount, "a position", 1) for k in range(1, min(width, POSITION_LIMIT) + 1)]
    out += _label_numbers([*t.labels, *t.columns], tag)
    out += _date_groups(t, ti)
    out += _group_values(t, ti)
    cells_all = [v for r in t.rows for v in r if v is not None]
    if len(t.columns) > 1 and cells_all:  # a pivot: one measure over column labels
        out.append(Allowed(sum(cells_all), amount, f"{tag} total of all cells", 1))
    ncol = max((len(r) for r in t.rows), default=0)
    for c in range(ncol):
        name = t.columns[c] if c < len(t.columns) else f"column {c + 1}"
        fmt = t.formats[c] if c < len(t.formats) else None
        col: list[tuple[int, float]] = [(i, v) for i, r in enumerate(t.rows) if (v := _cell(r, c)) is not None]
        vals = [v for _, v in col]
        if not vals:
            continue
        total = sum(vals)
        for i, v in col:
            at = frozenset({(ti, i)})
            out.append(Allowed(v, amount, f"{name} row {i + 1} = {v:,.2f}", 0, at))
            if _is_percent_format(fmt):
                out.append(Allowed(v * 100, percent, f"{name} row {i + 1} as % = {v * 100:.2f}", 0, at))
            if total:
                out.append(Allowed(v / total * 100, percent, f"{name} row {i + 1} share of column total", 2, at))
        out.append(Allowed(total, amount, f"{name} total = {total:,.2f}", 1))
        out.append(Allowed(total / len(vals), amount, f"{name} average"))
        for order, seq in (("largest", sorted(vals, reverse=True)), ("smallest", sorted(vals)), ("listed", vals)):
            acc = 0.0
            for k, v in enumerate(seq[:PREFIX_LIMIT], start=1):
                acc += v
                if k == 1:  # a cell, already allowed
                    continue
                out.append(Allowed(acc, amount, f"{name} sum of first {k} ({order})"))
                if total:
                    out.append(Allowed(acc / total * 100, percent, f"{name} share of first {k} ({order})"))
        out += _pair_values(col, name, table=ti)
        for a in range(len(col) if len(col) <= PAIRWISE_LIMIT else 0):  # consecutive rows: "18:00-22:00"
            acc = col[a][1]
            for b in range(a + 1, min(len(col), a + WINDOW_LIMIT)):
                acc += col[b][1]
                at = frozenset((ti, col[k][0]) for k in range(a, b + 1))
                how = f"{name} rows {col[a][0] + 1}-{col[b][0] + 1}"
                out.append(Allowed(acc, amount, how, 2, at))
                if total:
                    out.append(Allowed(acc / total * 100, percent, f"{how} share", 2, at))
        if len(col) <= SUBSET_LIMIT:
            out += _subset_values(col, name, lambda i: f"row {i + 1}")
    for i, r in enumerate(t.rows):  # within one row: current vs previous period, part vs whole
        names = [t.columns[c] if c < len(t.columns) else f"column {c + 1}" for c in range(len(r))]
        cells = [(c, v) for c, v in enumerate(r) if v is not None]
        if len(cells) < 2:
            continue
        at = frozenset({(ti, i)})
        row_total = sum(v for _, v in cells)
        row: list[Allowed] = [Allowed(row_total, amount, f"row {i + 1} total")]  # the agent may add rounded cells
        if row_total:
            row += [
                Allowed(va / row_total * 100, percent, f"row {i + 1}: {names[ca]} share of the row") for ca, va in cells
            ]
        # a wide row, or a long table's row of more than current and previous: total and shares only
        if len(cells) > ROW_PAIR_LIMIT or (len(t.rows) > PAIRWISE_LIMIT and len(cells) > 3):
            # first vs last period, neighbours, extremes: a fixed few per row
            row += _pair_values(cells, f"row {i + 1}:", lambda c: names[c], long=True)
            out += [dataclasses.replace(x, rows=at) for x in row]
            continue
        row += _pair_values(cells, f"row {i + 1}:", lambda c: names[c])
        # percentage cells: a % format, or a fraction next to one (a previous period's margin may come unformatted)
        has_pct = any(_is_percent_format(t.formats[c] if c < len(t.formats) else None) for c, _ in cells)
        pct = [
            (c, v)
            for c, v in cells
            if _is_percent_format(t.formats[c] if c < len(t.formats) else None) or (has_pct and abs(v) <= 1.5)
        ]
        row += [  # "about $2,952 per order": one measure per another, in one row
            Allowed(va / vb, amount, f"row {i + 1}: {names[ca]} per {names[cb]}")
            for ca, va in cells
            for cb, vb in cells
            if ca != cb and vb
        ]
        row += [  # 48.3% → 47.9% = 0.35 percentage points
            Allowed((va - vb) * 100, percent, f"row {i + 1}: {names[ca]} − {names[cb]} in points")
            for ca, va in pct
            for cb, vb in pct
            if ca != cb
        ]
        if len(cells) <= SUBSET_LIMIT:
            row += _subset_values(cells, f"row {i + 1}", lambda c: names[c])
        out += [dataclasses.replace(x, rows=at) for x in row]
    t.cache[ti] = out
    return out


def allowed_values(tables: Sequence[Table]) -> list[Allowed]:
    """Every value a figure may be: per table (cells, totals, shares, pairs, ...) and across one-row tables."""
    out: list[Allowed] = []
    amount = frozenset({"amount"})
    for ti, t in enumerate(tables):
        out += _table_allowed(t, ti)
    kpis = [
        (f"{t.columns[c] if c < len(t.columns) else 'value'}", v)
        for t in tables
        if len(t.rows) == 1
        for c, v in enumerate(t.rows[0])
        if v is not None
    ]
    if 1 < len(kpis) <= 40:  # one-row results side by side: Net Sales vs Total Sales, sales per order
        for (na, va), (nb, vb) in itertools.permutations(kpis, 2):
            out += _pair(va, vb, na, nb)
            if vb:
                out.append(Allowed(va / vb, amount, f"{na} per {nb}"))
    return out


def _label_numbers(labels: Iterable[str], tag: str) -> list[Allowed]:
    """Numbers inside labels or titles ("SanDisk 128GB", "Top 10"); a star rating label as its stars."""
    out: list[Allowed] = []
    for label in set(labels):
        if _ISO_DATE.search(label) or re.fullmatch(r"[\d\s/.:-]+", label.strip()):
            continue  # a date or a plain number: its parts ("31" of "2024-10-31") are no figures
        if re.fullmatch(r"\*{1,10}", label.strip()):
            out.append(Allowed(float(len(label.strip())), frozenset({"amount"}), f"{tag} rating label {label}", 1))
            continue
        out.extend(
            Allowed(_to_float(n), frozenset({"amount"}), f"{tag} number in label '{label[:40]}'", 1)
            for n in _NUMBER_IN_TEXT.findall(label)
        )
    return out


def _group_values(t: Table, ti: int) -> list[Allowed]:
    """Rows that share a label (a country over its states): their sum per column, its share, their count."""
    out: list[Allowed] = []
    if not t.row_labels or len(t.row_labels) != len(t.rows):
        return out
    depth = max((len(r) for r in t.row_labels), default=0)
    for level in range(depth):
        groups: dict[str, list[int]] = {}
        for i, labels in enumerate(t.row_labels):
            if level < len(labels):
                groups.setdefault(labels[level], []).append(i)
        if len(groups) > 50:
            continue
        for value, idx in groups.items():
            if not 1 < len(idx) < len(t.rows):
                continue
            at = frozenset((ti, i) for i in idx)
            out.append(Allowed(float(len(idx)), frozenset({"amount"}), f"rows of {value}", 1, at))
            ncol = max(len(t.rows[i]) for i in idx)
            for c in range(ncol):
                vals: list[float] = [v for i in idx if (v := _cell(t.rows[i], c)) is not None]
                col_total = sum(v for r in t.rows if (v := _cell(r, c)) is not None)
                name = t.columns[c] if c < len(t.columns) else f"column {c + 1}"
                acc = sum(vals)
                out.append(Allowed(acc, frozenset({"amount"}), f"{name} of {value} (sum of its rows)", 2, at))
                if acc:
                    out.extend(
                        Allowed(v / acc * 100, frozenset({"percent"}), f"{name} row as % of {value}", 2, at)
                        for v in vals
                    )
                if col_total:
                    out.append(
                        Allowed(acc / col_total * 100, frozenset({"percent"}), f"{name} of {value} share", 2, at)
                    )
    return out


def _date_groups(t: Table, ti: int) -> list[Allowed]:
    """A daily series summed by month, quarter and year of its date labels ("October: $5.3 M")."""
    out: list[Allowed] = []
    keys: dict[str, list[int]] = {}
    for i, labels in enumerate(t.row_labels):
        m = next((_ISO_DATE.search(x) for x in labels if _ISO_DATE.search(x)), None)
        if not m:
            continue
        y, mo = m.group(0)[:4], int(m.group(0)[5:7])
        for key in (f"{y}-{mo:02d}", f"{y}-Q{(mo - 1) // 3 + 1}", y):
            keys.setdefault(key, []).append(i)
    for key, idx in keys.items():
        if len(idx) < 2:
            continue
        at = frozenset((ti, i) for i in idx)
        ncol = max(len(t.rows[i]) for i in idx)
        for c in range(ncol):
            vals: list[float] = [v for i in idx if (v := _cell(t.rows[i], c)) is not None]
            name = t.columns[c] if c < len(t.columns) else f"column {c + 1}"
            out.append(Allowed(sum(vals), frozenset({"amount"}), f"{name} in {key}", 2, at))
            if vals:
                out.append(Allowed(sum(vals) / len(vals), frozenset({"amount"}), f"{name} average in {key}", 2, at))
    return out


def _pair(va: float, vb: float, a: str, b: str) -> list[Allowed]:
    out = [Allowed(va - vb, frozenset({"amount"}), f"{a} − {b}")]
    if vb:
        out += [
            Allowed(va / vb, frozenset({"ratio"}), f"{a} / {b}"),
            Allowed(va / vb * 100, frozenset({"percent"}), f"{a} as % of {b}"),
            Allowed((va - vb) / vb * 100, frozenset({"percent"}), f"change {b} → {a}"),
        ]
    return out


def _pair_values(
    col: list[tuple[int, float]], name: str, label: Any = None, table: int | None = None, long: bool = False
) -> list[Allowed]:
    """Pairs of one column (`table` set) or of one row's cells.

    Always: neighbours, first vs last, largest vs smallest; up to `PAIRWISE_LIMIT` values also each
    vs the largest. Any other pair of a column only when the sentence names both rows ("Tracy
    Carter leads Tiffany Durham by ...").
    """
    label = label or (lambda i: f"row {i + 1}")
    n = len(col)
    hi = max(range(n), key=lambda k: col[k][1]) if n else 0
    lo = min(range(n), key=lambda k: col[k][1]) if n else 0
    plain = {(a, a + 1) for a in range(n - 1)} | {(0, n - 1), (hi, lo)}
    long = long or n > PAIRWISE_LIMIT
    if not long:  # a long column or wide row: neighbours and its ends only, or every value would fit
        plain |= {(k, hi) for k in range(n)}
    plain = {p for p in plain | {(b, a) for a, b in plain} if p[0] != p[1]}
    named = {(a, b) for a in range(n) for b in range(n) if a != b} - plain if not long else set()
    if table is None:  # one row's cells: few, all plain
        plain, named = plain | named, set()
    out: list[Allowed] = []
    for pairs, need_names in ((plain, False), (named, True)):
        for a, b in sorted(pairs):
            (ia, va), (ib, vb) = col[a], col[b]
            at = frozenset({(table, ia), (table, ib)}) if table is not None else frozenset()
            out += [
                dataclasses.replace(x, rows=at, named=need_names)
                for x in _pair(va, vb, f"{name} {label(ia)}", label(ib))
            ]
    return out


def _subset_values(cells: list[tuple[int, float]], where: str, label: Any) -> list[Allowed]:
    """Every sum of 2+ cells (not all), its share of the total and of each other cell."""
    out: list[Allowed] = []
    total = sum(v for _, v in cells)
    for size in range(2, len(cells)):
        for combo in itertools.combinations(cells, size):
            acc = sum(v for _, v in combo)
            how = f"{where}: " + " + ".join(str(label(k)) for k, _ in combo)
            out.append(Allowed(acc, frozenset({"amount"}), how))
            if total:
                out.append(Allowed(acc / total * 100, frozenset({"percent"}), f"{how} share of the total"))
            for k, v in cells:
                if all(k != c for c, _ in combo):
                    if abs(v) > abs(acc):  # "Processed exceed In Cart and Canceled combined by 28,985"
                        out.append(Allowed(v - acc, frozenset({"amount"}), f"{label(k)} − ({how})"))
                    if v:
                        out.append(Allowed(acc / v * 100, frozenset({"percent"}), f"{how} as % of {label(k)}"))
                elif acc:
                    out.append(Allowed(v / acc * 100, frozenset({"percent"}), f"{label(k)} as % of ({how})"))
    return out


# ---------- figures ----------


def _strip_known_text(text: str, known: Iterable[str]) -> str:
    """Blank out labels and dates; same length, so positions still point into the answer."""
    for s in sorted({_dashes(k) for k in known if k and len(k) >= 2 and re.search(r"\d", k)}, key=len, reverse=True):
        # a whole label only: "03" must not cut "$295,039.98"
        text = re.sub(rf"(?<![\w.,]){re.escape(s)}(?![\w]|[.,]\d)", _blank, text)
    for rx in (_ISO_DATE, _DAY_AFTER_MONTH, _QUARTER, _TIME, _ORDINAL):
        text = rx.sub(_blank, text)
    return text


def _blank(m: re.Match[str]) -> str:
    return " " * len(m.group(0))


def _dashes(text: str) -> str:
    """An en dash as "-" ("1–3M" in an answer is the label "1-3M"); an em dash is a pause. Same length."""
    return text.replace("–", "-").replace("—", " ")


def _to_float(num: str) -> float:
    if _DECIMAL_COMMA.fullmatch(num):
        return float(num.replace(",", "."))
    return float(num.replace(",", ""))


def _scale_of(word: str | None) -> float:
    return _SCALE.get((word or "").strip().rstrip(".").lower(), 1.0)


def _tolerance(num: str, scale: float, value: float, kind: str = "amount") -> float:
    """Half of the last written digit, for an amount at most 10% of the value when it has no decimals.

    - Trailing zeros of a whole amount are not written digits: "$100K" may be a rounded 96 K (90-110 K).
    - A whole amount with a scale word keeps the same limit: "$1 M" is 0.9-1.1 M, "$7 M" 6.5-7.5 M.
    - A percentage is read as written: "20%" is 19.5-20.5.
    """
    digits = num.lstrip("-")
    if _DECIMAL_COMMA.fullmatch(digits):
        unit = 10.0 ** -len(digits.split(",")[1])
    elif "." in digits:
        unit = 10.0 ** -len(digits.split(".")[1])
    else:
        whole = digits.replace(",", "")
        unit = 10.0 ** (len(whole) - len(whole.rstrip("0"))) if whole.strip("0") and kind == "amount" else 1.0
    half = 0.5 * unit * scale
    if unit > 1:
        half = max(0.5 * scale, min(half, abs(value) * 0.1))
    elif unit == 1 and scale > 1 and kind == "amount":
        # "$1 M": half of its only digit is 50% of the value, wide enough to match an unrelated cell
        half = min(half, abs(value) * 0.1)
    return max(half, abs(value) * _RELATIVE_SLACK)


# a period after a title ("Mrs. Crystal Murray") ends no sentence
_SENTENCE_END = re.compile(r"(?<!\bMrs)(?<!\bMr)(?<!\bMs)(?<!\bDr)(?<!\bvs)[.!?](?=\s)|\n")


def _sentence_at(text: str, pos: int) -> str:
    """The sentence around `pos`; a decimal point does not end a sentence."""
    start = max((m.end() for m in _SENTENCE_END.finditer(text, 0, pos)), default=0)
    end_match = _SENTENCE_END.search(text, pos)
    end = end_match.start() + 1 if end_match else len(text)
    return " ".join(text[start:end].split())[:160]


def extract_figures(text: str, known_text: Iterable[str] = ()) -> list[Figure]:
    """Figures of an answer, labels and dates removed first; markdown bold is ignored."""
    plain = _dashes(text.replace("**", "").replace("__", ""))
    cleaned = _strip_known_text(plain, known_text)
    figures = [
        Figure(m.group(0), float(m.group(1)), "year", 0.0, _sentence_at(plain, m.start()), pos=m.start())
        for m in _YEAR.finditer(cleaned)
    ]
    cleaned_no_years = _YEAR.sub(lambda m: " " * len(m.group(0)), cleaned)
    range_unit = {m.start("a"): m.group("unit") for m in _RANGE.finditer(cleaned_no_years)}
    for m in _FIGURE.finditer(cleaned_no_years):
        if m.group("cur"):
            num, scale_word, kind = m.group("cnum"), m.group("cscale"), "amount"
        elif m.group("pct"):
            num, scale_word, kind = m.group("pnum"), None, "percent"
        elif m.group("ratio"):
            num, scale_word, kind = m.group("rnum"), None, "ratio"
        else:
            num, scale_word, kind = m.group("num"), m.group("nscale"), "amount"
        unit = range_unit.get(m.start())
        # "$1.0–$1.3 M" yes; "from $64,610.33 to $26.0 K" is a change, not a range
        if (
            unit
            and not scale_word
            and kind == "amount"
            and len(num.lstrip("-").split(".")[0].split(",")[0]) <= 3
            and "," not in num
        ):
            if unit.strip() == "%":
                kind = "percent"
            else:
                scale_word = unit
        scale = _scale_of(scale_word)
        value = _to_float(num) * scale
        if _BOUND.search(cleaned_no_years[max(0, m.start() - 20) : m.start()]):
            kind = "bound"  # "above $900 K" bounds the data, it is no value of it: stays unverified
        digits = num.lstrip("-").replace(",", "")
        rounded = kind == "amount" and digits.isdigit() and digits.endswith("0") and bool(digits.strip("0"))
        figures.append(
            Figure(
                m.group(0).strip(),
                value,
                kind,
                _tolerance(num, scale, value, kind),
                _sentence_at(plain, m.start()),
                rounded=rounded,
                pos=m.start(),
            )
        )
    return figures


# ---------- check ----------


def _fmt(v: float) -> str:
    a = abs(v)
    for limit, suffix in ((1e9, " B"), (1e6, " M"), (1e3, " K")):
        if a >= limit:
            return f"{v / limit:,.2f}{suffix}"
    return f"{v:,.4g}"


@dataclass
class GroundingResult:
    figures: list[Figure]
    tables_read: int

    @property
    def ungrounded(self) -> list[Figure]:
        return [f for f in self.figures if f.status == "ungrounded"]

    @property
    def passed(self) -> bool:
        return not self.ungrounded

    def reason(self) -> str:
        checked = [f for f in self.figures if f.status != "unverified"]
        head = (
            f"{len(self.ungrounded)} of {len(checked)} figures not in the data"
            if self.ungrounded
            else f"{len(checked)} figures grounded"
        )
        lines = [
            head + (f", {len(self.figures) - len(checked)} unverified" if len(checked) < len(self.figures) else "")
        ]
        for f in sorted(self.figures, key=lambda f: {"ungrounded": 0, "unverified": 1, "grounded": 2}[f.status]):
            mark = {"ungrounded": "✗", "unverified": "?", "grounded": "✓"}[f.status]
            if f.status == "ungrounded":
                lines.append(f'  {mark} "{f.raw}" ({f.kind}, ±{_fmt(f.tolerance)}) in "{f.sentence}"')
                lines.append(f"     nearest: {' · '.join(f.nearest) or '-'}")
            else:
                lines.append(f'  {mark} "{f.raw}" {("= " + f.match) if f.match else ""}'.rstrip())
        return "\n".join(lines)


def _allowed_years(filter_years: Iterable[int], tables: Sequence[Table]) -> set[int]:
    years = set()
    for y in filter_years:
        years |= {y - 1, y, y + 1}
    for t in tables:
        for label in [*t.labels, *t.columns]:
            for y in re.findall(r"\b(19\d{2}|20\d{2})\b", label):
                years |= {int(y) - 1, int(y)}
    return years


def _row_names(tables: Sequence[Table]) -> dict[tuple[int, int], list[str]]:
    """Per row, its label texts that can name it in a sentence (2+ chars, with a letter: "WD", "Ontario")."""
    out: dict[tuple[int, int], list[str]] = {}
    for ti, t in enumerate(tables):
        for i, labels in enumerate(t.row_labels):
            names = [_dashes(x).strip() for x in labels if len(x.strip()) >= 2 and re.search(r"[^\W\d_]", x)]
            names += [n for x in labels for n in _date_names(x)]
            if names:
                out[(ti, i)] = names
    # a label every row shares (one country) names no row in particular
    counts: dict[str, int] = {}
    for names in out.values():
        for n in set(names):
            counts[n] = counts.get(n, 0) + 1
    total = len(out)
    return {k: [n for n in v if counts[n] < total or total == 1] for k, v in out.items()}


_MONTH_NAMES = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def _date_names(label: str) -> list[str]:
    """How an answer names a day label ("2024-10-07"): "October 7" and "Oct 7"."""
    m = re.fullmatch(r"\s*(\d{4})-(\d{2})-(\d{2})\s*", label)
    if not m or not 1 <= int(m.group(2)) <= 12:
        return []
    month, day = _MONTH_NAMES[int(m.group(2)) - 1], int(m.group(3))
    return [f"{month} {day}", f"{month[:3]} {day}"]


def _mentions(text: str, row_names: dict[tuple[int, int], list[str]]) -> list[tuple[int, int, frozenset]]:
    """Where the answer names rows: (start, end, rows the name belongs to).

    A whole-word match in any case; a space and a hyphen match each other ("in-cart" = "In Cart"); a
    name without its title ("Crystal Murray") or the start of a longer label ("OBSBOT" for
    "OBSBOT Tiny PTZ 4K Webcam") names that row too.
    """
    by_name: dict[str, set[tuple[int, int]]] = {}
    for key, names in row_names.items():
        for n in names:
            for variant in {n, _HONORIFIC.sub("", n)}:
                if len(variant) >= 2:
                    by_name.setdefault(variant.lower(), set()).add(key)
    for name in list(by_name):  # a short name also names the longer labels it starts
        for other, rows in by_name.items():
            if other.startswith(name + " ") and len(name) >= 4:
                by_name[name] = by_name[name] | rows
    out: list[tuple[int, int, frozenset]] = []
    for name, rows in by_name.items():
        pattern = r"[\s-]+".join(re.escape(w) for w in re.split(r"[\s-]+", name))
        out.extend(
            (m.start(), m.end(), frozenset(rows)) for m in re.finditer(rf"(?<!\w){pattern}(?!\w)", text, re.IGNORECASE)
        )
    # a longer name wins over a name inside it ("Crystal Murray" in "Mrs. Crystal Murray")
    out.sort(key=lambda x: (x[0], -(x[1] - x[0])))
    kept: list[tuple[int, int, frozenset]] = []
    for x in out:
        if not kept or x[0] >= kept[-1][1]:
            kept.append(x)
    return kept


def _figure_row(f: Figure, figures: list[Figure], mentions: list[tuple[int, int, frozenset]], text: str) -> frozenset:
    """The rows a figure is about, from the names next to it in its sentence; empty when none.

    - names before it, after the previous figure ("Tracy Carter leads with $1.3 M"); several
      names there ("Clothing and Home Goods are at $3.2 M and $2.2 M") all count
    - the name right after it, joined by a few words ("2,002 are in cart"), not by "and" or a comma
    """
    start = max((m.end() for m in _SENTENCE_END.finditer(text, 0, f.pos)), default=0)
    end_match = _SENTENCE_END.search(text, f.pos)
    end = end_match.start() if end_match else len(text)
    prev = [g.pos + len(g.raw) for g in figures if g is not f and start <= g.pos < f.pos]
    seg = max([start, *prev])
    rows: set = set()
    before = [m for m in mentions if seg <= m[0] and m[1] <= f.pos]
    # the last name must be close and lead straight to the figure ("Tracy Carter leads, while the
    # bottom of the list is near $1.0 M" is not about Tracy); then every name of the list counts
    gap = text[before[-1][1] : f.pos] if before else ""
    # "from 3 on October 1 to 19": the figure after a bare "to" is the other end of a range
    led = bool(before) and not _SEPARATOR.search(gap) and gap.strip(" $€£*").lower() != "to"
    if led and f.pos - before[-1][1] <= ANCHOR_GAP:
        for m in before:
            rows |= m[2]
    after_pos = f.pos + len(f.raw)
    right_after = [m for m in mentions if after_pos < m[0] <= after_pos + 2 and not text[after_pos : m[0]].strip()]
    if right_after:  # "2,002 in-cart": the name glued to the figure is the one meant
        return right_after[0][2]
    nxt = min([g.pos for g in figures if g is not f and after_pos <= g.pos < end] + [end])
    after = [m for m in mentions if after_pos <= m[0] < nxt and m[0] - after_pos <= ANCHOR_GAP_AFTER]
    if after and not _SEPARATOR.search(text[after_pos : after[0][0]]):
        rows |= after[0][2]
    return frozenset(rows)


def _row_name(t: Table, r: int) -> str:
    return " / ".join(t.row_labels[r]) if r < len(t.row_labels) else f"row {r + 1}"


def _named_pairs(tables: Sequence[Table], anchors: set[tuple[int, int]]) -> list[Allowed]:
    """Pairs of rows a sentence names, in every column of their table ("February 10 was 155% above January 20")."""
    if not 1 < len(anchors) <= 8:
        return []
    out: list[Allowed] = []
    for (ta, ra), (tb, rb) in itertools.permutations(sorted(anchors), 2):
        if ta != tb or ta >= len(tables):
            continue
        t = tables[ta]
        for c in range(min(len(t.rows[ra]), len(t.rows[rb]))):
            va, vb = t.rows[ra][c], t.rows[rb][c]
            if va is None or vb is None:
                continue
            col = t.columns[c] if c < len(t.columns) else f"column {c + 1}"
            out += [
                dataclasses.replace(x, rows=frozenset({(ta, ra), (ta, rb)}))
                for x in _pair(va, vb, f"{col} {_row_name(t, ra)}", _row_name(t, rb))
            ]
    return out


def _fits_anchors(a: Allowed, anchors: set[tuple[int, int]], own: frozenset) -> bool:
    """Whether a value may explain a figure, given the rows its sentence names.

    - a pair of any two rows: only when the sentence names both
    - a figure with its own row (the name next to it): a cell of that row, a value about the whole
      data (totals, counts), or a derived value about rows the sentence names ("$44.1 M more than
      Home Goods" after "Audio & Video Accessories")
    """
    if a.named and not (anchors and a.rows <= anchors):
        return False
    if not own or not a.rows or a.rows & own:
        return True
    return a.rank == 2 and bool(anchors) and a.rows <= anchors


def check_figures(
    answer: str,
    tables: Sequence[Table],
    *,
    filter_years: Iterable[int] = (),
    known_text: Iterable[str] = (),
) -> GroundingResult:
    """Check every figure of `answer` against the values `tables` allow (see the module docstring).

    `filter_years` are the years of the active filters; `known_text` names on screen (titles,
    filter values) that hold digits and are no figures.
    """
    labels = [lab for t in tables for lab in t.labels] + [c for t in tables for c in t.columns]
    figures = extract_figures(answer, [*known_text, *labels])
    if not tables:
        return GroundingResult(figures, 0)
    allowed = allowed_values(tables) + _label_numbers(known_text, "title")
    by_kind: dict[str, list[Allowed]] = {"amount": [], "percent": [], "ratio": []}
    for a in allowed:
        for k in a.kinds:
            by_kind[k].append(a)
    sorted_by_kind = {k: sorted(v, key=lambda a: abs(a.value)) for k, v in by_kind.items()}
    keys = {k: [abs(a.value) for a in v] for k, v in sorted_by_kind.items()}
    years = _allowed_years(filter_years, tables)
    plain = _dashes(answer.replace("**", "").replace("__", ""))
    row_names = _row_names(tables)
    # labels stay in English: in another language a name next to a figure may not be the row's name
    letters = [ch for ch in plain if ch.isalpha()]
    english = not letters or sum(not ch.isascii() for ch in letters) / len(letters) < 0.01
    mentions = _mentions(plain, row_names) if english else []
    counts = {float(t.row_count) for t in tables} | {float(len(t.rows)) for t in tables}
    for f in figures:
        if f.kind == "year":
            if years and int(f.value) not in years:
                f.status, f.nearest = "ungrounded", [f"years in filters/labels: {sorted(years)}"]
            else:
                f.status, f.match = "grounded", "a year of the filters or labels"
            continue
        if f.kind == "bound":
            continue
        c_start = max((m.end() for m in _SENTENCE_END.finditer(plain, 0, f.pos)), default=0)
        c_end_match = _SENTENCE_END.search(plain, f.pos)
        c_end = c_end_match.start() if c_end_match else len(plain)
        anchors = {r for m in mentions if c_start <= m[0] < c_end for r in m[2]}
        own = _figure_row(f, figures, mentions, plain)
        of = _COUNT_OF.match(plain, f.pos + len(f.raw))
        if (
            of
            and f.kind == "amount"
            and float(f.value).is_integer()
            and _to_float(of.group(1)) in counts
            and f.value <= _to_float(of.group(1))
        ):
            f.status, f.match = "grounded", f"a count of rows out of {of.group(1)}"
            continue
        pool, pool_keys = sorted_by_kind[f.kind], keys[f.kind]
        named_pairs = [a for a in _named_pairs(tables, anchors) if f.kind in a.kinds]
        if named_pairs:  # rows the sentence names, compared on the fly (any two rows of a long column)
            pool = sorted([*pool, *named_pairs], key=lambda a: abs(a.value))
            pool_keys = [abs(a.value) for a in pool]
        target = abs(f.value)
        i = bisect.bisect_left(pool_keys, target)
        reach = f.tolerance if f.rounded else 2 * f.tolerance  # a derived value may come from rounded figures
        window = pool[
            max(0, bisect.bisect_left(pool_keys, target - reach) - 3) : bisect.bisect_right(pool_keys, target + reach)
            + 3
        ]
        inside = sorted(
            (
                a
                for a in window
                if abs(abs(a.value) - target) <= (reach if a.rank == 2 else f.tolerance) * (1 + 1e-9) + 1e-9
                and _fits_anchors(a, anchors, own)
            ),
            key=lambda a: (a.rank, abs(abs(a.value) - target)),
        )
        if inside:
            f.status, f.match = "grounded", f"{inside[0].how} ({_fmt(inside[0].value)})"
        else:
            near = sorted(pool[max(0, i - 3) : i + 3], key=lambda a: abs(abs(a.value) - target))[:3]
            cells = [a for a in pool if a.rank == 0]
            cell = min(cells, key=lambda a: abs(abs(a.value) - target)) if cells else None
            if cell and cell not in near:  # the closest cell says most about a wrong figure
                near = [cell, *near[:2]]
            f.status = "ungrounded"
            f.nearest = [f"{a.how} = {_fmt(a.value)}" for a in near]
            if own:
                f.nearest.append(f"about the row(s) named next to it: {sorted(r + 1 for _, r in own)[:5]}")
    return GroundingResult(figures, len(tables))
