# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Optional, Union

import gooddata_api_client.models as afm_models
from gooddata_api_client.model_utils import OpenApiModel
from gooddata_api_client.models import AbsoluteDateFilterAbsoluteDateFilter as AbsoluteDateFilterBody
from gooddata_api_client.models import (
    ComparisonMeasureValueFilterComparisonMeasureValueFilter as ComparisonMeasureValueFilterBody,
)
from gooddata_api_client.models import NegativeAttributeFilterNegativeAttributeFilter as NegativeAttributeFilterBody
from gooddata_api_client.models import PositiveAttributeFilterPositiveAttributeFilter as PositiveAttributeFilterBody
from gooddata_api_client.models import RangeMeasureValueFilterRangeMeasureValueFilter as RangeMeasureValueFilterBody
from gooddata_api_client.models import RankingFilterRankingFilter as RankingFilterBody
from gooddata_api_client.models import RelativeDateFilterRelativeDateFilter as RelativeDateFilterBody
from gooddata_sdk.compute.model.attribute import Attribute
from gooddata_sdk.compute.model.base import Filter, ObjId
from gooddata_sdk.compute.model.metric import Metric


def _extract_id_or_local_id(val: Union[ObjId, Attribute, Metric, str]) -> Union[ObjId, str]:
    if isinstance(val, (str, ObjId)):
        return val
    else:
        # if things bomb here it means bad input to model class
        return val.local_id


def _to_identifier(val: Union[ObjId, str]) -> Union[afm_models.AfmLocalIdentifier, afm_models.AfmIdentifier]:
    if isinstance(val, str):
        return afm_models.AfmLocalIdentifier(local_identifier=val)

    return val.as_identifier()


class AttributeFilter(Filter):
    def __init__(self, label: Union[ObjId, str, Attribute], values: Optional[list[str]] = None) -> None:
        super(AttributeFilter, self).__init__()

        self._label = _extract_id_or_local_id(label)
        self._values = values or []

    @property
    def label(self) -> Union[ObjId, str]:
        return self._label

    @label.setter
    def label(self, label: Union[ObjId, str]) -> None:
        self._label = label

    @property
    def values(self) -> list[str]:
        return self._values

    def is_noop(self) -> bool:
        return False

    def as_api_model(self) -> OpenApiModel:
        raise NotImplementedError()

    def __eq__(self, other: object) -> bool:
        return isinstance(other, AttributeFilter) and self._label == other._label and self._values == other._values


class PositiveAttributeFilter(AttributeFilter):
    def as_api_model(self) -> afm_models.PositiveAttributeFilter:
        label_id = _to_identifier(self._label)
        elements = afm_models.AttributeFilterElements(values=self.values)
        body = PositiveAttributeFilterBody(label=label_id, _in=elements, _check_type=False)
        return afm_models.PositiveAttributeFilter(body, _check_type=False)


class NegativeAttributeFilter(AttributeFilter):
    def is_noop(self) -> bool:
        return len(self.values) == 0

    def as_api_model(self) -> afm_models.NegativeAttributeFilter:
        label_id = _to_identifier(self._label)
        elements = afm_models.AttributeFilterElements(values=self.values)
        body = NegativeAttributeFilterBody(label=label_id, not_in=elements, _check_type=False)
        return afm_models.NegativeAttributeFilter(body)


_GRANULARITY: set[str] = {
    "YEAR",
    "QUARTER",
    "MONTH",
    "WEEK",
    "WEEK",
    "DAY",
    "HOUR",
    "MINUTE",
    "QUARTER_OF_YEAR",
    "MONTH_OF_YEAR",
    "WEEK_OF_YEAR",
    "DAY_OF_YEAR",
    "DAY_OF_MONTH",
    "DAY_OF_WEEK",
    "HOUR_OF_DAY",
    "MINUTE_OF_HOUR",
}


class RelativeDateFilter(Filter):
    def __init__(self, dataset: ObjId, granularity: str, from_shift: int, to_shift: int) -> None:
        super(RelativeDateFilter, self).__init__()

        if granularity not in _GRANULARITY:
            raise ValueError(
                f"Invalid relative date filter granularity '{granularity}'."
                f"It is expected to be one of: {_GRANULARITY}"
            )

        self._dataset = dataset
        self._granularity = granularity
        self._from_shift = from_shift
        self._to_shift = to_shift

    @property
    def dataset(self) -> ObjId:
        return self._dataset

    @property
    def granularity(self) -> str:
        return self._granularity

    @property
    def from_shift(self) -> int:
        return self._from_shift

    @property
    def to_shift(self) -> int:
        return self._to_shift

    def is_noop(self) -> bool:
        return False

    def as_api_model(self) -> afm_models.RelativeDateFilter:
        body = RelativeDateFilterBody(
            dataset=self.dataset.as_afm_id(),
            granularity=self.granularity,
            _from=self.from_shift,
            to=self.to_shift,
            _check_type=False,
        )
        return afm_models.RelativeDateFilter(body)


# noinspection PyAbstractClass
class AllTimeFilter(Filter):
    """Filter that is semantically equivalent to absent filter.

    This filter exists because 'All time filter' retrieved from GoodData.CN
    is non-standard as it does not have `from` and `to` fields;
    this is also the reason why as_api_model method is not implemented - it
    would lead to invalid object.

    The main feature of this filter is noop.
    """

    def is_noop(self) -> bool:
        return True


class AbsoluteDateFilter(Filter):
    def __init__(self, dataset: ObjId, from_date: str, to_date: str) -> None:
        super(AbsoluteDateFilter, self).__init__()

        self._dataset = dataset
        self._from_date = from_date
        self._to_date = to_date

    @property
    def dataset(self) -> ObjId:
        return self._dataset

    @property
    def from_date(self) -> str:
        return self._from_date

    @property
    def to_date(self) -> str:
        return self._to_date

    def is_noop(self) -> bool:
        return False

    def as_api_model(self) -> afm_models.AbsoluteDateFilter:
        body = AbsoluteDateFilterBody(
            dataset=self.dataset.as_afm_id(),
            _from=self._from_date,
            to=self._to_date,
            _check_type=False,
        )
        return afm_models.AbsoluteDateFilter(body)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, AbsoluteDateFilter)
            and self._dataset == other._dataset
            and self._from_date == other._from_date
            and self._to_date == other._to_date
        )


_METRIC_VALUE_FILTER_OPERATORS = {
    "EQUAL_TO": "comparison",
    "GREATER_THAN": "comparison",
    "GREATER_THAN_OR_EQUAL_TO": "comparison",
    "LESS_THAN": "comparison",
    "LESS_THAN_OR_EQUAL_TO": "comparison",
    "NOT_EQUAL_TO": "comparison",
    "BETWEEN": "range",
    "NOT_BETWEEN": "range",
}


class MetricValueFilter(Filter):
    def __init__(
        self,
        metric: Union[ObjId, str, Metric],
        operator: str,
        values: Union[float, int, tuple[float, float]],
        treat_nulls_as: Union[float, None] = None,
    ) -> None:
        super(MetricValueFilter, self).__init__()

        if operator not in _METRIC_VALUE_FILTER_OPERATORS:
            raise ValueError(
                f"Invalid metric value filter operator type '{operator}'."
                f"It is expected to be one of: {_METRIC_VALUE_FILTER_OPERATORS.keys()}"
            )

        if _METRIC_VALUE_FILTER_OPERATORS[operator] == "range":
            if not isinstance(values, tuple) or len(values) != 2:
                raise ValueError(f"Invalid number of values for {operator}. Expected two values: (from, to).")

            self._values: Union[tuple[float], tuple[float, float]] = values
        else:
            if not isinstance(values, (int, float)) and len(values) != 1:
                raise ValueError(
                    f"Invalid number of values for {operator}. "
                    f"Expected single int, float or one-sized list or tuple."
                )
            # Convert int to float as AFM model filters accept float values
            self._values = (float(values),) if isinstance(values, (int, float)) else values

        self._metric = _extract_id_or_local_id(metric)
        self._operator = operator
        self._treat_nulls_as = treat_nulls_as

    @property
    def metric(self) -> Union[ObjId, str]:
        return self._metric

    @metric.setter
    def metric(self, metric: Union[ObjId, str]) -> None:
        self._metric = metric

    @property
    def operator(self) -> str:
        return self._operator

    @property
    def values(self) -> Union[tuple[float], tuple[float, float]]:
        return self._values

    @property
    def treat_nulls_as(self) -> Union[float, None]:
        return self._treat_nulls_as

    def is_noop(self) -> bool:
        return False

    def as_api_model(self) -> Union[afm_models.ComparisonMeasureValueFilter, afm_models.RangeMeasureValueFilter]:
        measure = _to_identifier(self._metric)

        kwargs = dict(
            measure=measure,
            operator=self.operator,
            _check_type=False,
        )
        if self.treat_nulls_as is not None:
            kwargs["treat_null_values_as"] = self.treat_nulls_as

        if _METRIC_VALUE_FILTER_OPERATORS[self.operator] == "comparison":
            kwargs["value"] = self.values[0]

            body = ComparisonMeasureValueFilterBody(**kwargs)
            return afm_models.ComparisonMeasureValueFilter(body)
        else:
            kwargs["_from"] = min(self.values)
            kwargs["to"] = max(self.values)

            body = RangeMeasureValueFilterBody(**kwargs)
            return afm_models.RangeMeasureValueFilter(body)


_RANKING_OPERATORS = {"TOP", "BOTTOM"}


class RankingFilter(Filter):
    def __init__(
        self,
        metrics: list[Union[ObjId, Metric, str]],
        operator: str,
        value: int,
        dimensionality: Optional[list[Union[str, ObjId, Attribute, Metric]]],
    ) -> None:
        super(RankingFilter, self).__init__()

        if operator not in _RANKING_OPERATORS:
            raise ValueError(
                f"Invalid ranking filter operator type '{operator}'."
                f"It is expected to be one of: {_RANKING_OPERATORS}"
            )

        self._metrics = [_extract_id_or_local_id(m) for m in metrics]
        self._dimensionality = [_extract_id_or_local_id(d) for d in dimensionality] if dimensionality else None
        self._operator = operator
        self._value = value

    @property
    def metrics(self) -> list[Union[ObjId, str]]:
        return self._metrics

    @property
    def operator(self) -> str:
        return self._operator

    @property
    def value(self) -> int:
        return self._value

    @property
    def dimensionality(self) -> Optional[list[Union[ObjId, str]]]:
        return self._dimensionality

    def is_noop(self) -> bool:
        return False

    def as_api_model(self) -> afm_models.RankingFilter:
        measures = [_to_identifier(m) for m in self.metrics]
        dimensionality = {}
        if self.dimensionality:
            dimensionality["dimensionality"] = [_to_identifier(d) for d in self.dimensionality]
        body = RankingFilterBody(
            measures=measures, operator=self.operator, value=self.value, _check_type=False, **dimensionality
        )
        return afm_models.RankingFilter(body)
