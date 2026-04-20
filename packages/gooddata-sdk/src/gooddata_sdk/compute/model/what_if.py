# (C) 2025 GoodData Corporation
from __future__ import annotations

import gooddata_api_client.models as afm_models
from attrs import define, field


@define(kw_only=True)
class AfmWhatIfMeasureAdjustmentConfig:
    """SDK wrapper for a single measure adjustment within a what-if scenario.

    Represents an alternative MAQL definition for a catalog metric or fact that
    is used only during the current what-if computation without modifying the
    stored definition.
    """

    metric_id: str
    """ID of the metric or fact to adjust."""
    metric_type: str
    """Type of the object being adjusted. Typically 'metric' or 'fact'."""
    scenario_maql: str
    """Alternative MAQL expression to use for this scenario."""

    def as_api_model(self) -> afm_models.WhatIfMeasureAdjustmentConfig:
        return afm_models.WhatIfMeasureAdjustmentConfig(
            metric_id=self.metric_id,
            metric_type=self.metric_type,
            scenario_maql=self.scenario_maql,
            _check_type=False,
        )


@define(kw_only=True)
class AfmWhatIfScenarioItem:
    """SDK wrapper for a single what-if scenario.

    Represents one named scenario that overrides one or more measure definitions
    with alternative MAQL expressions.
    """

    label: str
    """Human-readable label for the scenario."""
    adjustments: list[AfmWhatIfMeasureAdjustmentConfig] = field(factory=list)
    """Measure adjustments for this scenario."""

    def as_api_model(self) -> afm_models.WhatIfScenarioItem:
        return afm_models.WhatIfScenarioItem(
            label=self.label,
            adjustments=[a.as_api_model() for a in self.adjustments],
            _check_type=False,
        )


@define(kw_only=True)
class AfmWhatIfScenarioConfig:
    """SDK wrapper for what-if scenario analysis configuration.

    Passed as part of :class:`AfmVisualizationConfig` to trigger what-if
    computation alongside a regular AFM execution.
    """

    include_baseline: bool
    """Whether the unmodified (baseline) values are included in the result."""
    scenarios: list[AfmWhatIfScenarioItem] = field(factory=list)
    """Scenarios, each providing alternative measure calculations."""

    def as_api_model(self) -> afm_models.WhatIfScenarioConfig:
        return afm_models.WhatIfScenarioConfig(
            include_baseline=self.include_baseline,
            scenarios=[s.as_api_model() for s in self.scenarios],
            _check_type=False,
        )
