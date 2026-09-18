# (C) 2026 GoodData Corporation
"""``validate()`` on the declarative objects themselves."""

from __future__ import annotations

from typing import Any

from gooddata_sdk import CatalogDeclarativeAnalytics, CatalogDeclarativeVisualizationObject


def _content(**overrides: Any) -> dict[str, Any]:
    content: dict[str, Any] = {
        "version": "2",
        "visualizationUrl": "local:column",
        "buckets": [{"localIdentifier": "measures", "items": [{"measure": {"localIdentifier": "m1"}}]}],
        "filters": [],
        "sorts": [],
        "properties": {},
    }
    content.update(overrides)
    return content


def _viz(object_id: str, **overrides: Any) -> CatalogDeclarativeVisualizationObject:
    return CatalogDeclarativeVisualizationObject(id=object_id, title=object_id, content=_content(**overrides))


_BROKEN_SORT = [{"measureSortItem": {"locators": [{"measureLocatorItem": {"measureIdentifier": "absent"}}]}}]


class TestVisualizationValidate:
    def test_a_valid_object_reports_nothing(self):
        assert _viz("v1").validate().ok

    def test_findings_carry_the_object_id(self):
        report = _viz("v1", sorts=_BROKEN_SORT).validate()
        assert not report.ok
        assert report.errors[0].object_id == "v1"

    def test_the_length_check_runs_on_the_serialised_content(self):
        """Length is a property of what gets sent, so it is measured on the JSON, not on
        the object -- a caller cannot see it any other way."""
        report = _viz("big", properties={"blob": "x" * 260_000}).validate()
        assert [f.code for f in report.errors] == ["content_too_long"]

    def test_unknown_chart_types_stay_warnings_so_the_report_still_passes(self):
        report = _viz("v1", visualizationUrl="local:sunburst").validate(
            known_visualization_urls=frozenset({"local:column"})
        )
        assert report.warnings
        assert report.ok is True


class TestAnalyticsModelValidate:
    def test_findings_from_every_visualization_are_collected(self):
        model = CatalogDeclarativeAnalytics.from_dict(
            {
                "analytics": {
                    "visualizationObjects": [
                        {"id": "good", "title": "good", "content": _content()},
                        {"id": "bad1", "title": "bad1", "content": _content(sorts=_BROKEN_SORT)},
                        {"id": "bad2", "title": "bad2", "content": _content(sorts=_BROKEN_SORT)},
                    ]
                }
            },
            camel_case=True,
        )
        report = model.validate()
        assert not report.ok
        assert sorted(f.object_id for f in report.errors) == ["bad1", "bad2"]

    def test_an_empty_model_validates_clean(self):
        assert CatalogDeclarativeAnalytics(analytics=None).validate().ok

    def test_a_model_with_no_visualizations_validates_clean(self):
        model = CatalogDeclarativeAnalytics.from_dict({"analytics": {"metrics": []}}, camel_case=True)
        assert model.validate().ok
