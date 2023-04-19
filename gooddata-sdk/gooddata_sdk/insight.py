# (C) 2021 GoodData Corporation
from __future__ import annotations

import functools
from typing import Any, Optional, Union, cast

from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.compute.model.attribute import Attribute
from gooddata_sdk.compute.model.base import ObjId
from gooddata_sdk.compute.model.filter import (
    AbsoluteDateFilter,
    AllTimeFilter,
    Filter,
    MetricValueFilter,
    NegativeAttributeFilter,
    PositiveAttributeFilter,
    RankingFilter,
    RelativeDateFilter,
)
from gooddata_sdk.compute.model.metric import (
    ArithmeticMetric,
    Metric,
    PopDate,
    PopDateDataset,
    PopDateMetric,
    PopDatesetMetric,
    SimpleMetric,
)
from gooddata_sdk.utils import IdObjType, SideLoads, load_all_entities, safeget

#
# Conversion from types stored in insight into the goodata_afm_client models. Insight is created by GD.UI SDK
# and is persisted in the freeform 'vis object' in the metadata. The types from SDK model are stored there.
#

_GRANULARITY_CONVERSION = {
    "GDC.time.year": "YEAR",
    "GDC.time.quarter": "QUARTER",
    "GDC.time.month": "MONTH",
    "GDC.time.week_us": "WEEK",
    "GDC.time.week": "WEEK",
    "GDC.time.date": "DAY",
    "GDC.time.hour": "HOUR",
    "GDC.time.minute": "MINUTE",
    "GDC.time.quarter_in_year": "QUARTER_OF_YEAR",
    "GDC.time.month_in_year": "MONTH_OF_YEAR",
    "GDC.time.week_in_year": "WEEK_OF_YEAR",
    "GDC.time.day_in_year": "DAY_OF_YEAR",
    "GDC.time.day_in_month": "DAY_OF_MONTH",
    "GDC.time.day_in_week": "DAY_OF_WEEK",
    "GDC.time.hour_in_day": "HOUR_OF_DAY",
    "GDC.time.minute_in_hour": "MINUTE_OF_HOUR",
}

_AGGREGATION_CONVERSION = {
    "sum": "SUM",
    "avg": "AVG",
    "count": "COUNT",
    "approximate_count": "APPROXIMATE_COUNT",
    "max": "MAX",
    "median": "MEDIAN",
    "min": "MIN",
    "runsum": "RUNSUM",
}

_ARITHMETIC_CONVERSION = {
    "sum": "SUM",
    "difference": "DIFFERENCE",
    "multiplication": "MULTIPLICATION",
    "ratio": "RATIO",
    "change": "CHANGE",
}


#
#
#


def _ref_extract_obj_id(ref: dict[str, Any]) -> ObjId:
    if "identifier" in ref:
        return ObjId(id=ref["identifier"]["id"], type=ref["identifier"]["type"])

    raise ValueError("invalid ref. must be identifier")


def _ref_extract(ref: dict[str, Any]) -> Union[str, ObjId]:
    try:
        return _ref_extract_obj_id(ref)
    except ValueError:
        pass

    if "localIdentifier" in ref:
        return ref["localIdentifier"]

    raise ValueError("invalid ref. must be identifier or localIdentifier")


def _convert_filter_to_computable(filter_obj: dict[str, Any]) -> Filter:
    if "positiveAttributeFilter" in filter_obj:
        f = filter_obj["positiveAttributeFilter"]
        # fallback to use URIs; SDK may be able to create filter with attr elements as uris...
        in_values = f["in"]["values"] if "values" in f["in"] else f["in"]["uris"]

        return PositiveAttributeFilter(label=_ref_extract(f["displayForm"]), values=in_values)

    elif "negativeAttributeFilter" in filter_obj:
        f = filter_obj["negativeAttributeFilter"]
        # fallback to use URIs; SDK may be able to create filter with attr elements as uris...
        not_in_values = f["notIn"]["values"] if "values" in f["notIn"] else f["notIn"]["uris"]

        return NegativeAttributeFilter(label=_ref_extract(f["displayForm"]), values=not_in_values)
    elif "relativeDateFilter" in filter_obj:
        f = filter_obj["relativeDateFilter"]

        # there is filter present, but uses all time
        if ("from" not in f) or ("to" not in f):
            return AllTimeFilter()

        return RelativeDateFilter(
            dataset=_ref_extract_obj_id(f["dataSet"]),
            granularity=_GRANULARITY_CONVERSION[f["granularity"]],
            from_shift=f["from"],
            to_shift=f["to"],
        )

    elif "absoluteDateFilter" in filter_obj:
        f = filter_obj["absoluteDateFilter"]

        return AbsoluteDateFilter(dataset=_ref_extract_obj_id(f["dataSet"]), from_date=f["from"], to_date=f["to"])
    elif "measureValueFilter" in filter_obj:
        f = filter_obj["measureValueFilter"]
        condition = f["condition"]

        if "comparison" in condition:
            c = condition["comparison"]
            treat_values_as_null = c["treatNullValuesAs"] if "treatNullValuesAs" in c else None

            return MetricValueFilter(
                metric=_ref_extract(f["measure"]),
                operator=c["operator"],
                values=c["value"],
                treat_nulls_as=treat_values_as_null,
            )
        elif "range" in condition:
            c = condition["range"]
            treat_values_as_null = c["treatNullValuesAs"] if "treatNullValuesAs" in c else None
            return MetricValueFilter(
                metric=_ref_extract(f["measure"]),
                operator=c["operator"],
                values=(c["from"], c["to"]),
                treat_nulls_as=treat_values_as_null,
            )
    elif "rankingFilter" in filter_obj:
        f = filter_obj["rankingFilter"]
        # mypy is unable to automatically convert Union[str, ObjId] to Union[str, ObjId, Attribute, Metric]
        # so use explicit cast here
        dimensionality = (
            [cast(Union[str, ObjId, Attribute, Metric], _ref_extract(a)) for a in f["attributes"]]
            if "attributes" in f
            else None
        )

        return RankingFilter(
            metrics=[_ref_extract(f["measure"])],
            dimensionality=dimensionality,
            operator=f["operator"],
            value=f["value"],
        )

    raise ValueError(f"Unable to convert filter {filter_obj}")


def _convert_metric_to_computable(metric: dict[str, Any]) -> Metric:
    m = metric["measure"]
    local_id = m["localIdentifier"]
    measure_def = m["definition"]

    if "measureDefinition" in measure_def:
        d = measure_def["measureDefinition"]
        aggregation = _AGGREGATION_CONVERSION[d["aggregation"]] if "aggregation" in d else None
        compute_ratio = d["computeRatio"] if "computeRatio" in d else False

        filters = [_convert_filter_to_computable(f) for f in d["filters"]] if "filters" in d else None

        return SimpleMetric(
            local_id=local_id,
            item=_ref_extract_obj_id(d["item"]),
            aggregation=aggregation,
            compute_ratio=compute_ratio,
            filters=filters,
        )

    elif "popMeasureDefinition" in measure_def:
        d = measure_def["popMeasureDefinition"]
        date_attributes = [PopDate(attribute=_ref_extract_obj_id(d["popAttribute"]), periods_ago=1)]

        return PopDateMetric(
            local_id=local_id,
            metric=d["measureIdentifier"],
            date_attributes=date_attributes,
        )

    elif "previousPeriodMeasure" in measure_def:
        d = measure_def["previousPeriodMeasure"]

        date_datasets = [PopDateDataset(_ref_extract(dd["dataSet"]), dd["periodsAgo"]) for dd in d["dateDataSets"]]

        return PopDatesetMetric(
            local_id=local_id,
            metric=d["measureIdentifier"],
            date_datasets=date_datasets,
        )

    elif "arithmeticMeasure" in measure_def:
        d = measure_def["arithmeticMeasure"]

        return ArithmeticMetric(
            local_id=local_id,
            operator=_ARITHMETIC_CONVERSION[d["operator"]],
            operands=d["measureIdentifiers"],
        )

    raise ValueError(f"Unable to convert measure {measure_def}")


#
#
#


class InsightMetric:
    """
    Represents metric placed on an insight.

    Note: this has different shape than object passed to execution.
    """

    def __init__(self, metric: dict[str, Any]) -> None:
        self._metric = metric
        self._m: dict[str, Any] = metric["measure"]
        self._d: dict[str, Any] = self._m["definition"]

    @property
    def local_id(self) -> str:
        return self._m["localIdentifier"]

    @property
    def alias(self) -> Optional[str]:
        return self._m.get("alias")

    @property
    def title(self) -> Optional[str]:
        return self._m.get("title")

    @property
    def format(self) -> Optional[str]:
        return self._m.get("format")

    @property
    def item(self) -> Optional[dict[str, Any]]:
        return safeget(self._d, ["measureDefinition", "item"])

    @property
    def aggregation(self) -> Optional[str]:
        return safeget(self._d, ["measureDefinition", "aggregation"])

    @property
    def item_id(self) -> Optional[str]:
        return safeget(self.item, ["identifier", "id"])

    @property
    def item_type(self) -> Optional[str]:
        return safeget(self.item, ["identifier", "type"])

    @property
    def is_time_comparison(self) -> bool:
        return "popMeasureDefinition" in self._d or "previousPeriodMeasure" in self._d

    @property
    def time_comparison_master(self) -> Optional[str]:
        """
        If this is a time comparison metric, return local_id of the master metric from which it is
        derived.

        :return: local_id of master metric, None if not a time comparison metric
        """
        return safeget(self._d, ["popMeasureDefinition", "measureIdentifier"]) or safeget(
            self._d, ["previousPeriodMeasure", "measureIdentifier"]
        )

    def as_computable(self) -> Metric:
        return _convert_metric_to_computable(self._metric)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"metric(local_id={self.local_id})"


class InsightAttribute:
    def __init__(self, attribute: dict[str, Any]) -> None:
        self._attribute = attribute
        self._a: dict[str, Any] = attribute["attribute"]

    @property
    def local_id(self) -> str:
        return self._a["localIdentifier"]

    @property
    def label_id(self) -> str:
        return self._a["displayForm"]["identifier"]["id"]

    @property
    def alias(self) -> Optional[str]:
        return self._a["alias"] if "alias" in self._a else None

    @property
    def label(self) -> dict[str, Any]:
        return self._a["displayForm"]

    @property
    def show_all_values(self) -> Optional[bool]:
        return self._a.get("showAllValues")

    def as_computable(self) -> Attribute:
        return Attribute(local_id=self.local_id, label=_ref_extract(self.label), show_all_values=self.show_all_values)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"attribute(local_id={self.local_id}, show_all_values={self.show_all_values})"


class InsightFilter:
    def __init__(self, f: dict[str, Any]) -> None:
        self._filter = f

    def as_computable(self) -> Filter:
        return _convert_filter_to_computable(self._filter)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return repr(self._filter)


class InsightBucket:
    def __init__(self, bucket: dict[str, Any]) -> None:
        self._b = bucket
        self._metrics: Optional[list[InsightMetric]] = None
        self._attributes: Optional[list[InsightAttribute]] = None

    @property
    def local_id(self) -> str:
        return self._b["localIdentifier"]

    @property
    def items(self) -> list[dict[str, Any]]:
        return self._b["items"]

    @property
    def metrics(self) -> list[InsightMetric]:
        if self._metrics is None:
            self._metrics = [InsightMetric(item) for item in self.items if "measure" in item]

        return self._metrics

    @property
    def attributes(self) -> list[InsightAttribute]:
        if self._attributes is None:
            self._attributes = [InsightAttribute(item) for item in self.items if "attribute" in item]

        return self._attributes

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"bucket(local_id={self.local_id}, items_count={len(self.items)})"


class Insight:
    def __init__(
        self,
        from_vis_obj: dict[str, Any],
        side_loads: Optional[SideLoads] = None,
    ) -> None:
        self._vo = from_vis_obj
        self._side_loads = SideLoads([]) if side_loads is None else side_loads

    @property
    def id(self) -> str:
        return self._vo["id"]

    @property
    def title(self) -> str:
        return self._vo["attributes"]["title"]

    @property
    def description(self) -> str:
        return self._vo["attributes"]["description"]

    @property
    def are_relations_valid(self) -> str:
        # Fallback to true for tests, where fixtures were generated without HTTP header activating this feature
        return self._vo["attributes"].get("areRelationsValid", "true")

    @property
    def buckets(self) -> list[InsightBucket]:
        return [InsightBucket(b) for b in self._vo["attributes"]["content"]["buckets"]]

    @property
    def filters(self) -> list[InsightFilter]:
        return [InsightFilter(f) for f in self._vo["attributes"]["content"]["filters"]]

    @property
    def sorts(self) -> list[Any]:
        return self._vo["attributes"]["content"]["sorts"]

    @property
    def properties(self) -> dict[str, Any]:
        return self._vo["attributes"]["content"]["properties"]

    @property
    def vis_url(self) -> str:
        return self._vo["attributes"]["content"]["visualizationUrl"]

    @property
    def metrics(self) -> list[InsightMetric]:
        return [m for b in self.buckets for m in b.metrics]

    @property
    def attributes(self) -> list[InsightAttribute]:
        return [a for b in self.buckets for a in b.attributes]

    @property
    def side_loads(self) -> SideLoads:
        return self._side_loads

    def get_metadata(self, id_obj: IdObjType) -> Optional[Any]:
        if not self._side_loads:
            return None

        # otherwise try to use the id object as is
        return self._side_loads.find(id_obj)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"insight(title='{self.title}', id='{self.id}', buckets='{str(self.buckets)}')'"


class InsightService:
    """
    Insight Service allows retrieval of insights from a GD.CN workspace. The insights are returned as instances of
    Insight which allows convenient introspection and necessary functions to convert the insight into a form where it
    can be sent for computation.

    Note: the insights are created using GD.CN Analytical Designer or using GoodData.UI SDK. They are stored as
    visualization objects with a free-form body. This body is specific for AD & SDK.
    The Insight wrapper exists to take care of these discrepancies.
    """

    # Note on the disabled checking:
    # generated client has issues parsing the vis objects; .. have to avoid return type checks
    #
    # note: the parsing is done lazily so it does not necessarily bomb on the next line but when trying to
    #  access returned object's properties

    def __init__(self, api_client: GoodDataApiClient) -> None:
        self._entities_api = api_client.entities_api

    def get_insights(self, workspace_id: str) -> list[Insight]:
        """
        Gets all insights for a workspace. The insights will contain side loaded metadata for all execution entities
        that they reference.

        Args:
             workspace_id (str):
                Workspace identification string e.g. "demo"
        Returns:
             list[Insight]:
                All available insights, each insight will contain side loaded metadata about the entities it references
        """
        get_func = functools.partial(
            self._entities_api.get_all_entities_visualization_objects,
            workspace_id,
            include=["ALL"],
            _check_return_type=False,
        )

        vis_objects = load_all_entities(get_func)
        side_loads = SideLoads(vis_objects.included)

        return [Insight(vis_obj, side_loads) for vis_obj in vis_objects.data]

    def get_insight(self, workspace_id: str, insight_id: str) -> Insight:
        """Gets a single insight from a workspace.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"
            insight_id (str):
                Insight identifier string e.g. "bikes"

        Returns:
            Insight:
                A single Insight object contains side loaded metadata about the entities it references
        """
        vis_obj = self._entities_api.get_entity_visualization_objects(
            workspace_id,
            object_id=insight_id,
            include=["ALL"],
            _check_return_type=False,
        )
        side_loads = SideLoads(vis_obj.included)

        return Insight(vis_obj.data, side_loads)
