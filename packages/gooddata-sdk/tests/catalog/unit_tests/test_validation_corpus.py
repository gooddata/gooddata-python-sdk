# (C) 2026 GoodData Corporation
"""The checks must stay silent on content the product itself produces.

A validator that reports healthy objects is worse than none: the reports get ignored, then
the validator gets switched off. These fixtures are real visualizations exported from a
live workspace -- every chart type it contained, preferring the ones carrying the most
sorts and filters -- so a change that starts flagging ordinary content fails here.

The fixtures are anonymised: every string is replaced with a hash of itself unless its key
is structural or its value is a known enum. That is default-deny on purpose, so a field
nobody thought about cannot carry a customer's metric names into the repository. What
survives is exactly what the checks read -- keys, bucket names, local identifiers, and the
shape of the references between them.
"""

from __future__ import annotations

import copy
import json
import re
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest
from gooddata_sdk.catalog.validation.references import extract_catalog_references, resolve_references
from gooddata_sdk.catalog.validation.visualization import validate_content

_CORPUS_PATH = Path(__file__).parent / "fixtures_visualization_corpus.json"


def _corpus() -> list[dict[str, Any]]:
    return json.loads(_CORPUS_PATH.read_text())


def _ids(corpus: list[dict[str, Any]]) -> list[str]:
    return [obj["id"] for obj in corpus]


class TestRealContentPassesCleanly:
    @pytest.mark.parametrize("obj", _corpus(), ids=_ids(_corpus()))
    def test_each_stored_visualization_produces_no_findings(self, obj):
        assert validate_content(obj["content"], object_id=obj["id"]) == []

    def test_the_corpus_covers_the_shapes_worth_covering(self):
        """A corpus of eight copies of the same chart would pass without proving anything."""
        corpus = _corpus()
        chart_types = {obj["content"].get("visualizationUrl") for obj in corpus}
        bucket_names = {
            bucket.get("localIdentifier")
            for obj in corpus
            for bucket in obj["content"].get("buckets", [])
            if isinstance(bucket, dict)
        }
        assert len(chart_types) >= 8
        assert len(bucket_names) >= 6
        assert sum(len(obj["content"].get("filters") or []) for obj in corpus) >= 20
        assert sum(len(obj["content"].get("sorts") or []) for obj in corpus) >= 5

    def test_the_corpus_carries_catalog_references_to_resolve(self):
        assert sum(len(extract_catalog_references(obj["content"])) for obj in _corpus()) >= 50

    def test_every_reference_resolves_when_the_catalog_has_it(self):
        corpus = _corpus()
        effective = {ref.obj_id for obj in corpus for ref in extract_catalog_references(obj["content"])}
        for obj in corpus:
            findings, _ = resolve_references(
                extract_catalog_references(obj["content"]), effective_ids=effective, object_id=obj["id"]
            )
            assert findings == []


class TestTheCorpusWouldCatchARegression:
    """A corpus that only ever passes cannot distinguish working checks from disabled ones."""

    def test_breaking_a_reference_in_real_content_is_caught(self):
        obj = next(o for o in _corpus() if o["content"].get("sorts"))
        content = copy.deepcopy(obj["content"])
        sort = content["sorts"][0]
        if "attributeSortItem" in sort:
            sort["attributeSortItem"]["attributeIdentifier"] = "not-a-bucket-item"
        else:
            sort["measureSortItem"]["locators"][0]["measureLocatorItem"]["measureIdentifier"] = "not-a-bucket-item"
        assert [f.code for f in validate_content(content)] == ["dangling_local_id"]

    def test_removing_a_required_key_from_real_content_is_caught(self):
        content = copy.deepcopy(_corpus()[0]["content"])
        del content["version"]
        assert [f.code for f in validate_content(content)] == ["missing_required_key"]

    def test_a_missing_catalog_object_is_caught(self):
        obj = _corpus()[0]
        refs = extract_catalog_references(obj["content"])
        findings, resolution = resolve_references(refs, effective_ids=set(), object_id=obj["id"])
        assert len(findings) == len([r for r in refs if r.type in {"metric", "label", "dataset", "attribute", "fact"}])
        assert resolution.resolved_count == 0


# Everything a string in this fixture is allowed to be, beyond a hash or a `local:` chart
# type: bucket names, the enumerated values the format draws on, and the content version.
_STRUCTURAL_VALUES = frozenset(
    {
        "2",
        "table",
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
        "asc",
        "desc",
        "label",
        "metric",
        "fact",
        "dataset",
        "guid",
        "rgb",
        "rows",
        "TOP",
        "BOTTOM",
        "sum",
        "avg",
        "max",
        "min",
        "med",
        "nat",
        "DAY",
        "WEEK",
        "MONTH",
        "QUARTER",
        "YEAR",
        "GREATER_THAN",
        "LESS_THAN",
    }
)

_FIELD_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _strings(node: Any, *, keys: bool) -> Iterator[str]:
    if isinstance(node, dict):
        for key, value in node.items():
            if keys:
                yield key
            yield from _strings(value, keys=keys)
    elif isinstance(node, list):
        for item in node:
            yield from _strings(item, keys=keys)
    elif isinstance(node, str) and not keys:
        yield node


class TestFixturesCarryNoCustomerData:
    """The fixture is built from a real workspace and lives in a public repository, so the
    anonymisation is the only thing between a customer's content and the internet.

    This is asserted structurally -- everything must be a hash or known vocabulary -- and
    deliberately not as a list of forbidden words. The word list was what was here before,
    and it is the same allowlist thinking that let four separate leaks through: `tags`,
    then the geo fields, then embedded MAQL, then filter element values and a colour
    identifier sitting in a plain list. A word list can only catch what someone thought of.
    """

    def test_every_value_is_a_hash_or_known_vocabulary(self):
        unexpected = {
            value
            for value in _strings(_corpus(), keys=False)
            if not (value.startswith(("obj_", "local:")) or value in _STRUCTURAL_VALUES)
        }
        assert unexpected == set(), f"un-anonymised values in the fixture: {sorted(unexpected)}"

    def test_every_key_is_a_field_name(self):
        """Two objects in this format are keyed by identifier rather than by field name --
        `attributeFilterConfigs` and `inlineVisualizations` -- so a key can be data too."""
        unexpected = {key for key in _strings(_corpus(), keys=True) if not _FIELD_NAME.match(key)}
        assert unexpected == set(), f"un-anonymised keys in the fixture: {sorted(unexpected)}"
