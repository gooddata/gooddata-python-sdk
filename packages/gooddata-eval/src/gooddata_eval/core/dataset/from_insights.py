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

from gooddata_sdk.catalog.workspace.aac import declarative_visualization_to_aac

from gooddata_eval.core.granularity import (
    GRANULARITIES,
    GRANULARITY_BY_ID,
    _camel,
    canonical_date_uri,
    granularity_of,
)
from gooddata_eval.core.models import CreatedVisualization, DatasetItem
from gooddata_eval.core.scoring import resolve_alias_to_uri, uri_to_display_name

# `GDC.time.week_us` converts to `WEEK_US`, which is not a platform granularity -- the
# SDK's own `_GRANULARITY_CONVERSION` maps it to `WEEK`. Override until the convertor is
# fixed; an expected_output carrying `WEEK_US` can never match what the agent builds.
# TODO(AIS-48): drop this once gooddata-code-convertors maps week_us to WEEK.
CONVERTOR_GRANULARITY_FIXES = {"WEEK_US": "WEEK"}

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
    "geo_chart": ("map", "pushpin"),
    "geo_area_chart": ("map", "choropleth", "area map"),
    "headline_chart": ("headline", "single number", "kpi", "big number"),
    "heatmap_chart": ("heatmap", "heat map"),
    "line_chart": ("line chart", "line graph"),
    "pie_chart": ("pie chart",),
    "pyramid_chart": ("pyramid chart",),
    "scatter_chart": ("scatter plot", "scatterplot"),
    "table": ("table",),
    "treemap_chart": ("treemap", "tree map"),
    "waterfall_chart": ("waterfall chart",),
}

RANK_WORDS = re.compile(
    r"\b(top|bottom|most|least|fewest|highest|lowest|largest|smallest|greatest|best|worst"
    r"|ranked|rank|limit it to)\b",
    re.I,
)
FILTER_WORDS = re.compile(
    r"\b(only|excluding|exclude|filtered|restricted to|limited to|just the"
    r"|last (?:year|quarter|month|week)|this (?:year|quarter|month|week)"
    r"|year to date|ytd|in \d{4})\b",
    re.I,
)

# Which end of the ranking a title names. A title using both ("Top and Bottom Products")
# names no single direction and is left alone.
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


def _reject_unscorable(spec: dict) -> None:
    """Skip an insight whose AAC form this evaluator cannot compare.

    Not a judgement on the insight -- the platform emitted it and it renders. These
    convert fine and then score wrong: a derived measure (previous period, arithmetic)
    is a field `using` another alias rather than an object, a measure-level filter lands
    on the field where `check_filters` never looks, and a repeater lists labels among its
    metrics. Teach the comparator about one and its line here can go.
    """
    fields = spec["query"]["fields"]
    for alias in spec["metrics"]:
        field = fields[alias]
        aggregated = False
        if isinstance(field, dict):
            if field.get("type"):
                raise Unsupported(f"derived measure ({field['type']})")
            if field.get("filter_by"):
                raise Unsupported("measure-level filters")
            aggregated = bool(field.get("aggregation"))
            field = field.get("using")
        if not isinstance(field, str):
            raise Unsupported("derived measure (arithmetic)")
        # `COUNT(attribute/x)` is a metric the agent builds and the scorer resolves; a bare
        # label with no aggregation is a repeater column, not something to compare.
        if not field.startswith(("metric/", "fact/")) and not aggregated:
            raise Unsupported(f"a label among the metrics ({field})")


def _to_aac(viz: dict) -> dict:
    """Declarative visualization -> AAC spec, via the SDK's convertor."""
    try:
        converted = declarative_visualization_to_aac(viz)
    except Exception as exc:  # ConversionError, and whatever else the WASM layer raises
        raise Unsupported(f"convertor rejected the definition: {exc}") from exc
    spec = converted.get("json")
    if spec is None:
        url = (viz.get("content") or {}).get("visualizationUrl")
        raise Unsupported(f"convertor produced no spec for visualizationUrl '{url}'")
    return spec


def _normalize_filters(raw: dict) -> dict:
    """Convertor `filter_by` -> the shape the evaluator compares, no-ops dropped.

    A no-op is AD's "All" selection -- an attribute filter with no `state`, or a date
    filter with no window. Both restrict nothing, and the convertor keeps them, which
    would let a question claim a filter its chart does not have.
    """
    out = {}
    for entry in raw.values():
        if entry.get("type") == "attribute_filter" and not any((entry.get("state") or {}).values()):
            continue
        if entry.get("type") == "date_filter":
            if entry.get("from") is None and entry.get("to") is None:
                continue
            using = entry.get("using")
            granularity = entry.get("granularity")
            entry = {
                **entry,
                # The convertor emits a bare dataset id; every other uri in the spec, and
                # everything the agent emits, carries its type prefix.
                "using": using if str(using).startswith("dataset/") else f"dataset/{using}",
            }
            if granularity is not None:
                entry["granularity"] = CONVERTOR_GRANULARITY_FIXES.get(granularity, granularity)
        out[f"f{len(out)}"] = entry
    return out


def convert(viz: dict) -> dict:
    """Declarative visualization object -> AAC `visualization` spec. Raises `Unsupported`."""
    if any(b.get("localIdentifier") == "location" for b in (viz.get("content") or {}).get("buckets") or []):
        # The one thing read off the declarative object. A map's location is a rendering
        # label (`city_pushpin_latitude`) that AAC files under `view_by` like any other
        # dimension, and a question built from it reads "broken down by City pushpin
        # latitude". The bucket name is the only exact marker.
        raise Unsupported("unknown bucket 'location'")
    aac = _to_aac(viz)
    query = aac.get("query") or {}
    spec: dict[str, Any] = {
        "id": re.sub(r"[^a-z0-9_]+", "_", (viz.get("id") or "viz").lower())[:30],
        "type": aac["type"],
        "title": viz.get("title") or viz.get("id"),
        "query": {
            "fields": query.get("fields") or {},
            "filter_by": _normalize_filters(query.get("filter_by") or {}),
            "sort_by": query.get("sort_by") or [],
        },
        "metrics": aac.get("metrics") or [],
        "view_by": aac.get("view_by") or [],
        "segment_by": aac.get("segment_by") or [],
        "columns": aac.get("columns") or [],
        "rows": aac.get("rows") or [],
    }
    for bucket in ("metrics", "view_by", "segment_by", "rows", "columns"):
        # A bucket item is an alias, or `{"field": alias, ...}` carrying `format`, `axis`,
        # `totals` or `display_as` -- presentation, which nothing here or in the scorer reads.
        spec[bucket] = [item["field"] if isinstance(item, dict) else item for item in spec[bucket]]
    if not spec["metrics"]:
        raise Unsupported("no measures")
    _reject_unscorable(spec)
    return spec


def sorts_of(spec: dict) -> list:
    """The spec's sort entries."""
    return spec["query"].get("sort_by") or []


def _sort_field(sort: dict) -> str:
    """The alias a sort entry orders on, whichever key its type puts it under."""
    return sort["by"] if sort.get("type") == "attribute_sort" else sort["metrics"][0]


def ranks(spec: dict) -> bool:
    return bool(sorts_of(spec)) or any(f.get("type") == "ranking_filter" for f in spec["query"]["filter_by"].values())


def filters(spec: dict) -> bool:
    return any(f.get("type") in ("date_filter", "attribute_filter") for f in spec["query"]["filter_by"].values())


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
            enum = GRANULARITY_BY_ID.get(granularity, granularity.upper())
            suffix = GRANULARITIES.get(enum, (granularity.title(), ""))[0]
            # Registered under every spelling: the LDM declares MONTH_OF_YEAR, the API
            # returns `monthOfYear`, and a lookup under one must not miss the other and
            # fall back to a de-slugged id ("Order Created At - Monthofyear").
            for spelling in {_camel(enum), enum.lower(), granularity}:
                names[f"label/{instance['id']}.{spelling}"] = f"{title} - {suffix}"
    return names


def display_name(uri: str, display_names: dict) -> str:
    """Human title for a URI, falling back to a de-slugged id."""
    if uri in display_names:
        return display_names[uri]
    for key, value in display_names.items():  # ids are case-inconsistent across LDM/AD
        if key.lower() == uri.lower():
            return value
    return uri_to_display_name(uri).strip().title()


def _filter_phrase(f: dict, fields: dict, display_names: dict) -> str:
    """One filter, in words -- never raw JSON, which the writer would copy verbatim."""

    def resolve(alias: str) -> str:
        return display_name(resolve_alias_to_uri(alias, fields), display_names)

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
        return display_name(resolve_alias_to_uri(alias, fields), display_names)

    def dim(aliases: list) -> list:
        return _dim_briefs(spec, display_names, aliases)

    lines = [f"metric: {name(a)}" for a in spec["metrics"]]
    lines += [f"broken down by: {d}" for d in dim(spec["view_by"] + spec["columns"] + spec["rows"])]
    lines += [f"split by: {d}" for d in dim(spec["segment_by"])]
    lines += [f"sorted by: {name(_sort_field(s))}, {s['direction'].lower()}ending" for s in sorts_of(spec)]
    lines += [f"filter: {_filter_phrase(f, fields, display_names)}" for f in spec["query"]["filter_by"].values()]
    return "\n".join(lines)


def ambiguous_titles(display_names: dict) -> set:
    """Display titles that more than one object in the model carries.

    Loop has six labels all titled "Product Title". A question naming one of them cannot
    say which is meant, so the expected dimension is unguessable and the item punishes a
    defensible answer -- `label/product_title_at_time_of_return` instead of
    `label/product_details.LINE_ITEM_TITLE` scored zero on an otherwise perfect chart.
    """
    seen, dupes = {}, set()
    for uri, title in display_names.items():
        # Every granularity is registered under several spellings of one label, so the
        # aliases must fold together or each date dimension looks like a name collision.
        canonical = canonical_date_uri(uri)
        key = _normalize(title)
        if key in seen and seen[key] != canonical:
            dupes.add(key)
        seen.setdefault(key, canonical)
    return dupes


def ambiguous_fields(spec: dict, display_names: dict, dupes: set | None = None) -> list:
    """The display names in `spec` that do not identify one object in the model."""
    dupes = ambiguous_titles(display_names) if dupes is None else dupes
    names = _metric_names(spec, display_names) + _dim_names(spec, display_names)
    return sorted({name for name in names if _normalize(name) in dupes})


def granularity_phrase(uri: str, display_names: dict) -> str | None:
    """What a date breakdown does, in words, or None if `uri` is not a date granularity.

    "Order Created At - Month" is a label name, not something a person says, and it does
    not distinguish the sequential granularity from its cyclical twin. The phrase does
    both: it pins the date dataset and states which reading is meant.
    """
    enum = granularity_of(uri)
    if enum is None:
        return None
    dataset = uri.split("/", 1)[-1].rpartition(".")[0]
    return f"{display_name(f'dataset/{dataset}', display_names)}, {GRANULARITIES[enum][1]}"


def _dim_briefs(spec: dict, display_names: dict, aliases: list) -> list:
    """Dimension names for the writer: date dimensions as phrases, labels verbatim."""
    fields = spec["query"]["fields"]
    out = []
    for alias in aliases:
        uri = resolve_alias_to_uri(alias, fields)
        out.append(granularity_phrase(uri, display_names) or display_name(uri, display_names))
    return out


def _dim_names(spec: dict, display_names: dict) -> list:
    fields = spec["query"]["fields"]
    aliases = spec["view_by"] + spec["segment_by"] + spec["columns"] + spec["rows"]
    return [display_name(resolve_alias_to_uri(a, fields), display_names) for a in aliases]


def _metric_names(spec: dict, display_names: dict) -> list:
    fields = spec["query"]["fields"]
    return [display_name(resolve_alias_to_uri(a, fields), display_names) for a in spec["metrics"]]


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", "", text.lower()).strip()


def _mentions(name: str, question: str) -> bool:
    """Whether `question` names `name`, tolerating plurals and word order."""
    lowered = question.lower()
    tokens = [t for t in _normalize(name).split() if len(t) >= 4]
    return any(t in lowered for t in tokens) if tokens else _normalize(name) in lowered


def _without_field_names(question: str, spec: dict, display_names: dict) -> str:
    """`question` with the spec's own field names blanked out.

    A field may be called "Most Recent Label Created At" or "Top Tier Customers". A
    question naming it verbatim -- which the rules require -- is not thereby claiming a
    ranking, so the claim checks have to read around the names.
    """
    fields = spec["query"]["fields"]
    names = [display_name(resolve_alias_to_uri(a, fields), display_names) for a in fields]
    names += [display_name(f.get("using", ""), display_names) for f in spec["query"]["filter_by"].values()]
    # A date label reads "Most Recent Label Created At - Month" but the question names
    # the dataset and the granularity separately ("by month for Most Recent Label
    # Created At"), so each side of the separator has to be maskable on its own.
    names += [part for name in list(names) for part in name.split(" - ")]
    for name in sorted(names, key=len, reverse=True):
        if len(name.strip()) > 3:
            question = re.sub(re.escape(name.strip()), " ", question, flags=re.I)
    return question


def contradictions(question: str, spec: dict, display_names: dict | None = None) -> list:
    """Ways `question` and `spec` disagree. Any hit is a hard error, never a warning."""
    display_names = display_names or {}
    problems = []
    claims = _without_field_names(question, spec, display_names)
    if not ranks(spec):
        hit = RANK_WORDS.search(claims)
        if hit:
            problems.append(f"uses ranking word '{hit.group(0)}' but the chart has no sort or ranking filter")
    if not filters(spec):
        hit = FILTER_WORDS.search(claims)
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
    all_dims = spec["view_by"] + spec["segment_by"] + spec["columns"] + spec["rows"]
    dated = [
        phrase
        for alias in all_dims
        if (phrase := granularity_phrase(resolve_alias_to_uri(alias, spec["query"]["fields"]), display_names))
    ]
    segments = [
        display_name(resolve_alias_to_uri(a, spec["query"]["fields"]), display_names) for a in spec["segment_by"]
    ]
    lines = [
        "Write the question an analyst would ask to get exactly this chart. Rules:",
        "- Name every metric listed above explicitly, using its name verbatim.",
    ]
    ranking = next((f for f in spec["query"]["filter_by"].values() if f.get("type") == "ranking_filter"), None)
    # A ranking filter with no `attribute` ranks over the full dimension tuple, so the
    # "top N <dimension>" shorthand is only true when there is exactly one dimension.
    # With two, naming one tells the writer a scope the filter does not have -- "top 5
    # Customer State, split by City" reads as within-state, and the agent obliges.
    ranked_dim = dims[0] if ranking and len(dims) == 1 and not ranking.get("attribute") else None
    if ranking is not None and ranked_dim:
        # The ranking phrasing already names the dimension. Asking for the breakdown as
        # well produces "broken down by Carrier, showing the top 3 Carriers by Returns" --
        # the dimension twice, which no analyst writes. One instruction, not two.
        n = ranking.get("top") or ranking.get("bottom")
        end = "top" if "top" in ranking else "bottom"
        lines.append(
            f"- This chart keeps only the {end} {n} rows of {ranked_dim}. Ask for 'the {end} {n} "
            f"{ranked_dim} by <metric>' and name {ranked_dim} exactly once -- do not also say "
            f"'broken down by {ranked_dim}'."
        )
    elif dated:
        # A date breakdown is the one dimension not to quote verbatim: "broken down by
        # Order Created At - Month" is a label id in prose, and it leaves the agent to
        # guess between the sequential granularity and its cyclical twin.
        plain = [name for name in dims if not any(name.startswith(p.split(",")[0]) for p in dated)]
        lines.append(
            "- Say the question is broken down by " + "; and ".join(dated) + ". Write that in "
            "natural words ('by month', 'monthly', 'per month'), never as a label name like "
            "'Order Created At - Month', but do keep the date dataset's name."
        )
        if plain:
            lines.append("- It is also broken down by " + ", ".join(plain) + ", naming each verbatim.")
    elif dims:
        lines.append("- Say the question is broken down by " + ", ".join(dims) + ", naming each verbatim.")
    else:
        lines += [
            "- This chart has NO breakdown. Ask for the metric on its own -- do not write "
            "'by ...', 'broken down by ...' or 'grouped by ...' at all. Never break a metric "
            "down by itself.",
            # "What is the Upsell Ratio?" is answered as a definition, and "Show me Gross
            # Revenue" is answered by looking the metric up -- the agent activates only its
            # search skill and builds nothing. Naming the chart form is what makes a bare
            # metric a charting request, so a no-breakdown question has to name it.
            "- Ask for it AS A CHART, naming the form: 'as a single number', 'as a KPI' or "
            "'as a headline'. Never a bare 'What is <metric>?' (answered as a definition) and "
            "never a bare 'Show me <metric>' (answered by looking the metric up).",
        ]
    if segments:
        lines.append("- Say it is split by " + ", ".join(segments) + ".")
    lines += [
        "- State every filter and sort listed above in words (time period, included values, top/bottom N).",
        "- Claim NOTHING that is not listed above. If no sort or ranking is listed, do not say "
        "top/bottom/most/highest/lowest/ranked. If no filter is listed, do not restrict to a "
        "time period or a subset of values.",
        "- Write real names only. Never emit a literal word like 'breakdown dimension', 'metric' "
        "or 'dimension' as a stand-in for a name.",
        # A single-metric chart is the exception: without a named form the request is
        # indistinguishable from a metric lookup, so there the form is the question.
        *([] if not dims else ["- Do not name the chart type; the assistant should infer it."]),
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
        messages: list = [
            {"role": "system", "content": PHRASE_SYSTEM},
            {"role": "user", "content": f"{describe(spec, display_names)}\n\n{_rules_for(spec, display_names)}"},
        ]
        question, problems = None, []
        for _attempt in range(2):
            reply = client.chat.completions.create(model=model, messages=messages)
            # `content` is None when the model returns a refusal or no text at all; an
            # empty candidate fails the contradiction check and takes the retry, which is
            # what should happen anyway.
            candidate = (reply.choices[0].message.content or "").strip().strip('"')
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
    spec = {**spec, "type": resolve_type(spec, question)}
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
                "metadata": {"synthetic": True, "test_kind": TEST_KIND, "workspace": workspace_id, "origin": origin},
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
        if sdk_factory is None:
            raise ValueError("a live run needs an SDK; pass --snapshot-in to replay a saved model instead")
        snapshot = fetch_snapshot(sdk_factory(), args.workspace)
    if args.snapshot_out:
        Path(args.snapshot_out).write_text(json.dumps(snapshot, indent=2))

    analytics = snapshot["analytics"]
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
            specs.append(convert(viz))
        except Unsupported as exc:
            skipped.append((viz.get("id"), str(exc)))

    dupes = ambiguous_titles(display_names)
    ambiguous = [(spec, names) for spec in specs if (names := ambiguous_fields(spec, display_names, dupes))]
    if args.skip_ambiguous:
        drop = {id(spec) for spec, _ in ambiguous}
        specs = [spec for spec in specs if id(spec) not in drop]

    n_filtered = sum(1 for s in specs if filters(s))
    print(
        f"workspace {snapshot['workspace_id']}: {len(visualizations)} insights read, "
        f"{len(specs)} convertible, {len(skipped)} skipped"
    )
    print(f"  with filters             {n_filtered}")
    print(f"  with sort/ranking        {sum(1 for s in specs if ranks(s))}")
    if ambiguous:
        verb = "dropped" if args.skip_ambiguous else "kept"
        print(
            f"  ambiguous field names    {len(ambiguous)} item(s) {verb}: a name below matches "
            f"more than one object in the model, so the question cannot say which is meant"
        )
        for spec, names in ambiguous[:5]:
            print(f"    {spec['title'][:40]:<40} {', '.join(names)}")
        if len(ambiguous) > 5:
            print(f"    ... and {len(ambiguous) - 5} more")
        if not args.skip_ambiguous:
            print("    pass --skip-ambiguous to exclude them", file=sys.stderr)
    for viz_id, reason in skipped:
        print(f"  SKIP {viz_id}: {reason}")

    failures = []
    if len(specs) < args.min_questions:
        failures.append(f"only {len(specs)} questions, need >= {args.min_questions}")
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
            "fill the gap. Point at more dashboards, or accept a smaller set with --min-questions.",
            file=sys.stderr,
        )

    if args.dry_run:
        for spec in specs:
            print(f"\n{spec['title']}\n{describe(spec, display_names)}")
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

    for envelope in envelopes:
        (out_dir / f"{envelope['id']}.json").write_text(json.dumps(envelope, indent=2) + "\n")
    print(f"wrote {len(envelopes)} questions to {out_dir}")

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
    print(f"validated {len(envelopes)}/{len(envelopes)}")
    return 1 if failures else 0
