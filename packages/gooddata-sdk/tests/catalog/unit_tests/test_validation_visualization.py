# (C) 2026 GoodData Corporation
"""Offline visualization-content checks.

The fixtures below are shaped from real stored visualizations: the reference forms
(``attributeSortItem.attributeIdentifier``, ``measureSortItem.locators[].measureLocatorItem``,
``rankingFilter.measure.localIdentifier``) are the ones that actually occur, not invented
ones -- a validator tested only against hand-written content proves nothing about the
content it will meet.
"""

from __future__ import annotations

import json
from typing import Any

from gooddata_sdk.catalog.validation.model import Severity, ValidationError, ValidationReport
from gooddata_sdk.catalog.validation.visualization import (
    MAX_CONTENT_LENGTH,
    defined_local_ids,
    referenced_local_ids,
    validate_content,
    validate_content_length,
)


def _content(**overrides: Any) -> dict[str, Any]:
    """A valid two-bucket visualization: one measure, one attribute, sorted by the measure."""
    content: dict[str, Any] = {
        "version": "2",
        "visualizationUrl": "local:column",
        "buckets": [
            {
                "localIdentifier": "measures",
                "items": [
                    {
                        "measure": {
                            "localIdentifier": "m1",
                            "definition": {
                                "measureDefinition": {"item": {"identifier": {"id": "rev", "type": "metric"}}}
                            },
                        }
                    }
                ],
            },
            {
                "localIdentifier": "view",
                "items": [
                    {
                        "attribute": {
                            "localIdentifier": "a1",
                            "displayForm": {"identifier": {"id": "label.region", "type": "label"}},
                        }
                    }
                ],
            },
        ],
        "filters": [],
        "sorts": [
            {"measureSortItem": {"direction": "asc", "locators": [{"measureLocatorItem": {"measureIdentifier": "m1"}}]}}
        ],
        "properties": {},
    }
    content.update(overrides)
    return content


def _codes(findings: list[Any]) -> list[str]:
    return [f.code for f in findings]


class TestCleanContent:
    def test_a_well_formed_visualization_produces_no_findings(self):
        assert validate_content(_content()) == []

    def test_unknown_keys_are_not_reported(self):
        """The format gains fields without warning; an SDK that flagged them would report
        every object the day a new one ships."""
        assert validate_content(_content(someNewField={"a": 1})) == []

    def test_an_empty_sorts_and_filters_list_is_fine(self):
        assert validate_content(_content(sorts=[], filters=[])) == []


class TestLocalIdentifiers:
    def test_defined_ids_come_only_from_bucket_items(self):
        assert defined_local_ids(_content()) == {"m1", "a1"}

    def test_an_attribute_filters_own_local_id_does_not_define_a_bucket_item(self):
        """The filter's localIdentifier names the filter. Counting it as a definition would
        let a sort resolve against a filter and hide a genuinely dangling reference."""
        content = _content(
            filters=[
                {
                    "positiveAttributeFilter": {
                        "displayForm": {"identifier": {"id": "label.region", "type": "label"}},
                        "in": {"values": ["EU"]},
                        "localIdentifier": "filter-local-id",
                    }
                }
            ]
        )
        assert "filter-local-id" not in defined_local_ids(content)

    def test_a_sort_pointing_at_a_missing_bucket_item_is_an_error(self):
        content = _content(
            sorts=[{"measureSortItem": {"locators": [{"measureLocatorItem": {"measureIdentifier": "nope"}}]}}]
        )
        findings = validate_content(content)
        assert _codes(findings) == ["dangling_local_id"]
        assert findings[0].severity is Severity.ERROR
        assert "nope" in findings[0].message

    def test_an_attribute_sort_is_resolved_too(self):
        content = _content(sorts=[{"attributeSortItem": {"attributeIdentifier": "a1", "direction": "desc"}}])
        assert validate_content(content) == []
        content = _content(sorts=[{"attributeSortItem": {"attributeIdentifier": "ghost", "direction": "desc"}}])
        assert _codes(validate_content(content)) == ["dangling_local_id"]

    def test_a_ranking_filter_measure_is_resolved(self):
        content = _content(
            filters=[{"rankingFilter": {"measure": {"localIdentifier": "m1"}, "operator": "TOP", "value": 10}}]
        )
        assert validate_content(content) == []
        content = _content(
            filters=[{"rankingFilter": {"measure": {"localIdentifier": "gone"}, "operator": "TOP", "value": 10}}]
        )
        assert _codes(validate_content(content)) == ["dangling_local_id"]

    def test_measure_value_filter_dimensionality_is_resolved(self):
        content = _content(
            filters=[
                {
                    "measureValueFilter": {
                        "measure": {"localIdentifier": "m1"},
                        "dimensionality": [{"localIdentifier": "a1"}, {"localIdentifier": "missing"}],
                        "condition": {"comparison": {"operator": "GREATER_THAN", "value": 0}},
                    }
                }
            ]
        )
        findings = validate_content(content)
        assert _codes(findings) == ["dangling_local_id"]
        assert "dimensionality[1]" in findings[0].location

    def test_the_location_points_at_the_offending_element(self):
        content = _content(
            sorts=[
                {"attributeSortItem": {"attributeIdentifier": "a1"}},
                {"measureSortItem": {"locators": [{"measureLocatorItem": {"measureIdentifier": "bad"}}]}},
            ]
        )
        findings = validate_content(content)
        assert (
            findings[0].location == "content.sorts[1].measureSortItem.locators[0].measureLocatorItem.measureIdentifier"
        )

    def test_references_are_enumerated_by_shape(self):
        content = _content(filters=[{"rankingFilter": {"measure": {"localIdentifier": "m1"}}}])
        assert sorted(local_id for local_id, _ in referenced_local_ids(content)) == ["m1", "m1"]


class TestRequiredKeys:
    def test_a_missing_version_is_an_error(self):
        """version is required by the platform's own content model and is easy to omit when
        the content is written by hand rather than produced by the UI."""
        content = _content()
        del content["version"]
        findings = validate_content(content)
        assert _codes(findings) == ["missing_required_key"]
        assert findings[0].severity is Severity.ERROR

    def test_missing_buckets_and_url_are_both_reported(self):
        content = _content()
        del content["buckets"]
        del content["visualizationUrl"]
        assert _codes(validate_content(content)) == ["missing_required_key", "missing_required_key"]

    def test_missing_buckets_does_not_cascade_into_dangling_reference_noise(self):
        """Every reference dangles once the buckets are gone. Reporting each one would bury
        the single finding that explains them all."""
        content = _content()
        del content["buckets"]
        assert _codes(validate_content(content)) == ["missing_required_key"]

    def test_content_that_is_not_an_object_stops_there(self):
        """No point reporting a missing key on something that was never a content object."""
        assert _codes(validate_content([])) == ["content_not_an_object"]
        assert _codes(validate_content(None)) == ["content_not_an_object"]

    def test_buckets_of_the_wrong_type_is_an_error(self):
        assert "buckets_not_a_list" in _codes(validate_content(_content(buckets={})))


class TestUnknownValuesAreOnlyWarnings:
    """Chart types and bucket names are owned by the platform and gain members without
    notice. Erroring on them would turn every new chart type into an SDK bug."""

    def test_an_unknown_visualization_url_warns(self):
        findings = validate_content(
            _content(visualizationUrl="local:sunburst"), known_visualization_urls=frozenset({"local:column"})
        )
        assert _codes(findings) == ["unknown_visualization_url"]
        assert findings[0].severity is Severity.WARNING

    def test_an_unknown_bucket_name_warns(self):
        findings = validate_content(_content(), known_bucket_names=frozenset({"measures"}))
        assert _codes(findings) == ["unknown_bucket_name"]
        assert findings[0].severity is Severity.WARNING

    def test_without_a_known_set_the_value_is_not_checked_at_all(self):
        """None means "no opinion". An empty set would instead report every single object."""
        assert validate_content(_content(visualizationUrl="local:anything")) == []

    def test_an_unknown_version_warns_rather_than_errors(self):
        findings = validate_content(_content(version="3"))
        assert _codes(findings) == ["unknown_content_version"]
        assert findings[0].severity is Severity.WARNING


class TestContentLength:
    def test_content_within_the_limit_passes(self):
        assert validate_content_length(json.dumps(_content())) == []

    def test_content_over_the_limit_is_an_error(self):
        findings = validate_content_length("x" * (MAX_CONTENT_LENGTH + 1), object_id="big")
        assert _codes(findings) == ["content_too_long"]
        assert findings[0].object_id == "big"

    def test_the_limit_is_the_platform_limit_not_the_declarative_schemas(self):
        """The declarative OpenAPI advertises 15000 for this field because it reuses a
        generic JsonNode schema; the metadata model's own constant is 250000. Validating
        against the smaller number would reject content the platform accepts."""
        assert MAX_CONTENT_LENGTH == 250_000
        assert validate_content_length("x" * 20_000) == []


class TestReport:
    def test_warnings_alone_leave_the_report_passing(self):
        report = ValidationReport().extend(validate_content(_content(version="3")))
        assert report.warnings and not report.errors
        assert report.ok is True
        assert bool(report) is True
        report.raise_for_errors()

    def test_errors_make_it_fail_and_raise(self):
        content = _content()
        del content["version"]
        report = ValidationReport().extend(validate_content(content))
        assert report.ok is False
        assert not report
        try:
            report.raise_for_errors()
        except ValidationError as exc:
            assert exc.report is report
        else:
            raise AssertionError("raise_for_errors did not raise")

    def test_to_dict_is_serialisable(self):
        report = ValidationReport().extend(validate_content(_content(version="3"), object_id="v1"))
        as_dict = report.to_dict()
        assert as_dict["ok"] is True
        assert as_dict["findings"][0]["objectId"] == "v1"
        json.dumps(as_dict)

    def test_format_summarises_counts(self):
        report = ValidationReport().extend(validate_content([], object_id="v1"))
        assert "1 error(s), 0 warning(s)." in report.format()

    def test_an_empty_report_formats_as_ok(self):
        assert ValidationReport().format() == "OK: no findings."
