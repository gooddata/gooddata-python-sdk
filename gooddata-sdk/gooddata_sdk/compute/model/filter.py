# (C) 2022 GoodData Corporation
from __future__ import annotations

from datetime import datetime
from importlib.util import find_spec
from typing import Any, Optional, Union

from gooddata_api_client.model.inline_filter_definition_inline import InlineFilterDefinitionInline

if find_spec("icu") is not None:
    from icu import Locale, SimpleDateFormat  # type: ignore[import-not-found]

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

_DATE_FORMAT_INPUT = "%Y-%m-%d"
_DATE_FORMAT_OUTPUT = "%-m/%-d/%Y"

# input ICU format of date filters from datepicker
_ICU_DATE_FORMAT_INPUT = "y-M-d HH:mm"

# predefined default localized ICU date formats for date filters
#   taken from UI SDK:
#   https://github.com/gooddata/gooddata-ui-sdk/blob/master/libs/sdk-ui-filters/src/DateFilter/utils/FormattingUtils.ts
_ICU_LOCALIZED_DATE_FORMAT_PATTERNS = {
    "en-US": "M/d/y",
    "en-GB": "dd/MM/y",
    "cs-CZ": "d. M. y",
    "de-DE": "d.M.y",
    "es-ES": "d/M/y",
    "fr-FR": "dd/MM/y",
    "ja-JP": "y/M/d",
    "nl-NL": "d-M-y",
    "pt-BR": "dd/MM/y",
    "pt-PT": "dd/MM/y",
    "zh-Hans": "y/M/d",
    "ru-RU": "dd.MM.y",
    "it-IT": "dd/MM/y",
}

_METRIC_VALUE_FILTER_OPERATOR_LABEL = {
    "EQUAL_TO": "=",
    "GREATER_THAN": ">",
    "GREATER_THAN_OR_EQUAL_TO": ">=",
    "LESS_THAN": "<",
    "LESS_THAN_OR_EQUAL_TO": "<=",
    "NOT_EQUAL_TO": "!=",
}


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
        super().__init__()

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

    def description(self, labels: dict[str, str], format_locale: Optional[str] = None) -> str:
        label_id = self.label.id if isinstance(self.label, ObjId) else self.label
        values = ", ".join(self.values) if len(self.values) else "All"
        return f"{labels.get(label_id, label_id)}: {values}"


class NegativeAttributeFilter(AttributeFilter):
    def is_noop(self) -> bool:
        return len(self.values) == 0

    def as_api_model(self) -> afm_models.NegativeAttributeFilter:
        label_id = _to_identifier(self._label)
        elements = afm_models.AttributeFilterElements(values=self.values)
        body = NegativeAttributeFilterBody(label=label_id, not_in=elements, _check_type=False)
        return afm_models.NegativeAttributeFilter(body)

    def description(self, labels: dict[str, str], format_locale: Optional[str] = None) -> str:
        label_id = self.label.id if isinstance(self.label, ObjId) else self.label
        values = "All except " + ", ".join(self.values) if len(self.values) else "All"
        return f"{labels.get(label_id, label_id)}: {values}"


_GRANULARITY: set[str] = {
    "YEAR",
    "QUARTER",
    "MONTH",
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
        super().__init__()

        if granularity not in _GRANULARITY:
            raise ValueError(
                f"Invalid relative date filter granularity '{granularity}'. It is expected to be one of: {_GRANULARITY}"
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

    def description(self, labels: dict[str, str], format_locale: Optional[str] = None) -> str:
        # TODO compare with other period is not implemented as it's not defined in the filter but in measures
        from_shift = self.from_shift
        to_shift = self.to_shift
        gr = self.granularity
        range_str = "All time"
        if from_shift == -1 and to_shift == -1:
            range_str = "Yesterday" if gr == "DAY" else "Last " + gr.lower()
        elif from_shift == 0 and to_shift == 0:
            range_str = "Today" if gr == "DAY" else "This " + gr.lower()
        elif from_shift == 1 and to_shift == 1:
            range_str = "Tomorrow" if gr == "DAY" else "Next " + gr.lower()
        else:
            if to_shift == 0:
                range_str = f"Last {abs(from_shift) + 1} " + gr.lower() + "s"
            elif from_shift == 0:
                range_str = f"Next {to_shift + 1} " + gr.lower() + "s"
            else:
                abs_from_shift = abs(from_shift)
                abs_to_shift = abs(to_shift)
                plural_from_shift = "s" if abs_from_shift > 1 else ""
                plural_to_shift = "s" if abs_to_shift > 1 else ""
                if from_shift < 0 < to_shift:
                    range_str = (
                        f"From {abs_from_shift} {gr.lower()}{plural_from_shift} ago "
                        f"to {to_shift} {gr.lower()}{plural_to_shift} ahead"
                    )
                elif from_shift < 0 and to_shift < 0:
                    range_str = (
                        f"From {abs_from_shift} {gr.lower()}{plural_from_shift} "
                        f"to {abs_to_shift} {gr.lower()}{plural_to_shift} ago"
                    )
                elif from_shift > 0 and to_shift > 0:
                    range_str = (
                        f"From {from_shift} {gr.lower()}{plural_from_shift} "
                        f"to {to_shift} {gr.lower()}{plural_to_shift} ahead"
                    )
        return f"{labels.get(self.dataset.id, self.dataset.id)}: {range_str}"


# noinspection PyAbstractClass
class AllTimeFilter(Filter):
    """Filter that is semantically equivalent to absent filter.

    This filter exists because 'All time filter' retrieved from GoodData.CN
    is non-standard as it does not have `from` and `to` fields;
    this is also the reason why as_api_model method is not implemented - it
    would lead to invalid object.

    The main feature of this filter is noop.
    """

    def __init__(self, dataset: ObjId) -> None:
        super().__init__()
        self._dataset = dataset

    @property
    def dataset(self) -> ObjId:
        return self._dataset

    def is_noop(self) -> bool:
        return True

    def description(self, labels: dict[str, str], format_locale: Optional[str] = None) -> str:
        return f"{labels.get(self.dataset.id, self.dataset.id)}: All time"


class AbsoluteDateFilter(Filter):
    def __init__(self, dataset: ObjId, from_date: str, to_date: str) -> None:
        super().__init__()

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

    def description(self, labels: dict[str, str], format_locale: Optional[str] = None) -> str:
        if format_locale is not None and find_spec("icu") is not None:
            src_parser = SimpleDateFormat(_ICU_DATE_FORMAT_INPUT)
            dest_formatter = SimpleDateFormat(
                _ICU_LOCALIZED_DATE_FORMAT_PATTERNS.get(format_locale, _ICU_LOCALIZED_DATE_FORMAT_PATTERNS["en-US"]),
                Locale.createCanonical(format_locale),
            )
            from_date = dest_formatter.format(src_parser.parse(self.from_date))
            to_date = dest_formatter.format(src_parser.parse(self.to_date))
            return f"{labels.get(self.dataset.id, self.dataset.id)}: {from_date} - {to_date}"
        else:
            from_date = datetime.strptime(self.from_date.split(" ")[0], _DATE_FORMAT_INPUT).strftime(
                _DATE_FORMAT_OUTPUT
            )
            to_date = datetime.strptime(self.to_date.split(" ")[0], _DATE_FORMAT_INPUT).strftime(_DATE_FORMAT_OUTPUT)
            return f"{labels.get(self.dataset.id, self.dataset.id)}: {from_date} - {to_date}"


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


class AllMetricValueFilter(Filter):
    def __init__(self, metric: Union[ObjId, str, Metric]) -> None:
        super().__init__()
        self._metric = _extract_id_or_local_id(metric)

    @property
    def metric(self) -> Union[ObjId, str]:
        return self._metric

    def is_noop(self) -> bool:
        return True

    def description(self, labels: dict[str, str], format_locale: Optional[str] = None) -> str:
        metric_id = self.metric.id if isinstance(self.metric, ObjId) else self.metric
        return f"{labels.get(metric_id, metric_id)}: All"


class MetricValueFilter(Filter):
    def __init__(
        self,
        metric: Union[ObjId, str, Metric],
        operator: str,
        values: Union[float, int, tuple[float, float]],
        treat_nulls_as: Union[float, None] = None,
    ) -> None:
        super().__init__()

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
                    f"Invalid number of values for {operator}. Expected single int, float or one-sized list or tuple."
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

    def description(self, labels: dict[str, str], format_locale: Optional[str] = None) -> str:
        metric_id = self.metric.id if isinstance(self.metric, ObjId) else self.metric
        if self.operator in ["BETWEEN", "NOT_BETWEEN"] and len(self.values) == 2:
            not_between = "not" if self.operator == "NOT_BETWEEN" else ""
            return f"{labels.get(metric_id, metric_id)}: {not_between}between {self.values[0]} - {self.values[1]}"
        else:
            return (
                f"{labels.get(metric_id, metric_id)}: "
                f"{_METRIC_VALUE_FILTER_OPERATOR_LABEL.get(self.operator, self.operator)} {self.values[0]}"
            )


_RANKING_OPERATORS = {"TOP", "BOTTOM"}


class RankingFilter(Filter):
    def __init__(
        self,
        metrics: list[Union[ObjId, Metric, str]],
        operator: str,
        value: int,
        dimensionality: Optional[list[Union[str, ObjId, Attribute, Metric]]],
    ) -> None:
        super().__init__()

        if operator not in _RANKING_OPERATORS:
            raise ValueError(
                f"Invalid ranking filter operator type '{operator}'. It is expected to be one of: {_RANKING_OPERATORS}"
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

    def description(self, labels: dict[str, str], format_locale: Optional[str] = None) -> str:
        # TODO more metrics and dimensions not supported now as it's not supported on FE as well
        dimensionality_ids = (
            [d.id if isinstance(d, ObjId) else d for d in self.dimensionality] if self.dimensionality else []
        )
        dimensionality_str = (
            f" out of {labels.get(dimensionality_ids[0], dimensionality_ids[0])} based on" if dimensionality_ids else ""
        )
        metric_ids = [m.id if isinstance(m, ObjId) else m for m in self.metrics]
        return (
            f"{self.operator.capitalize()} {self.value}{dimensionality_str} {labels.get(metric_ids[0], metric_ids[0])}"
        )


class InlineFilter(Filter):
    """Filter using a custom MAQL expression.

        Automatically decides, whether to create or update.

        Args:
            maql (str): The MAQL expression string that defines the filter condition.

    Example:
        ```python
        from gooddata_sdk import InlineFilter
        from gooddata_pandas import GoodPandas

        gp = GoodPandas.create_from_profile()
        factory = gp.data_frames("demo")

        filter_by = InlineFilter('{label/region} = "West"')

        factory.not_indexed(columns=dict(order_amount="metric/order_amount"), filter_by=filter_by)
        ```
    """

    def __init__(
        self, maql: str, apply_on_result: Optional[bool] = None, local_identifier: Optional[Union[ObjId, str]] = None
    ) -> None:
        super().__init__(apply_on_result)

        self.maql = maql
        self.local_identifier = local_identifier

    def is_noop(self) -> bool:
        return False

    def as_api_model(self) -> afm_models.InlineFilterDefinition:
        kwargs: dict[str, Any] = {}
        if self.apply_on_result is not None:
            kwargs["apply_on_result"] = self.apply_on_result
        if self.local_identifier is not None:
            kwargs["local_identifier"] = str(self.local_identifier)
        body = InlineFilterDefinitionInline(self.maql, **kwargs)
        return afm_models.InlineFilterDefinition(body, _check_type=False)
