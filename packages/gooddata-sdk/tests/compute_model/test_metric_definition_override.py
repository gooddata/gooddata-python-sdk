# (C) 2025 GoodData Corporation
from __future__ import annotations

import pytest
from gooddata_sdk.compute.model.base import ObjId
from gooddata_sdk.compute.model.execution import MetricDefinitionOverride, compute_model_to_api_model
from gooddata_sdk.compute.model.metric import SimpleMetric
from gooddata_sdk.compute.model.what_if import (
    AfmWhatIfMeasureAdjustmentConfig,
    AfmWhatIfScenarioConfig,
    AfmWhatIfScenarioItem,
)


class TestMetricDefinitionOverride:
    def test_as_api_model_produces_correct_structure(self):
        override = MetricDefinitionOverride(
            item_id="my.metric",
            item_type="metric",
            maql="SELECT SUM({fact/revenue}) WHERE {attribute/region} = 'West'",
        )
        api_model = override.as_api_model()
        result = api_model.to_dict()

        assert result["item"]["identifier"]["id"] == "my.metric"
        assert result["item"]["identifier"]["type"] == "metric"
        assert result["definition"]["inline"]["maql"] == (
            "SELECT SUM({fact/revenue}) WHERE {attribute/region} = 'West'"
        )

    def test_as_api_model_with_fact_type(self):
        override = MetricDefinitionOverride(
            item_id="revenue.fact",
            item_type="fact",
            maql="SELECT AVG({fact/revenue})",
        )
        api_model = override.as_api_model()
        result = api_model.to_dict()

        assert result["item"]["identifier"]["type"] == "fact"


class TestComputeModelToApiModelWithOverrides:
    def test_measure_definition_overrides_forwarded(self):
        metric = SimpleMetric(local_id="m1", item=ObjId(type="metric", id="catalog.metric"))
        override = MetricDefinitionOverride(
            item_id="catalog.metric",
            item_type="metric",
            maql="SELECT SUM({fact/cost})",
        )

        afm = compute_model_to_api_model(
            metrics=[metric],
            measure_definition_overrides=[override],
        )
        result = afm.to_dict()

        assert "measureDefinitionOverrides" in result
        overrides = result["measureDefinitionOverrides"]
        assert len(overrides) == 1
        assert overrides[0]["item"]["identifier"]["id"] == "catalog.metric"
        assert overrides[0]["definition"]["inline"]["maql"] == "SELECT SUM({fact/cost})"

    def test_no_overrides_omits_field(self):
        metric = SimpleMetric(local_id="m1", item=ObjId(type="metric", id="catalog.metric"))
        afm = compute_model_to_api_model(metrics=[metric])
        result = afm.to_dict()

        assert result.get("measureDefinitionOverrides") is None or result.get("measureDefinitionOverrides") == []


class TestAfmWhatIfMeasureAdjustmentConfig:
    def test_as_api_model_produces_correct_structure(self):
        adjustment = AfmWhatIfMeasureAdjustmentConfig(
            metric_id="revenue",
            metric_type="metric",
            scenario_maql="SELECT SUM({fact/revenue}) * 1.1",
        )
        api_model = adjustment.as_api_model()
        result = api_model.to_dict()

        assert result["metricId"] == "revenue"
        assert result["metricType"] == "metric"
        assert result["scenarioMaql"] == "SELECT SUM({fact/revenue}) * 1.1"


class TestAfmWhatIfScenarioItem:
    def test_as_api_model_with_adjustments(self):
        adjustment = AfmWhatIfMeasureAdjustmentConfig(
            metric_id="revenue",
            metric_type="metric",
            scenario_maql="SELECT SUM({fact/revenue}) * 1.1",
        )
        scenario = AfmWhatIfScenarioItem(
            label="Optimistic +10%",
            adjustments=[adjustment],
        )
        api_model = scenario.as_api_model()
        result = api_model.to_dict()

        assert result["label"] == "Optimistic +10%"
        assert len(result["adjustments"]) == 1
        assert result["adjustments"][0]["metricId"] == "revenue"

    def test_as_api_model_empty_adjustments(self):
        scenario = AfmWhatIfScenarioItem(label="Empty scenario")
        result = scenario.as_api_model().to_dict()

        assert result["label"] == "Empty scenario"
        assert result["adjustments"] == []


class TestAfmWhatIfScenarioConfig:
    def test_as_api_model_with_scenarios(self):
        adjustment = AfmWhatIfMeasureAdjustmentConfig(
            metric_id="revenue",
            metric_type="metric",
            scenario_maql="SELECT SUM({fact/revenue}) * 0.9",
        )
        scenario = AfmWhatIfScenarioItem(label="Pessimistic -10%", adjustments=[adjustment])
        config = AfmWhatIfScenarioConfig(include_baseline=True, scenarios=[scenario])

        result = config.as_api_model().to_dict()

        assert result["includeBaseline"] is True
        assert len(result["scenarios"]) == 1
        assert result["scenarios"][0]["label"] == "Pessimistic -10%"

    def test_as_api_model_no_baseline(self):
        config = AfmWhatIfScenarioConfig(include_baseline=False)
        result = config.as_api_model().to_dict()

        assert result["includeBaseline"] is False
        assert result["scenarios"] == []

    @pytest.mark.parametrize(
        "include_baseline, scenario_count",
        [
            (True, 0),
            (False, 1),
            (True, 2),
        ],
    )
    def test_as_api_model_parametrized(self, include_baseline: bool, scenario_count: int):
        scenarios = [AfmWhatIfScenarioItem(label=f"scenario_{i}") for i in range(scenario_count)]
        config = AfmWhatIfScenarioConfig(include_baseline=include_baseline, scenarios=scenarios)
        result = config.as_api_model().to_dict()

        assert result["includeBaseline"] == include_baseline
        assert len(result["scenarios"]) == scenario_count
