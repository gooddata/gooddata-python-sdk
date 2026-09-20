# (C) 2026 GoodData Corporation
"""Bucket names against the chart type that carries them.

The restraint is the point here. The table says only what the platform's execution
converter can be read to say -- which bucket each chart type takes each dimension from --
so a good half of these tests are about what the check declines to say.
"""

from __future__ import annotations

from typing import Any

from gooddata_sdk.catalog.validation.buckets import (
    BUCKET_NAMES,
    BUCKETS_BY_VISUALIZATION,
    VISUALIZATION_NAMES,
    VISUALIZATION_URLS,
    check_buckets_for_visualization_type,
)
from gooddata_sdk.catalog.validation.model import ValidationReport
from gooddata_sdk.catalog.validation.visualization import validate_content


def _content(url: str, *buckets: str, empty: tuple[str, ...] = ()) -> dict[str, Any]:
    return {
        "version": "2",
        "visualizationUrl": url,
        "buckets": [
            {
                "localIdentifier": name,
                "items": [
                    {
                        "measure": {
                            "localIdentifier": f"m_{name}",
                            "definition": {
                                "measureDefinition": {"item": {"identifier": {"id": "r", "type": "metric"}}}
                            },
                        }
                    }
                ],
            }
            for name in buckets
        ]
        + [{"localIdentifier": name, "items": []} for name in empty],
        "filters": [],
        "sorts": [],
    }


def _codes(findings: list[Any]) -> list[str]:
    return [f.code for f in findings]


class TestChartTypesWithARule:
    def test_a_column_chart_using_its_own_buckets_is_quiet(self):
        assert check_buckets_for_visualization_type(_content("local:column", "measures", "view", "stack")) == []

    def test_a_line_chart_using_a_column_charts_dimension_bucket_is_reported(self):
        """The classic hand-authoring mistake: a line chart's dimension bucket is `trend`,
        a column chart's is `view`, and the wrong one stores fine and renders nothing."""
        findings = check_buckets_for_visualization_type(_content("local:line", "measures", "view"), object_id="v1")
        assert _codes(findings) == ["unexpected_bucket_for_visualization_type"]
        assert findings[0].object_id == "v1"
        assert "local:line" in findings[0].message

    def test_it_is_a_warning_not_an_error(self):
        """A chart type can learn a new bucket long before this table hears about it."""
        findings = check_buckets_for_visualization_type(_content("local:line", "view"))
        assert findings[0].severity.value == "warning"

    def test_the_finding_points_at_the_offending_bucket(self):
        findings = check_buckets_for_visualization_type(_content("local:line", "measures", "trend", "view"))
        assert findings[0].location == "content.buckets[2].localIdentifier"

    def test_a_table_is_checked_under_both_spellings_that_occur(self):
        """Stored content carries both `local:table` and a bare `table`."""
        assert check_buckets_for_visualization_type(_content("table", "measures", "attribute")) == []
        assert _codes(check_buckets_for_visualization_type(_content("table", "trend"))) == [
            "unexpected_bucket_for_visualization_type"
        ]


class TestWhatItDeclinesToSay:
    def test_a_chart_type_with_no_rule_is_not_checked(self):
        """No entry means no opinion, which is not the same as "this is wrong"."""
        assert check_buckets_for_visualization_type(_content("local:sunburst", "anything", "at_all")) == []
        assert "local:sunburst" not in BUCKETS_BY_VISUALIZATION

    def test_a_treemap_has_no_rule_on_purpose(self):
        """The converter reads a treemap's attributes out of every bucket without naming
        one, so no bucket can be the wrong bucket."""
        assert "local:treemap" not in BUCKETS_BY_VISUALIZATION
        assert check_buckets_for_visualization_type(_content("local:treemap", "view", "segment")) == []

    def test_measure_buckets_are_accepted_on_every_type_that_has_a_rule(self):
        """The converter collects measures by walking all buckets rather than by name, so
        a measure bucket is never in the wrong place. Only attribute buckets are looked up
        per chart type, so only those can be wrong."""
        for url, allowed in BUCKETS_BY_VISUALIZATION.items():
            assert {"measures", "secondary_measures", "tertiary_measures"} <= allowed, url

    def test_a_missing_bucket_is_never_reported(self):
        """A chart with no dimension bucket is a legitimate work in progress."""
        assert check_buckets_for_visualization_type(_content("local:column", "measures")) == []

    def test_an_empty_bucket_of_the_wrong_name_is_ignored(self):
        """It carries nothing and breaks nothing -- reporting it would flag the placeholder
        buckets the UI leaves behind on a half-built chart."""
        assert check_buckets_for_visualization_type(_content("local:line", "measures", empty=("view",))) == []

    def test_content_that_is_not_an_object_is_left_to_the_structural_checks(self):
        assert check_buckets_for_visualization_type(None) == []
        assert check_buckets_for_visualization_type({"visualizationUrl": "local:line", "buckets": "nonsense"}) == []

    def test_a_caller_can_supply_its_own_rules(self):
        """The table is a default, not a fact: a caller covering a chart type this SDK does
        not know should be able to say so without waiting for a release."""
        rules = {"local:sunburst": frozenset({"measures", "view"})}
        assert check_buckets_for_visualization_type(_content("local:sunburst", "measures"), rules=rules) == []
        assert _codes(check_buckets_for_visualization_type(_content("local:sunburst", "trend"), rules=rules)) == [
            "unexpected_bucket_for_visualization_type"
        ]


class TestTheVocabularies:
    """Both lists come from the platform's execution converter: it looks buckets up by
    name and dispatches on chart type, so a name outside either list is read by nothing."""

    def test_every_chart_type_is_accepted_in_both_spellings(self):
        for name in VISUALIZATION_NAMES:
            assert name in VISUALIZATION_URLS
            assert f"local:{name}" in VISUALIZATION_URLS

    def test_the_bare_table_spelling_that_occurs_in_stored_content_is_known(self):
        assert {"table", "local:table"} <= VISUALIZATION_URLS

    def test_the_chart_types_the_platform_converts_are_all_present(self):
        assert {"sankey", "repeater", "waterfall", "mekko", "xirr", "radar", "choropleth"} <= VISUALIZATION_NAMES

    def test_every_bucket_any_rule_names_is_a_known_bucket_name(self):
        """The two tables cannot drift apart: a rule naming a bucket the converter has no
        name for would report every chart of that type."""
        for url, allowed in BUCKETS_BY_VISUALIZATION.items():
            assert allowed <= BUCKET_NAMES, url

    def test_every_type_with_a_rule_is_a_known_chart_type(self):
        assert set(BUCKETS_BY_VISUALIZATION) <= VISUALIZATION_URLS


class TestChartTypesGroundedInTheConverter:
    """Types the table gained from the execution converter rather than from observation."""

    def test_a_sankey_uses_its_from_and_to_buckets(self):
        assert check_buckets_for_visualization_type(_content("local:sankey", "attribute_from", "attribute_to")) == []

    def test_a_sankey_carrying_a_view_bucket_is_reported(self):
        assert _codes(check_buckets_for_visualization_type(_content("local:sankey", "view"))) == [
            "unexpected_bucket_for_visualization_type"
        ]

    def test_a_scatter_plot_uses_attribute_and_segment(self):
        assert check_buckets_for_visualization_type(_content("local:scatter", "attribute", "segment")) == []

    def test_a_heatmap_carrying_a_trend_bucket_is_reported(self):
        assert _codes(check_buckets_for_visualization_type(_content("local:heatmap", "trend"))) == [
            "unexpected_bucket_for_visualization_type"
        ]

    def test_a_geo_chart_keeps_the_buckets_built_from_its_properties(self):
        """latitude and longitude are buckets the platform builds out of
        properties.controls, so they are legitimate on a stored geo chart."""
        content = _content("local:pushpin", "location", "latitude", "longitude", "tooltipText")
        assert check_buckets_for_visualization_type(content) == []


class TestWiredIntoContentValidation:
    def test_validate_content_reports_it(self):
        codes = _codes(validate_content(_content("local:line", "measures", "view")))
        assert "unexpected_bucket_for_visualization_type" in codes

    def test_a_warning_alone_does_not_make_content_invalid(self):
        report = ValidationReport().extend(validate_content(_content("local:line", "measures", "view")))
        assert report.warnings
        assert report.ok is True
