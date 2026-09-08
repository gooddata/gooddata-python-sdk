# (C) 2026 GoodData Corporation
"""Reverse-generate `visualization` dataset items from a workspace's real insights.

The inverse of hand-authoring: instead of writing a question and then guessing the
expected metric/dimension/filter, this reads the *existing* visualizations a customer
already built (via the read-only declarative analytics model), translates each one's
buckets/filters into an `expected_output.visualization` AAC spec, and only then asks an
LLM to write the analyst question a user would ask to get that chart back.

`expected_output` is therefore copied out of a real object, never invented -- which is
what satisfies "answerable with the current data model" and "expected answers reference
metrics that exist in the LDM" by construction. The LLM only writes English.

Driven by `gd-eval generate`; the functions here are importable for programmatic use.
"""

import hashlib
import json
import os
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from gooddata_eval.core.models import CreatedVisualization, DatasetItem

# AD `visualizationUrl` -> AAC type. Explicit and exhaustive: an unmapped url raises
# `Unsupported` and the insight is skipped loudly, rather than silently degrading to an
# unscored "". Types outside the evaluator's own type map still normalize predictably
# (`x_chart` -> `X`), so keeping them is safe.
VIZ_TYPE_MAP = {
    "local:area": "area_chart",
    "local:bar": "bar_chart",
    "local:bubble": "bubble_chart",
    "local:bullet": "bullet_chart",
    "local:column": "column_chart",
    "local:combo": "combo_chart",
    "local:combo2": "combo_chart",
    "local:dependencywheel": "dependency_wheel_chart",
    "local:donut": "donut_chart",
    "local:funnel": "funnel_chart",
    "local:headline": "headline",
    "local:heatmap": "heatmap",
    "local:line": "line_chart",
    "local:pie": "pie_chart",
    "local:pushpin": "geo_pushpin_chart",
    "local:pyramid": "pyramid_chart",
    "local:repeater": "repeater",
    "local:sankey": "sankey_chart",
    "local:scatter": "scatter_plot",
    "local:table": "table",
    "local:treemap": "treemap",
    "local:waterfall": "waterfall_chart",
    "local:xirr": "xirr",
}

# Words that make a question *name* a chart form. `expected_output.type` is only set
# when the question actually constrains the form -- an insight's `visualizationUrl`
# records what a human clicked, not what the question asks for, so copying it in
# unconditionally scores the agent on a choice the question never made.
TYPE_WORDS = {
    "area_chart": ("area chart",),
    "bar_chart": ("bar chart", "bar graph"),
    "bubble_chart": ("bubble chart",),
    "bullet_chart": ("bullet chart",),
    "column_chart": ("column chart",),
    "combo_chart": ("combo chart", "combination chart"),
    "donut_chart": ("donut chart", "doughnut chart"),
    "funnel_chart": ("funnel chart",),
    "geo_pushpin_chart": ("map", "pushpin"),
    "headline": ("headline", "single number", "kpi", "big number"),
    "heatmap": ("heatmap", "heat map"),
    "line_chart": ("line chart", "line graph"),
    "pie_chart": ("pie chart",),
    "pyramid_chart": ("pyramid chart",),
    "scatter_plot": ("scatter plot", "scatterplot"),
    "table": ("table",),
    "treemap": ("treemap", "tree map"),
    "waterfall_chart": ("waterfall chart",),
}

# AD bucket localIdentifier -> AAC bucket. The evaluator unions view_by/segment_by/
# rows/columns into one dimension set when scoring, so an imperfect row/column split
# costs nothing.
BUCKET_MAP = {
    "measures": "metrics",
    "secondary_measures": "metrics",
    "view": "view_by",
    "attribute": "view_by",
    "trend": "view_by",
    "segment": "segment_by",
    "stack": "segment_by",
    "columns": "columns",
}

SHAPES = (
    "single_metric_callout",
    "breakdown_by_dimension",
    "filtered_view",
    "time_series",
    "comparison",
)

# A question may only use ranking language if the spec actually ranks, and filter
# language if the spec actually filters. Otherwise the expected output contradicts the
# question and the item punishes the agent for reading it correctly.
RANK_WORDS = re.compile(r"\b(top|bottom|most|fewest|highest|lowest|ranked|rank|limit it to)\b", re.I)
FILTER_WORDS = re.compile(
    r"\b(only|excluding|exclude|filtered|restricted to|limited to|just the"
    r"|last (?:year|quarter|month|week)|this (?:year|quarter|month|week)"
    r"|year to date|ytd|in \d{4})\b",
    re.I,
)

# A slot the writer failed to fill: it copied the instruction instead of a real name.
PLACEHOLDER = re.compile(r"\b(breakdown|split|filter)\s+dimension\b|[{}<>]")
# The text a question breaks down by. `(?<!...)` keeps a bare "by" from matching the
# ranking phrasing ("top 5 by Spend"), which is legitimate without any dimension.
BY_CLAUSE = re.compile(
    r"\b(?:broken down by|split by|grouped by|(?<!ranked )(?<!sorted )(?<!\d )by)\s+(.+?)(?:\?|$|,| for | with | in | over )",
    re.I,
)
# Phrasings that deliberately assert the absence of a breakdown.
NO_BREAKDOWN = re.compile(
    r"\b(?:no|without|not)\b[^?.]{0,40}?"
    r"\b(?:breakdown|break(?:ing)? (?:it|them) down|split|splits|grouping|dimensions?)\b",
    re.I,
)

PHRASE_SYSTEM = (
    "You write the question a business analyst would type into a BI chat assistant to get "
    "a specific chart back. You are given that chart's exact definition. Reply with the "
    "question only -- no quotes, no preamble, no explanation."
)

TEST_KIND = "visualization"

_MAX_SLUG_LEN = 50
_HASH_LEN = 4


class Unsupported(Exception):
    """This insight cannot be expressed as an AAC spec without guessing."""


def _slugify(text: str) -> str:
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text).strip("-")
    if len(slug) <= _MAX_SLUG_LEN:
        return slug
    truncated = slug[:_MAX_SLUG_LEN]
    if "-" in truncated:
        truncated = truncated.rsplit("-", 1)[0]
    return truncated.strip("-")


def mint_id(question: str, existing_ids: set[str]) -> str:
    """Stable slug id for a question, with a content hash appended on collision."""
    candidate = _slugify(question) or "question"
    if candidate not in existing_ids:
        return candidate
    return f"{candidate}-{hashlib.sha256(question.encode()).hexdigest()[:_HASH_LEN]}"


def list_ids(directory: Path) -> set[str]:
    """Ids already present in `directory` (recursively), so new ones don't collide."""
    ids: set[str] = set()
    if not Path(directory).is_dir():
        return ids
    for path in Path(directory).glob("**/*.json"):
        try:
            raw = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(raw, dict) and isinstance(raw.get("id"), str):
            ids.add(raw["id"])
    return ids


def _alias(prefix: str, uri: str, taken: set) -> str:
    stem = re.sub(r"[^a-z0-9]+", "_", uri.split("/", 1)[-1].lower()).strip("_")
    base = prefix + re.sub(rf"^{prefix}", "", stem)[:40]
    alias, n = base, 2
    while alias in taken:
        alias, n = f"{base}_{n}", n + 1
    taken.add(alias)
    return alias


def _measure_field(measure: dict) -> dict:
    """AD measure -> AAC query field. Raises `Unsupported` for anything derived."""
    definition = measure.get("definition") or {}
    simple = definition.get("measureDefinition")
    if simple is None:
        raise Unsupported(f"derived measure ({', '.join(definition) or 'unknown'})")
    if simple.get("filters"):
        # Measure-level filters have no AAC `filter_by` equivalent -- they'd silently
        # vanish and turn a filtered number into an unfiltered one.
        raise Unsupported("measure-level filters")
    identifier = (simple.get("item") or {}).get("identifier") or {}
    obj_id, obj_type = identifier.get("id"), identifier.get("type")
    if not obj_id or obj_type not in ("metric", "fact"):
        raise Unsupported(f"unresolvable measure item ({obj_type})")
    field = {"using": f"{obj_type}/{obj_id}"}
    if obj_type == "fact":
        field["aggregation"] = (simple.get("aggregation") or "sum").upper()
    return field


def _granularity(raw: str) -> str:
    """'GDC.time.month' -> 'MONTH'."""
    return (raw or "").rsplit(".", 1)[-1].upper()


def _local_id(ref) -> str | None:
    """A field reference, in either the bare-string or `{"localIdentifier": ...}` form."""
    if isinstance(ref, dict):
        return ref.get("localIdentifier")
    return ref if isinstance(ref, str) else None


def _convert_filter(raw: dict, alias_of: dict) -> dict | None:
    """AD filter -> AAC filter_by entry.

    Returns None for a no-op filter (AD's "All" selection), which carries no meaning to
    express and must not make the whole insight unusable. Raises `Unsupported` when a
    filter does mean something this can't express.
    """
    if "relativeDateFilter" in raw:
        f = raw["relativeDateFilter"]
        if f.get("from") is None and f.get("to") is None:
            return None  # all-time window: no restriction to state
        return {
            "type": "date_filter",
            "using": f"dataset/{(f.get('dataSet') or {}).get('identifier', {}).get('id', '')}",
            "granularity": _granularity(f.get("granularity")),
            "from": f.get("from"),
            "to": f.get("to"),
        }
    if "absoluteDateFilter" in raw:
        f = raw["absoluteDateFilter"]
        return {
            "type": "date_filter",
            "using": f"dataset/{(f.get('dataSet') or {}).get('identifier', {}).get('id', '')}",
            "from": f.get("from"),
            "to": f.get("to"),
        }
    for key, state_key in (("positiveAttributeFilter", "include"), ("negativeAttributeFilter", "exclude")):
        if key in raw:
            f = raw[key]
            elements = f.get("in") if "in" in f else f.get("notIn") or {}
            values = elements.get("values")
            if values == []:
                # AD's "All" selection -- an empty exclusion restricts nothing, and an empty
                # inclusion is not something a question can ask for either.
                return None
            if not values:
                # `uris`-form element refs can't be turned back into the literal strings
                # the evaluator compares on -- authoring a guessed string fails silently.
                raise Unsupported(f"{key} without literal values")
            label_id = (f.get("displayForm") or {}).get("identifier", {}).get("id")
            if not label_id:
                raise Unsupported(f"{key} without a resolvable displayForm")
            return {"type": "attribute_filter", "using": f"label/{label_id}", "state": {state_key: values}}
    if "rankingFilter" in raw:
        f = raw["rankingFilter"]
        # Both AD spellings: plural lists of local ids, and the singular object form.
        measures = f.get("measures") or ([f["measure"]] if f.get("measure") else [])
        measure_id = _local_id(measures[0]) if measures else None
        if measure_id not in alias_of:
            raise Unsupported("ranking filter over an unresolvable measure")
        entry = {"type": "ranking_filter", "using": alias_of[measure_id]}
        attributes = f.get("attributes") or ([f["attribute"]] if f.get("attribute") else [])
        attribute_id = _local_id(attributes[0]) if attributes else None
        if attribute_id in alias_of:
            entry["attribute"] = alias_of[attribute_id]
        entry["bottom" if f.get("operator") == "BOTTOM" else "top"] = f.get("value")
        return entry
    raise Unsupported(f"filter type {', '.join(raw) or 'unknown'}")


def _sorts(content: dict, alias_of: dict) -> list:
    """AD sorts -> AAC `sort_by`. Raises `Unsupported` for an unresolvable sort."""
    out = []
    for raw in content.get("sorts") or []:
        if "attributeSortItem" in raw:
            item = raw["attributeSortItem"]
            local_id = item.get("attributeIdentifier")
        elif "measureSortItem" in raw:
            item = raw["measureSortItem"]
            locators = item.get("locators") or []
            local_id = next(
                (loc["measureLocatorItem"].get("measureIdentifier") for loc in locators if "measureLocatorItem" in loc),
                None,
            )
        else:
            raise Unsupported(f"sort type {', '.join(raw) or 'unknown'}")
        if local_id not in alias_of:
            raise Unsupported("sort over an unresolvable field")
        out.append({"field": alias_of[local_id], "direction": (item.get("direction") or "desc").upper()})
    return out


def convert(viz: dict, date_instance_ids: set, display_names: dict | None = None) -> dict:
    """Declarative visualization object -> AAC `visualization` spec. Raises `Unsupported`."""
    content = viz.get("content") or {}
    url = content.get("visualizationUrl")
    if url not in VIZ_TYPE_MAP:
        raise Unsupported(f"unmapped visualizationUrl '{url}' -- add it to VIZ_TYPE_MAP")
    spec: dict[str, Any] = {
        "id": re.sub(r"[^a-z0-9_]+", "_", (viz.get("id") or "viz").lower())[:30],
        "type": VIZ_TYPE_MAP[url],
        "title": viz.get("title") or viz.get("id"),
        "query": {"fields": {}, "filter_by": {}},
        "metrics": [],
        "view_by": [],
        "segment_by": [],
        "columns": [],
        "rows": [],
        "sort_by": [],
    }
    fields, taken, alias_of = spec["query"]["fields"], set(), {}

    for bucket in content.get("buckets") or []:
        target = BUCKET_MAP.get(bucket.get("localIdentifier"))
        if target is None:
            raise Unsupported(f"unknown bucket '{bucket.get('localIdentifier')}'")
        for item in bucket.get("items") or []:
            if "measure" in item:
                measure = item["measure"]
                field = _measure_field(measure)
                alias = _alias("m_", field["using"], taken)
                alias_of[measure.get("localIdentifier")] = alias
            elif "attribute" in item:
                attribute = item["attribute"]
                label_id = (attribute.get("displayForm") or {}).get("identifier", {}).get("id")
                if not label_id:
                    raise Unsupported("attribute without a resolvable displayForm")
                field = {"using": f"label/{label_id}"}
                alias = _alias("d_", field["using"], taken)
                alias_of[attribute.get("localIdentifier")] = alias
            else:
                raise Unsupported(f"unknown bucket item ({', '.join(item) or 'empty'})")
            fields[alias] = field
            spec[target].append(alias)

    if not spec["metrics"]:
        raise Unsupported("no measures")

    converted = [_convert_filter(raw, alias_of) for raw in content.get("filters") or []]
    for i, entry in enumerate(f for f in converted if f is not None):
        spec["query"]["filter_by"][f"f{i}"] = entry
    spec["sort_by"] = _sorts(content, alias_of)

    _reject_degenerate(spec)
    spec["_shape"] = classify(spec, date_instance_ids)
    return spec


def ranks(spec: dict) -> bool:
    return bool(spec["sort_by"]) or any(f.get("type") == "ranking_filter" for f in spec["query"]["filter_by"].values())


def filters(spec: dict) -> bool:
    return any(f.get("type") in ("date_filter", "attribute_filter") for f in spec["query"]["filter_by"].values())


def _reject_degenerate(spec: dict) -> None:
    """Skip insights whose title promises behaviour their definition doesn't implement.

    A chart called "Products by Most Items Sold" with `sorts: []` and `filters: []` is a
    mis-specified object, not a fixture: any faithful question about its definition
    contradicts its name, and any question true to its name contradicts its
    `expected_output`. Excluding it is the only honest option.
    """
    title = spec["title"] or ""
    if RANK_WORDS.search(title) and not ranks(spec):
        raise Unsupported(f"title '{title}' promises a ranking the definition has no sort/ranking filter for")
    if FILTER_WORDS.search(title) and not filters(spec):
        raise Unsupported(f"title '{title}' promises a filter the definition has no date/attribute filter for")


def classify(spec: dict, date_instance_ids: set) -> str:
    """Question shape, for the coverage report.

    ponytail: first-match-wins heuristic -- a top-5 breakdown counts as `filtered_view`,
    not `breakdown_by_dimension`. Good enough to prove the corpus isn't all one type;
    replace with per-insight labels if the mix ever needs to be exact.
    """
    dims = spec["view_by"] + spec["segment_by"] + spec["columns"] + spec["rows"]
    fields = spec["query"]["fields"]
    filter_types = {f.get("type") for f in spec["query"]["filter_by"].values()}
    if filter_types & {"attribute_filter", "ranking_filter"}:
        return "filtered_view"
    if not dims:
        return "single_metric_callout"
    if any(field_uri(fields, a).split("/", 1)[-1].split(".", 1)[0] in date_instance_ids for a in dims):
        return "time_series"
    if spec["segment_by"] or len(spec["metrics"]) > 1:
        return "comparison"
    return "breakdown_by_dimension"


def fetch_snapshot(sdk, workspace_id: str) -> dict:
    """Two read-only SDK calls, assembled into a replayable JSON snapshot."""
    analytics = sdk.catalog_workspace_content.get_declarative_analytics_model(workspace_id).analytics.to_dict(
        camel_case=True
    )
    ldm = sdk.catalog_workspace_content.get_declarative_ldm(workspace_id).ldm.to_dict(camel_case=True)
    return {
        "workspace_id": workspace_id,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "analytics": analytics,
        "date_instance_ids": sorted(di["id"] for di in ldm.get("dateInstances") or []),
        "display_names": build_display_names(analytics, ldm),
    }


def insight_ids_on(analytics: dict, dashboard_ids: list) -> set:
    """Insight ids placed on the given dashboards, walking nested layout sections."""
    wanted = set(dashboard_ids)
    found = set()

    def walk(node):
        if isinstance(node, dict):
            if node.get("type") == "insight":
                identifier = (node.get("insight") or {}).get("identifier") or {}
                if identifier.get("id"):
                    found.add(identifier["id"])
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    for dashboard in analytics.get("analyticalDashboards") or []:
        if dashboard.get("id") in wanted:
            walk(dashboard.get("content") or {})
    return found


GRANULARITY_TITLES = {
    "minute": "Minute",
    "hour": "Hour",
    "day": "Day",
    "week": "Week",
    "month": "Month",
    "quarter": "Quarter",
    "year": "Year",
}


def build_display_names(analytics: dict, ldm: dict) -> dict:
    """`{uri: human title}` for every metric, fact, label and date dataset.

    Raw ids leak into question text otherwise ("the metric metric/m_units_sold"), which
    is both unreadable and a giveaway that no analyst wrote the question.
    """
    names = {}
    for metric in analytics.get("metrics") or []:
        names[f"metric/{metric['id']}"] = metric.get("title") or metric["id"]
    for dataset in ldm.get("datasets") or []:
        names[f"dataset/{dataset['id']}"] = dataset.get("title") or dataset["id"]
        for fact in dataset.get("facts") or []:
            names[f"fact/{fact['id']}"] = fact.get("title") or fact["id"]
        for attribute in dataset.get("attributes") or []:
            labels = attribute.get("labels") or []
            for label in labels:
                names[f"label/{label['id']}"] = label.get("title") or label["id"]
            if not labels:
                # An attribute with no explicit label is referenced by its own id.
                names[f"label/{attribute['id']}"] = attribute.get("title") or attribute["id"]
    for instance in ldm.get("dateInstances") or []:
        title = instance.get("title") or instance["id"]
        names[f"dataset/{instance['id']}"] = title
        for granularity in instance.get("granularities") or []:
            key = granularity.lower()
            names[f"label/{instance['id']}.{key}"] = f"{title} - {GRANULARITY_TITLES.get(key, granularity.title())}"
    return names


def display_name(uri: str, display_names: dict) -> str:
    """Human title for a URI, falling back to a de-slugged id."""
    if uri in display_names:
        return display_names[uri]
    for key, value in display_names.items():  # ids are case-inconsistent across LDM/AD
        if key.lower() == uri.lower():
            return value
    return uri.split("/", 1)[-1].replace(".", " - ").replace("_", " ").strip().title()


def _filter_phrase(f: dict, fields: dict, display_names: dict) -> str:
    """One filter, in words -- never raw JSON, which the writer would copy verbatim."""

    def resolve(alias: str) -> str:
        return display_name(field_uri(fields, alias), display_names)

    if f["type"] == "date_filter":
        on = display_name(f.get("using", ""), display_names)
        if isinstance(f.get("from"), str):
            return f"date range {f['from']} to {f['to']} on {on}"
        granularity = (f.get("granularity") or "period").lower()
        return (
            f"a relative {granularity} window from {f.get('from')} to {f.get('to')} "
            f"({granularity}s back from the current one, 0 = current) on {on}"
        )
    if f["type"] == "attribute_filter":
        on = display_name(f.get("using", ""), display_names)
        state = f.get("state") or {}
        if state.get("include"):
            return f"only these {on} values: {', '.join(state['include'])}"
        return f"excluding these {on} values: {', '.join(state.get('exclude') or [])}"
    if f["type"] == "ranking_filter":
        n = f.get("top") or f.get("bottom")
        end = "top" if "top" in f else "bottom"
        within = f", ranked within {resolve(f['attribute'])}" if f.get("attribute") else ""
        return f"{end} {n} by {resolve(f.get('using', ''))}{within}"
    return json.dumps(f)


def describe(spec: dict, display_names: dict | None = None) -> str:
    """The writer's brief: buckets, sorts and filters as display names.

    Deliberately excludes the insight title and the chart type. Titles describe intent
    the definition often doesn't implement, and every contradiction between a generated
    question and its `expected_output` traced back to one; the chart type is a UI choice
    the question isn't meant to constrain.
    """
    display_names = display_names or {}
    fields = spec["query"]["fields"]

    def name(alias: str) -> str:
        return display_name(field_uri(fields, alias), display_names)

    lines = [f"metric: {name(a)}" for a in spec["metrics"]]
    lines += [f"broken down by: {name(a)}" for a in spec["view_by"] + spec["columns"] + spec["rows"]]
    lines += [f"split by: {name(a)}" for a in spec["segment_by"]]
    lines += [f"sorted by: {name(s['field'])}, {s['direction'].lower()}ending" for s in spec["sort_by"]]
    lines += [f"filter: {_filter_phrase(f, fields, display_names)}" for f in spec["query"]["filter_by"].values()]
    return "\n".join(lines)


def field_uri(fields: dict, alias: str) -> str:
    """Resolve a bucket alias to its URI.

    A field may be `{"using": uri}` or a bare uri string (the AAC schema allows both),
    and an alias may already be a uri.
    """
    field = fields.get(alias)
    if field is None:
        return alias
    return field["using"] if isinstance(field, dict) else field


def _dim_names(spec: dict, display_names: dict) -> list:
    fields = spec["query"]["fields"]
    aliases = spec["view_by"] + spec["segment_by"] + spec["columns"] + spec["rows"]
    return [display_name(field_uri(fields, a), display_names) for a in aliases]


def _metric_names(spec: dict, display_names: dict) -> list:
    fields = spec["query"]["fields"]
    return [display_name(field_uri(fields, a), display_names) for a in spec["metrics"]]


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", "", text.lower()).strip()


def _mentions(name: str, question: str) -> bool:
    """Whether `question` names `name`, tolerating plurals and word order."""
    lowered = question.lower()
    tokens = [t for t in _normalize(name).split() if len(t) >= 4]
    return any(t in lowered for t in tokens) if tokens else _normalize(name) in lowered


def contradictions(question: str, spec: dict, display_names: dict | None = None) -> list:
    """Ways `question` and `spec` disagree. Any hit is a hard error, never a warning."""
    display_names = display_names or {}
    problems = []
    if not ranks(spec):
        hit = RANK_WORDS.search(question)
        if hit:
            problems.append(f"uses ranking word '{hit.group(0)}' but the chart has no sort or ranking filter")
    if not filters(spec):
        hit = FILTER_WORDS.search(question)
        if hit:
            problems.append(f"uses filter word '{hit.group(0)}' but the chart has no date or attribute filter")

    hit = PLACEHOLDER.search(question)
    if hit:
        problems.append(f"leaks the un-substituted placeholder '{hit.group(0)}'")

    dims = _dim_names(spec, display_names)
    clause = BY_CLAUSE.search(question)
    if clause:
        subject = _normalize(clause.group(1))
        echoes_metric = any(subject == _normalize(m) for m in _metric_names(spec, display_names))
        if echoes_metric and not ranks(spec):
            # "Show me X by X" -- the metric echoed into its own breakdown slot. Harmless
            # when the chart ranks, where "by <metric>" is how you say what it ranks on.
            problems.append(f"breaks down '{clause.group(1).strip()}' by itself; it is a metric, not a dimension")
        elif not dims and not NO_BREAKDOWN.search(question):
            problems.append(f"asks for a breakdown by '{clause.group(1).strip()}' but view_by and segment_by are empty")
    elif dims and not any(_mentions(d, question) for d in dims):
        # The inverse error: the chart breaks down, the question never says so.
        problems.append(f"names no dimension, but the chart breaks down by {', '.join(dims)}")
    return problems


def _rules_for(spec: dict, display_names: dict) -> str:
    dims = _dim_names(spec, display_names)
    segments = [display_name(field_uri(spec["query"]["fields"], a), display_names) for a in spec["segment_by"]]
    lines = [
        "Write the question an analyst would ask to get exactly this chart. Rules:",
        "- Name every metric listed above explicitly, using its name verbatim.",
    ]
    if dims:
        lines.append("- Say the question is broken down by " + ", ".join(dims) + ", naming each verbatim.")
    else:
        lines.append(
            "- This chart has NO breakdown. Ask for the metric on its own -- do not write "
            "'by ...', 'broken down by ...' or 'grouped by ...' at all. Never break a metric "
            "down by itself."
        )
    if segments:
        lines.append("- Say it is split by " + ", ".join(segments) + ".")
    lines += [
        "- State every filter and sort listed above in words (time period, included values, top/bottom N).",
        "- Claim NOTHING that is not listed above. If no sort or ranking is listed, do not say "
        "top/bottom/most/highest/lowest/ranked. If no filter is listed, do not restrict to a "
        "time period or a subset of values.",
        "- Write real names only. Never emit a literal word like 'breakdown dimension', 'metric' "
        "or 'dimension' as a stand-in for a name.",
        "- Do not name the chart type; the assistant should infer it.",
        "- Sound like a person asking a colleague, not like a chart title.",
        "- One sentence.",
    ]
    return "\n".join(lines)


def phrase(specs: list, model: str, display_names: dict) -> list:
    """Question per insight, or None where the writer kept contradicting the spec.

    One retry with the specific contradiction quoted back; a second failure drops the
    item rather than shipping a question its own `expected_output` disagrees with.
    """
    try:
        from openai import OpenAI  # noqa: PLC0415
    except ImportError as err:
        raise ImportError(
            "Question phrasing requires the llm-judge extra: uv add 'gooddata-eval[llm-judge]' (or pass --no-phrase)"
        ) from err
    if not os.environ.get("OPENAI_API_KEY"):
        raise OSError("OPENAI_API_KEY environment variable is required for the phrasing step.")

    client = OpenAI()
    questions = []
    for i, spec in enumerate(specs, 1):
        messages = [
            {"role": "system", "content": PHRASE_SYSTEM},
            {"role": "user", "content": f"{describe(spec, display_names)}\n\n{_rules_for(spec, display_names)}"},
        ]
        question, problems = None, []
        for _attempt in range(2):
            reply = client.chat.completions.create(model=model, messages=messages)
            candidate = reply.choices[0].message.content.strip().strip('"')
            problems = contradictions(candidate, spec, display_names)
            if not problems:
                question = candidate
                break
            messages += [
                {"role": "assistant", "content": candidate},
                {
                    "role": "user",
                    "content": "That question "
                    + "; and ".join(problems)
                    + ". Rewrite it describing only what the definition above actually contains.",
                },
            ]
        if question is None:
            print(f"  DROP {spec['title']}: {'; '.join(problems)}", file=sys.stderr)
        questions.append(question)
        print(f"  phrased {i}/{len(specs)}", file=sys.stderr)
    return questions


def resolve_type(spec: dict, question: str) -> str:
    """The insight's chart type, but only when the question actually names that form."""
    lowered = question.lower()
    return spec["type"] if any(w in lowered for w in TYPE_WORDS.get(spec["type"], ())) else ""


def build(spec: dict, question: str, dataset_name: str, existing_ids: set) -> dict:
    spec = {k: v for k, v in spec.items() if k != "_shape"}
    spec["type"] = resolve_type(spec, question)
    question_id = mint_id(question, existing_ids)
    existing_ids.add(question_id)
    return {
        "id": question_id,
        "dataset_name": dataset_name,
        "test_kind": TEST_KIND,
        "question": question,
        "expected_output": {"visualization": spec},
    }


def langfuse_payload(envelopes: list, dataset: str, workspace_id: str, origin: str, id_prefix: str = "") -> dict:
    """Langfuse-importable dataset JSON.

    `id_prefix` rewrites ids on export only: Langfuse item ids are unique per PROJECT,
    so importing the same item into a second dataset under its original id is a 409.
    """
    return {
        "dataset": dataset,
        "workspace": workspace_id,
        "items": [
            {
                "id": id_prefix + e["id"],
                "input": {"question": e["question"]},
                "expected_output": e["expected_output"],
                "metadata": {
                    "synthetic": True,
                    "test_kind": TEST_KIND,
                    "workspace": workspace_id,
                    "origin": origin,
                },
            }
            for e in envelopes
        ],
    }


def _validation_errors(envelope: dict) -> str | None:
    """The envelope must load as both a DatasetItem and a scorable AAC visualization."""
    try:
        DatasetItem.model_validate(envelope)
        CreatedVisualization.model_validate(envelope["expected_output"]["visualization"])
    except Exception as exc:  # pydantic ValidationError, or a missing key
        return str(exc)
    return None


def generate(args, sdk_factory=None) -> int:
    """Run the whole generation pipeline. Returns a process exit code."""
    if args.snapshot_in:
        snapshot = json.loads(Path(args.snapshot_in).read_text())
    else:
        sdk = sdk_factory()
        snapshot = fetch_snapshot(sdk, args.workspace)

    if args.snapshot_out:
        Path(args.snapshot_out).write_text(json.dumps(snapshot, indent=2))

    analytics = snapshot["analytics"]
    date_instance_ids = set(snapshot.get("date_instance_ids") or [])
    display_names = snapshot.get("display_names") or {}
    visualizations = analytics.get("visualizationObjects") or []
    if args.dashboard:
        keep = insight_ids_on(analytics, args.dashboard)
        if not keep:
            print(f"ERROR: no insights found on dashboard(s) {', '.join(args.dashboard)}", file=sys.stderr)
            return 1
        visualizations = [v for v in visualizations if v.get("id") in keep]

    specs, skipped = [], []
    for viz in visualizations:
        if viz.get("isHidden"):
            # Hidden objects are invisible to the AI assistant's catalog search, so a
            # question about one is unwinnable rather than merely hard.
            skipped.append((viz.get("id"), "hidden"))
            continue
        try:
            specs.append(convert(viz, date_instance_ids, display_names))
        except Unsupported as exc:
            skipped.append((viz.get("id"), str(exc)))

    shapes: dict[str, list] = {}
    for spec in specs:
        shapes.setdefault(spec["_shape"], []).append(spec["title"])

    n_filtered = sum(1 for s in specs if filters(s))
    n_ranked = sum(1 for s in specs if ranks(s))
    print(
        f"workspace {snapshot['workspace_id']}: {len(visualizations)} insights read, "
        f"{len(specs)} convertible, {len(skipped)} skipped"
    )
    for shape in SHAPES:
        print(f"  {shape:<24} {len(shapes.get(shape, []))}")
    print(f"  with filters             {n_filtered}")
    print(f"  with sort/ranking        {n_ranked}")
    for viz_id, reason in skipped:
        print(f"  SKIP {viz_id}: {reason}")

    failures = []
    if len(specs) < args.min_questions:
        failures.append(f"only {len(specs)} questions, need >= {args.min_questions}")
    if len(shapes) < args.min_shapes:
        failures.append(
            f"only {len(shapes)} distinct shapes ({', '.join(shapes) or 'none'}), need >= {args.min_shapes}"
        )
    if n_filtered < args.min_filtered:
        # With zero filtered items the eval can only punish a spurious filter, never
        # confirm the agent builds a required one -- half the behaviour goes untested.
        failures.append(
            f"only {n_filtered} items carry a filter, need >= {args.min_filtered}; "
            "point at dashboards whose insights actually filter"
        )
    for failure in failures:
        print(f"QUALITY GATE: {failure}", file=sys.stderr)
    if failures:
        print(
            "Not enough real insights to build a usable dataset -- nothing is fabricated to "
            "fill the gap. Point at more dashboards, or accept a smaller set with "
            "--min-questions/--min-shapes.",
            file=sys.stderr,
        )

    if args.dry_run:
        for spec in specs:
            print(f"\n[{spec['_shape']}] {spec['title']}\n{describe(spec, display_names)}")
        return 1 if failures else 0

    if args.no_phrase:
        questions = [f"Show {s['title']}" for s in specs]
    else:
        questions = phrase(specs, args.phrase_model, display_names)

    dropped = [spec["title"] for spec, q in zip(specs, questions) if q is None]
    specs, questions = zip(*[(s, q) for s, q in zip(specs, questions) if q]) if any(questions) else ([], [])
    if dropped:
        failures.append(f"{len(dropped)} question(s) dropped as self-contradictory: {', '.join(dropped[:5])}")
        print(f"DROPPED {len(dropped)} self-contradictory question(s)", file=sys.stderr)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    existing_ids = list_ids(out_dir)
    envelopes = [build(spec, q, args.dataset_name, existing_ids) for spec, q in zip(specs, questions)]
    if args.no_viz_type:
        for envelope in envelopes:
            envelope["expected_output"]["visualization"]["type"] = ""

    written = []
    for envelope in envelopes:
        path = out_dir / f"{envelope['id']}.json"
        path.write_text(json.dumps(envelope, indent=2) + "\n")
        written.append(path)
    print(f"wrote {len(written)} questions to {out_dir}")

    if args.langfuse_out:
        origin = (
            f"AUTO-GENERATED by reverse-engineering real insights in workspace "
            f"{snapshot['workspace_id']} -- expected_output copied from live "
            f"visualization definitions, question text written by "
            f"{'a mechanical template' if args.no_phrase else args.phrase_model}"
        )
        payload = langfuse_payload(envelopes, args.dataset_name, snapshot["workspace_id"], origin, args.id_prefix)
        Path(args.langfuse_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.langfuse_out).write_text(json.dumps(payload, indent=2) + "\n")
        print(f"wrote Langfuse dataset to {args.langfuse_out}")

    invalid = [(e["id"], err) for e in envelopes if (err := _validation_errors(e))]
    if invalid:
        print(f"VALIDATION FAILED for {len(invalid)} item(s):", file=sys.stderr)
        for item_id, err in invalid[:5]:
            print(f"  {item_id}: {err}", file=sys.stderr)
        return 1
    print(f"validated {len(written)}/{len(written)}")
    return 1 if failures else 0
