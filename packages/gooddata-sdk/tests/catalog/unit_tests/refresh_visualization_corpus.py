#!/usr/bin/env python3
# (C) 2026 GoodData Corporation
"""Regenerate ``fixtures_visualization_corpus.json`` from a real workspace.

The corpus exists so the checks are tested against content the product actually produces
rather than content invented to pass them -- a validator proven only against hand-written
fixtures proves nothing about what it will meet. That means it has to be refreshable when
the format moves, which is what this script is for.

It is not a test and CI does not run it: it needs a workspace and credentials. Run it by
hand and commit the result.

    GOODDATA_HOST=... GOODDATA_TOKEN=... python refresh_visualization_corpus.py <workspace>

**Anonymisation is default-deny, and that is the point.** A string survives only if its key
is structural or its value is a recognised enum; everything else is replaced by a hash of
itself. The alternative -- listing the fields that carry customer data and scrubbing those
-- was tried first and leaked four times: `tags`, then the geo `latitude`/`longitude`/
`tooltipText` fields, then whole MAQL statements embedded in measure definitions, and
finally filter element values together with a colour identifier sitting in a plain list of
strings. The last of those reached a public repository before it was caught.

Read that list again before adding an exception to the rule below. Every one of those
leaks was a place the rule did not reach, not a rule that was wrong: strings in lists went
unjudged, and object keys were assumed to be field names. Both are now judged the same way
as everything else, and `test_validation_corpus.py` asserts structurally -- every value a
hash or known vocabulary, every key a field name -- rather than scanning for words somebody
thought of in advance, which is what let all four through.

What survives is exactly what the checks read: field names, bucket names, chart types,
local identifiers and the shape of the references between them.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

_OUTPUT = Path(__file__).parent / "fixtures_visualization_corpus.json"

# Keys whose string values name a structure rather than describe data.
_ID_KEYS = frozenset({"id", "localIdentifier", "attributeIdentifier", "measureIdentifier"})

# Bucket names are part of the structure under test, so they must survive verbatim -- they
# are also the one place a "localIdentifier" is a fixed vocabulary word rather than a
# generated id.
_BUCKET_NAMES = frozenset(
    {
        "measures",
        "secondary_measures",
        "tertiary_measures",
        "attribute",
        "attribute_from",
        "attribute_to",
        "attributes",
        "view",
        "stack",
        "trend",
        "segment",
        "columns",
        "location",
        "longitude",
        "latitude",
        "size",
        "color",
        "tooltipText",
    }
)

# Keys whose values are drawn from a fixed vocabulary and carry nothing about the customer.
_ENUM_KEYS = frozenset({"type", "visualizationUrl", "version", "direction", "operator", "granularity", "aggregation"})


# Objects whose *keys* are identifiers rather than vocabulary: `attributeFilterConfigs`
# maps a filter's local identifier to its configuration and `inlineVisualizations` maps a
# measure's, so in both the key is customer data, even though every key elsewhere in the
# format is a field name.
_ID_KEYED_OBJECTS = frozenset({"attributeFilterConfigs", "inlineVisualizations"})

# A key shaped like a generated identifier is treated as data whatever it hangs under.
# The list above can only name the id-keyed objects that are known; this catches the next
# one, which is the failure mode this whole script keeps meeting.
_ID_SHAPED_KEY = re.compile(r"^[0-9a-f]{8}-?(?:[0-9a-f]{4}-?){3}[0-9a-f]{12}$", re.IGNORECASE)


def _anonymise(value: str) -> str:
    return "obj_" + hashlib.sha1(value.encode()).hexdigest()[:10]  # noqa: S324 - not a security hash


def _scrub_string(value: str, key: str | None) -> str:
    """Decide one string's fate from the key it arrived under.

    Split out so that a string in a list is judged by exactly the same rule as a string
    under a key -- see :func:`_scrub`.
    """
    if key in _ENUM_KEYS:
        return value
    if key in _ID_KEYS:
        return value if value in _BUCKET_NAMES else _anonymise(value)
    # Default-deny: titles, aliases, MAQL, tags, geo field names, filter element values and
    # anything the format gains next all land here.
    return _anonymise(value)


def _scrub(node: Any, key: str | None = None) -> Any:
    """Anonymise a content tree, judging every string by the key it hangs under.

    The key is carried into lists rather than stopped at their boundary. It used to stop
    there: a string *inside* a list was returned untouched unless its key happened to be
    `values`, which had a special case of its own. That hole published a workspace's colour
    palette identifier out of `secondary_yaxis.measures`, a plain list of strings, and it
    would have published anything else the format ever puts in a bare list. A rule with one
    exception is a rule with one hole, so there is now no exception: a string is judged the
    same way wherever it is found.
    """
    if isinstance(node, dict):
        scrubbed: dict[str, Any] = {}
        for node_key, value in node.items():
            # Almost every key in this format is a field name. The exceptions map an
            # identifier to its configuration, so their keys are data.
            is_data_key = key in _ID_KEYED_OBJECTS or _ID_SHAPED_KEY.match(node_key)
            out_key = _anonymise(node_key) if is_data_key else node_key
            scrubbed[out_key] = _scrub_string(value, node_key) if isinstance(value, str) else _scrub(value, node_key)
        return scrubbed
    if isinstance(node, list):
        return [_scrub_string(item, key) if isinstance(item, str) else _scrub(item, key) for item in node]
    return node


def build_corpus(visualizations: list[dict[str, Any]], *, per_chart_type: int = 2) -> list[dict[str, Any]]:
    """Pick a spread of real visualizations and anonymise them.

    Up to ``per_chart_type`` of each chart type, preferring the ones carrying the most sorts
    and filters -- those exercise the reference shapes the checks actually walk, and a
    corpus of simple charts would pass without proving anything.
    """
    by_type: dict[Any, list[dict[str, Any]]] = {}
    for visualization in visualizations:
        by_type.setdefault(visualization["content"].get("visualizationUrl"), []).append(visualization)

    picked: list[dict[str, Any]] = []
    for _, group in sorted(by_type.items(), key=lambda item: str(item[0])):
        group.sort(
            key=lambda v: -(len(v["content"].get("sorts") or []) + len(v["content"].get("filters") or [])),
        )
        picked.extend(group[:per_chart_type])

    return [{"id": _anonymise(v["id"]), "content": _scrub(v["content"])} for v in picked]


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    workspace_id = sys.argv[1]
    host, token = os.environ.get("GOODDATA_HOST"), os.environ.get("GOODDATA_TOKEN")
    if not host or not token:
        print("GOODDATA_HOST and GOODDATA_TOKEN are required.")
        return 2

    from gooddata_sdk import GoodDataSdk  # noqa: PLC0415 - keeps the module importable without the SDK configured

    sdk = GoodDataSdk.create(host, token)
    model = sdk.catalog_workspace_content.get_declarative_analytics_model(workspace_id)
    visualizations = [
        {"id": v.id, "content": v.content} for v in (model.analytics.visualization_objects if model.analytics else [])
    ]
    corpus = build_corpus(visualizations)

    _OUTPUT.write_text(json.dumps(corpus, indent=1, sort_keys=True) + "\n")
    chart_types = sorted({obj["content"].get("visualizationUrl") for obj in corpus})
    print(f"wrote {len(corpus)} object(s) covering {len(chart_types)} chart type(s) to {_OUTPUT.name}")
    print("Review the diff before committing: this is the last line of defence.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
