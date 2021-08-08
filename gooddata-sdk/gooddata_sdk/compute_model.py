# (C) 2021 GoodData Corporation
from typing import Union
import gooddata_afm_client.models as afm_models


class ObjId:
    def __init__(self, id, type):
        self._id: str = id
        self._type: str = type

    @property
    def id(self) -> str:
        return self._id

    @property
    def type(self) -> str:
        return self._type

    def as_afm_id(self):
        return afm_models.AfmObjectIdentifier(
            identifier=afm_models.ObjectIdentifier(id=self._id, type=self._type)
        )

    def as_identifier(self):
        return afm_models.Identifier(
            identifier=afm_models.ObjectIdentifier(id=self._id, type=self._type),
            _check_type=False,
        )

    def __eq__(self, other):
        return (
            isinstance(other, ObjId) and self.id == other.id and self.type == other.type
        )

    def __str__(self):
        """
        String representation is used to transform ObjId to string key.

        :return: string in format <type>/<id>
        :rtype: str
        """
        return f"{self.type}/{self.id}"

    def __repr__(self):
        return f"{self.type}/{self.id}"


def _to_identifier(val: Union[ObjId, str]):
    if isinstance(val, str):
        return afm_models.LocalIdentifier(local_identifier=val)

    return val.as_identifier()


def _extract_id_or_local_id(val) -> Union[ObjId, str]:
    if isinstance(val, (str, ObjId)):
        return val
    else:
        # if things bomb here it means bad input to model class
        return val.local_id


def _extract_local_id(val) -> str:
    if isinstance(val, str):
        return val
    else:
        # if things bomb here it means bad input to model class
        return val.local_id


class ExecModelEntity:
    def __init__(self):
        pass

    def as_api_model(self):
        raise NotImplementedError()


class Attribute(ExecModelEntity):
    def __init__(self, local_id: str, label: Union[ObjId, str]):
        """
        Creates new attribute that can be used to slice or dice metric values during computation.

        :param local_id: identifier of the attribute within the execution
        :param label: identifier of the label to use for slicing or dicing; specified either as ObjId or str containing the label id
        """
        super(Attribute, self).__init__()

        self._local_id = local_id
        self._label = ObjId(label, "label") if isinstance(label, str) else label

    @property
    def local_id(self):
        return self._local_id

    @property
    def label(self):
        return self._label

    def has_same_label(self, other):
        return isinstance(other, Attribute) and other.label == self.label

    def as_api_model(self) -> afm_models.AttributeItem:
        return afm_models.AttributeItem(
            local_identifier=self.local_id, label=self.label.as_afm_id()
        )


class Filter(ExecModelEntity):
    def __init__(self):
        super(Filter, self).__init__()

        self._apply_on_result = None

    @property
    def apply_on_result(self) -> Union[bool, None]:
        return self._apply_on_result

    def is_noop(self):
        raise NotImplementedError()

    def as_api_model(self):
        raise NotImplementedError()


class Metric(ExecModelEntity):
    def __init__(self, local_id: str):
        super(Metric, self).__init__()
        self._local_id = local_id

    @property
    def local_id(self) -> str:
        return self._local_id

    def as_api_model(self) -> afm_models.MeasureItem:
        definition = self._body_as_api_model()

        return afm_models.MeasureItem(
            local_identifier=self._local_id, definition=definition
        )

    def _body_as_api_model(self):
        raise NotImplementedError()


SIMPLE_METRIC_AGGREGATION = {
    "SUM",
    "AVG",
    "COUNT",
    "APPROXIMATE_COUNT",
    "MAX",
    "MEDIAN",
    "MIN",
    "RUNSUM",
}


class SimpleMetric(Metric):
    def __init__(
        self,
        local_id: str,
        item: ObjId,
        aggregation=None,
        compute_ratio=False,
        filters: list[Filter] = None,
    ):
        super(SimpleMetric, self).__init__(local_id)

        _agg = aggregation.upper() if aggregation is not None else None
        if _agg is not None and _agg not in SIMPLE_METRIC_AGGREGATION:
            raise ValueError(
                f"Invalid simple metric aggregation '{_agg}'. "
                f"Valid operators: {SIMPLE_METRIC_AGGREGATION}"
            )

        self._item = item

        if item.type == "metric":
            self._aggregation = None
        elif _agg is None:
            self._aggregation = "SUM"
        else:
            self._aggregation = _agg

        self._compute_ratio = compute_ratio

        if filters is None:
            self._filters = []
        else:
            self._filters = filters

    @property
    def item(self) -> ObjId:
        return self._item

    @property
    def aggregation(self) -> str:
        return self._aggregation

    @property
    def compute_ratio(self) -> bool:
        return self._compute_ratio

    @property
    def filters(self) -> list[Filter]:
        return self._filters

    def _body_as_api_model(self):
        _filters = [f.as_api_model() for f in self.filters]

        # aggregation is optional yet the model bombs if None is sent :(
        if self.aggregation is not None:
            return afm_models.SimpleMeasureDefinition(
                afm_models.SimpleMeasureDefinitionMeasure(
                    item=self.item.as_afm_id(),
                    aggregation=self.aggregation,
                    compute_ratio=self.compute_ratio,
                    filters=_filters,
                    _check_type=False,
                )
            )
        else:
            return afm_models.SimpleMeasureDefinition(
                afm_models.SimpleMeasureDefinitionMeasure(
                    item=self.item.as_afm_id(),
                    compute_ratio=self.compute_ratio,
                    filters=_filters,
                    _check_type=False,
                )
            )


class PopDate:
    def __init__(self, attribute: Union[ObjId, Attribute], periods_ago: int):
        if isinstance(attribute, Attribute):
            self._attribute = attribute.label
        else:
            self._attribute = attribute
        self._periods_ago = periods_ago

    @property
    def attribute(self) -> ObjId:
        return self._attribute

    @property
    def periods_ago(self) -> int:
        return self._periods_ago

    def as_api_model(self):
        return afm_models.PopDate(
            attribute=self.attribute.as_afm_id(), periods_ago=self.periods_ago
        )


class PopDateMetric(Metric):
    def __init__(
        self,
        local_id: str,
        metric: Union[str, Metric],
        date_attributes: list[PopDate],
    ):
        super(PopDateMetric, self).__init__(local_id)

        self._metric = _extract_local_id(metric)
        self._date_attributes = date_attributes

    @property
    def metric_local_id(self) -> str:
        return self._metric

    @property
    def date_attributes(self) -> list[PopDate]:
        return self._date_attributes

    def _body_as_api_model(self):
        measure_identifier = afm_models.LocalIdentifier(
            local_identifier=self.metric_local_id
        )
        date_attributes = list([a.as_api_model() for a in self.date_attributes])

        return afm_models.PopDateMeasureDefinition(
            afm_models.PopDateMeasureDefinitionOverPeriodMeasure(
                measure_identifier=measure_identifier, date_attributes=date_attributes
            )
        )


class PopDateDataset:
    def __init__(self, dataset: Union[ObjId, str], periods_ago: int):
        self._dataset = (
            ObjId(dataset, "dataset") if isinstance(dataset, str) else dataset
        )
        self._periods_ago = periods_ago

    @property
    def dataset(self) -> ObjId:
        return self._dataset

    @property
    def periods_ago(self) -> int:
        return self._periods_ago

    def as_api_model(self):
        return afm_models.PopDataset(
            dataset=self.dataset.as_afm_id(), periods_ago=self.periods_ago
        )


class PopDatesetMetric(Metric):
    def __init__(
        self,
        local_id: str,
        metric: Union[str, Metric],
        date_datasets: list[PopDateDataset],
    ):
        super(PopDatesetMetric, self).__init__(local_id)

        self._metric = _extract_local_id(metric)
        self._date_datasets = date_datasets

    @property
    def metric_local_id(self) -> str:
        return self._metric

    @property
    def date_datasets(self) -> list[PopDateDataset]:
        return self._date_datasets

    def _body_as_api_model(self):
        measure_identifier = afm_models.LocalIdentifier(
            local_identifier=self.metric_local_id
        )
        date_datasets = list([d.as_api_model() for d in self.date_datasets])

        return afm_models.PopDatasetMeasureDefinition(
            afm_models.PopDatasetMeasureDefinitionPreviousPeriodMeasure(
                measure_identifier=measure_identifier, date_datasets=date_datasets
            )
        )


ARITHMETIC_METRIC_OPERATORS = {
    "SUM",
    "DIFFERENCE",
    "MULTIPLICATION",
    "RATIO",
    "CHANGE",
}


class ArithmeticMetric(Metric):
    def __init__(
        self, local_id: str, operator: str, operands: list[Union[str, Metric]]
    ):
        super(ArithmeticMetric, self).__init__(local_id)

        if operator not in ARITHMETIC_METRIC_OPERATORS:
            raise ValueError(
                f"Invalid arithmetic metric operator '{operator}'. "
                f"Valid operators: {ARITHMETIC_METRIC_OPERATORS}"
            )

        self._operator = operator
        self._operands = list([_extract_local_id(o) for o in operands])

    @property
    def operator(self) -> str:
        return self._operator

    @property
    def operand_local_ids(self) -> list[str]:
        return self._operands

    def _body_as_api_model(self):
        measure_identifiers = [
            afm_models.LocalIdentifier(local_identifier=local_d)
            for local_d in self._operands
        ]

        return afm_models.ArithmeticMeasureDefinition(
            afm_models.ArithmeticMeasureDefinitionArithmeticMeasure(
                operator=self.operator, measure_identifiers=measure_identifiers
            )
        )


class PositiveAttributeFilter(Filter):
    def __init__(
        self, label: Union[ObjId, str, Attribute], in_values: list[str] = None
    ):
        super(PositiveAttributeFilter, self).__init__()

        self._label = _extract_id_or_local_id(label)
        self._in_values = in_values or []

    @property
    def label(self) -> Union[ObjId, str]:
        return self._label

    @property
    def in_values(self) -> list[str]:
        return self._in_values

    def is_noop(self):
        return False

    def as_api_model(self):
        label_id = _to_identifier(self._label)
        elements = afm_models.AttributeFilterElements(values=self.in_values)
        body = afm_models.PositiveAttributeFilterBody(
            label=label_id, _in=elements, _check_type=False
        )
        return afm_models.PositiveAttributeFilter(body, _check_type=False)


class NegativeAttributeFilter(Filter):
    def __init__(self, label: Union[ObjId, str, Attribute], not_in_values: list[str]):
        super(NegativeAttributeFilter, self).__init__()

        self._label = _extract_id_or_local_id(label)
        self._not_in_values = not_in_values

    @property
    def label(self) -> Union[ObjId, str]:
        return self._label

    @property
    def not_in_values(self) -> list[str]:
        return self._not_in_values

    def is_noop(self):
        return len(self.not_in_values) == 0

    def as_api_model(self):
        label_id = _to_identifier(self._label)
        elements = afm_models.AttributeFilterElements(values=self.not_in_values)
        body = afm_models.NegativeAttributeFilterBody(
            label=label_id, not_in=elements, _check_type=False
        )
        return afm_models.NegativeAttributeFilter(body)


_GRANULARITY = {
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
    def __init__(
        self, dataset: ObjId, granularity: str, from_shift: int, to_shift: int
    ):
        super(RelativeDateFilter, self).__init__()

        if granularity not in _GRANULARITY:
            raise ValueError(
                f"Invalid relative date filter granularity '{granularity}'."
                f"It is expected to be one of: {_GRANULARITY.keys()}"
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

    def is_noop(self):
        return False

    def as_api_model(self):
        body = afm_models.RelativeDateFilterBody(
            dataset=self.dataset.as_afm_id(),
            granularity=self.granularity,
            _from=self.from_shift,
            to=self.to_shift,
            _check_type=False,
        )
        return afm_models.RelativeDateFilter(body)


class AbsoluteDateFilter(Filter):
    def __init__(self, dataset: ObjId, from_date: str, to_date: str):
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

    def is_noop(self):
        return False

    def as_api_model(self):
        body = afm_models.AbsoluteDateFilterBody(
            dataset=self.dataset.as_afm_id(),
            _from=self._from_date,
            to=self._to_date,
            _check_type=False,
        )
        return afm_models.AbsoluteDateFilter(body)


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
    ):
        super(MetricValueFilter, self).__init__()

        if operator not in _METRIC_VALUE_FILTER_OPERATORS:
            raise ValueError(
                f"Invalid metric value filter operator type '{operator}'."
                f"It is expected to be one of: {_METRIC_VALUE_FILTER_OPERATORS.keys()}"
            )

        if _METRIC_VALUE_FILTER_OPERATORS[operator] == "range":
            if len(values) != 2:
                raise ValueError(
                    f"Invalid number of values for {operator}. Expected two values: (from, to)."
                )

            self._values = values
        else:
            if not isinstance(values, (int, float)) and len(values) != 1:
                raise ValueError(
                    f"Invalid number of values for {operator}. "
                    f"Expected single int, float or one-sized list or tuple."
                )

            self._values = (values,) if isinstance(values, (int, float)) else values

        self._metric = _extract_id_or_local_id(metric)
        self._operator = operator
        self._treat_nulls_as = treat_nulls_as

    @property
    def metric(self) -> Union[ObjId, str]:
        return self._metric

    @property
    def operator(self) -> str:
        return self._operator

    @property
    def values(self) -> tuple[float]:
        return self._values

    @property
    def treat_nulls_as(self) -> Union[float, None]:
        return self._treat_nulls_as

    def is_noop(self):
        return False

    def as_api_model(self):
        measure = _to_identifier(self._metric)

        if _METRIC_VALUE_FILTER_OPERATORS[self.operator] == "comparison":
            body = afm_models.ComparisonMeasureValueFilterBody(
                measure=measure,
                operator=self.operator,
                value=self.values[0],
                treat_null_values_as=self.treat_nulls_as,
                _check_type=False,
            )

            return afm_models.ComparisonMeasureValueFilter(body)
        else:
            _from = min(self.values)
            to = max(self.values)

            body = afm_models.RangeMeasureValueFilterBody(
                measure=measure,
                operator=self.operator,
                _from=_from,
                to=to,
                treat_null_values_as=self.treat_nulls_as,
                _check_type=False,
            )

            return afm_models.RangeMeasureValueFilter(body)


_RANKING_OPERATORS = {"TOP", "BOTTOM"}


class RankingFilter(Filter):
    def __init__(
        self,
        metrics: list[Union[ObjId, Metric, str]],
        operator: str,
        value: int,
        dimensionality: list[Union[ObjId, Attribute, str]],
    ):
        super(RankingFilter, self).__init__()

        if operator not in _RANKING_OPERATORS:
            raise ValueError(
                f"Invalid ranking filter operator type '{operator}'."
                f"It is expected to be one of: {_RANKING_OPERATORS}"
            )

        self._metrics = [_extract_id_or_local_id(m) for m in metrics]
        self._dimensionality = [_extract_id_or_local_id(d) for d in dimensionality]
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
    def dimensionality(self) -> list[Union[ObjId, str]]:
        return self._dimensionality

    def is_noop(self):
        return False

    def as_api_model(self):
        measures = [_to_identifier(m) for m in self.metrics]
        dimensionality = [_to_identifier(d) for d in self.dimensionality]

        body = afm_models.RankingFilterBody(
            measures=measures,
            dimensionality=dimensionality,
            operator=self.operator,
            value=self.value,
            _check_type=False,
        )
        return afm_models.RankingFilter(body)


def compute_model_to_api_model(
    attributes: list[Attribute] = None,
    metrics: list[Metric] = None,
    filters: list[Filter] = None,
) -> afm_models.AFM:
    """
    Transforms categorized execution model entities (attributes, metrics, facts) into an API model
    that can be used for computations of data results or computations of object availability.

    :param attributes: optionally specify list of attributes
    :param metrics: optionally specify list of metrics
    :param filters: optionally specify list of filters
    :return:
    """
    return afm_models.AFM(
        attributes=[a.as_api_model() for a in attributes]
        if attributes is not None
        else [],
        measures=[m.as_api_model() for m in metrics] if metrics is not None else [],
        filters=[f.as_api_model() for f in filters] if filters is not None else [],
    )
