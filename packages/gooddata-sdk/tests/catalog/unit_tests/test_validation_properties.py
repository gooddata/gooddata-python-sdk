# (C) 2026 GoodData Corporation
"""Checks on ``content.properties``.

The test that matters most here is the one asserting nothing is reported: ``properties``
is full of keys the platform models nowhere, and a check that flagged them would fire on
ordinary working charts. Everything else verifies that the few fields the platform does
read are actually looked at.
"""

from __future__ import annotations

from typing import Any

from gooddata_sdk.catalog.validation.properties import check_properties, extract_properties_references
from gooddata_sdk.catalog.validation.visualization import validate_content


def _content(url: str = "local:column", controls: dict[str, Any] | None = None, **extra: Any) -> dict[str, Any]:
    content: dict[str, Any] = {
        "version": "2",
        "visualizationUrl": url,
        "buckets": [
            {
                "localIdentifier": "measures",
                "items": [{"measure": {"localIdentifier": "m1", "definition": {"measure": {"item": {}}}}}],
            }
        ],
    }
    if controls is not None:
        content["properties"] = {"controls": controls}
    content.update(extra)
    return content


def _geo(controls: dict[str, Any], *, url: str = "local:pushpin", location: bool = True) -> dict[str, Any]:
    buckets = []
    if location:
        buckets.append(
            {
                "localIdentifier": "location",
                "items": [{"attribute": {"localIdentifier": "loc", "displayForm": {"identifier": {}}}}],
            }
        )
    return {"version": "2", "visualizationUrl": url, "buckets": buckets, "properties": {"controls": controls}}


def _codes(findings: list[Any]) -> list[str]:
    return [finding.code for finding in findings]


def _check(content: dict[str, Any], defined: set[str] | None = None) -> list[Any]:
    return check_properties(content, defined_local_ids=defined if defined is not None else {"m1"})


class TestUnmodelledKeysAreLeftAlone:
    """The platform ignores controls it does not recognise, and so must this. Stored
    content is full of them -- legend, xaxis, colorMapping, dualAxis, grid -- and every one
    belongs to the renderer, not to anything validation can speak about."""

    def test_the_renderers_own_controls_are_not_reported(self):
        controls = {
            "legend": {"position": "top", "enabled": True},
            "xaxis": {"visible": False},
            "yaxis": {"labelsEnabled": True},
            "dataLabels": {"visible": "auto"},
            "colorMapping": [{"id": "m1", "color": {"type": "guid", "value": "1"}}],
            "dualAxis": True,
            "grid": {"enabled": False},
            "primaryChartType": "column",
            "continuousLine": {"enabled": False},
        }
        assert _check(_content(controls=controls)) == []

    def test_a_chart_with_no_properties_at_all_is_fine(self):
        assert _check(_content()) == []

    def test_properties_that_are_not_an_object_are_reported_once(self):
        assert _codes(_check(_content(properties=["controls"]))) == ["properties_not_an_object"]

    def test_controls_that_are_not_an_object_are_reported_once(self):
        content = _content()
        content["properties"] = {"controls": "none"}
        assert _codes(_check(content)) == ["controls_not_an_object"]


class TestEnumeratedControls:
    def test_an_unrecognised_measure_group_dimension_warns(self):
        findings = _check(_content(controls={"measureGroupDimension": "diagonal"}))
        assert _codes(findings) == ["unknown_control_value"]
        assert findings[0].location == "content.properties.controls.measureGroupDimension"

    def test_both_real_measure_group_dimensions_pass(self):
        for value in ("rows", "columns"):
            assert _check(_content(controls={"measureGroupDimension": value})) == []

    def test_an_unrecognised_grand_totals_position_warns(self):
        assert _codes(_check(_content(controls={"grandTotalsPosition": "middle"}))) == ["unknown_control_value"]

    def test_every_real_grand_totals_position_passes(self):
        for value in ("pinnedBottom", "pinnedTop", "bottom", "top"):
            assert _check(_content(controls={"grandTotalsPosition": value})) == []

    def test_an_unrecognised_calculation_type_warns(self):
        controls = {"comparison": {"enabled": True, "calculationType": "delta"}}
        assert _codes(_check(_content("local:headline", controls))) == ["unknown_control_value"]

    def test_every_real_calculation_type_passes(self):
        for value in ("change", "ratio", "difference", "change_difference"):
            assert _check(_content("local:headline", {"comparison": {"calculationType": value}})) == []

    def test_a_comparison_without_a_calculation_type_is_fine(self):
        """The platform derives one from the secondary measure when it is absent."""
        assert _check(_content("local:headline", {"comparison": {"enabled": True}})) == []


class TestLocalIdentifierReferences:
    """Two controls name a measure by its bucket local identifier. Neither is reachable by
    the sort and filter walk, so a stale one has been invisible until now."""

    def test_a_secondary_axis_measure_that_no_bucket_defines_warns(self):
        findings = _check(_content(controls={"secondary_xaxis": {"measures": ["ghost"]}}))
        assert _codes(findings) == ["dangling_local_id_in_properties"]
        assert findings[0].location == "content.properties.controls.secondary_xaxis.measures[0]"

    def test_a_secondary_axis_measure_that_exists_passes(self):
        assert _check(_content(controls={"secondary_xaxis": {"measures": ["m1"]}})) == []

    def test_an_inline_visualization_for_no_measure_warns(self):
        findings = _check(_content("local:repeater", {"inlineVisualizations": {"ghost": {"type": "metric"}}}))
        assert _codes(findings) == ["dangling_local_id_in_properties"]

    def test_an_inline_visualization_of_an_unknown_type_warns(self):
        findings = _check(_content("local:repeater", {"inlineVisualizations": {"m1": {"type": "pie"}}}))
        assert _codes(findings) == ["unknown_control_value"]

    def test_every_real_inline_visualization_type_passes(self):
        for value in ("metric", "line", "column"):
            assert _check(_content("local:repeater", {"inlineVisualizations": {"m1": {"type": value}}})) == []


class TestGeoPositionReferences:
    """latitude, longitude and tooltipText hold label identifiers in a plain string. The
    reference walk looks for `identifier` nodes and goes straight past them."""

    def test_the_three_position_controls_become_label_references(self):
        references = extract_properties_references(_geo({"latitude": "lat", "longitude": "lon", "tooltipText": "name"}))
        assert [reference.obj_id for reference in references] == ["label/lat", "label/lon", "label/name"]

    def test_the_location_is_reported_where_it_was_found(self):
        references = extract_properties_references(_geo({"latitude": "lat"}))
        assert references[0].location == "content.properties.controls.latitude"

    def test_a_path_prefix_is_respected(self):
        references = extract_properties_references(_geo({"latitude": "lat"}), path="viz")
        assert references[0].location == "viz.properties.controls.latitude"

    def test_nothing_is_extracted_without_a_location_attribute(self):
        """The platform builds the derived buckets out of the location attribute; with no
        location attribute it builds nothing and never reads these values."""
        assert extract_properties_references(_geo({"latitude": "lat"}, location=False)) == []

    def test_nothing_is_extracted_on_a_chart_type_that_is_not_geo(self):
        assert extract_properties_references(_geo({"latitude": "lat"}, url="local:column")) == []

    def test_an_empty_position_control_is_not_a_reference(self):
        assert extract_properties_references(_geo({"latitude": ""})) == []

    def test_every_geo_chart_type_is_covered(self):
        for url in ("local:geo", "local:pushpin", "local:choropleth"):
            assert extract_properties_references(_geo({"latitude": "lat"}, url=url)) != []


class TestWiredIntoValidateContent:
    """The check has to be called, not merely imported -- a previous check in this package
    landed with its import in place and its call missing, and looked like success."""

    def test_validate_content_reports_a_properties_finding(self):
        findings = validate_content(_content(controls={"measureGroupDimension": "diagonal"}), object_id="viz")
        assert "unknown_control_value" in _codes(findings)
        assert findings[0].object_id == "viz"

    def test_a_healthy_chart_with_rich_properties_stays_clean(self):
        assert validate_content(_content(controls={"legend": {"position": "top"}, "dualAxis": True})) == []
