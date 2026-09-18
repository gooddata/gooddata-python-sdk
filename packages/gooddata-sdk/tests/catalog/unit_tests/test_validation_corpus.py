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


class TestFixturesCarryNoCustomerData:
    def test_no_identifier_survives_unhashed(self):
        """Guards the anonymisation itself: a future refresh that forgets to scrub a new
        field would put real metric names into the repository."""
        blob = _CORPUS_PATH.read_text().lower()
        for token in ("mastercard", "micai", "merchant", "spend", "acquirer", "issuer", "select "):
            assert token not in blob
