# (C) 2021 GoodData Corporation
from __future__ import annotations

import functools
from typing import List

import gooddata_metadata_client.apis as metadata_apis
from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.compute_model import (
    AbsoluteDateFilter,
    AllTimeFilter,
    ArithmeticMetric,
    Attribute,
    MetricValueFilter,
    NegativeAttributeFilter,
    ObjId,
    PopDate,
    PopDateDataset,
    PopDateMetric,
    PopDatesetMetric,
    PositiveAttributeFilter,
    RankingFilter,
    RelativeDateFilter,
    SimpleMetric,
)
from gooddata_sdk.utils import Sideloads, load_all_entities

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


def _ref_extract(ref):
    if "identifier" in ref:
        return ObjId(id=ref["identifier"]["id"], type=ref["identifier"]["type"])
    elif "localIdentifier" in ref:
        return ref["localIdentifier"]

    raise ValueError("invalid ref. must be identifier or localIdentifier")


def _convert_filter_to_computable(filter_obj):
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
            dataset=_ref_extract(f["dataSet"]),
            granularity=_GRANULARITY_CONVERSION[f["granularity"]],
            from_shift=f["from"],
            to_shift=f["to"],
        )

    elif "absoluteDateFilter" in filter_obj:
        f = filter_obj["absoluteDateFilter"]

        return AbsoluteDateFilter(dataset=_ref_extract(f["dataSet"]), from_date=f["from"], to_date=f["to"])
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
        dimensionality = [_ref_extract(a) for a in f["attributes"]] if "attributes" in f else None

        return RankingFilter(
            metrics=[_ref_extract(f["measure"])],
            dimensionality=dimensionality,
            operator=f["operator"],
            value=f["value"],
        )

    raise ValueError(f"Unable to convert filter {filter_obj}")


def _convert_metric_to_computable(metric):
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
            item=_ref_extract(d["item"]),
            aggregation=aggregation,
            compute_ratio=compute_ratio,
            filters=filters,
        )

    elif "popMeasureDefinition" in measure_def:
        d = measure_def["popMeasureDefinition"]
        date_attributes = [PopDate(attribute=_ref_extract(d["popAttribute"]), periods_ago=1)]

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

    def __init__(self, metric=None):
        self._metric = metric
        self._m = metric["measure"]
        self._d = self._m["definition"]

    @property
    def local_id(self):
        return self._m["localIdentifier"]

    @property
    def alias(self):
        return self._m.get("alias")

    @property
    def title(self):
        return self._m.get("title")

    @property
    def format(self):
        return self._m.get("format")

    @property
    def item(self):
        if "measureDefinition" in self._d:
            return self._d["measureDefinition"]["item"]

        return None

    @property
    def item_id(self):
        item = self.item

        return item["identifier"]["id"] if item is not None else None

    @property
    def is_time_comparison(self):
        return "popMeasureDefinition" in self._d or "previousPeriodMeasure" in self._d

    @property
    def time_comparison_master(self):
        """
        If this is a time comparison metric, return local_id of the master metric from which it is
        derived.
        :return: local_id of master metric, None if not a time comparison metric
        """
        if "popMeasureDefinition" in self._d:
            return self._d["popMeasureDefinition"]["measureIdentifier"]
        elif "previousPeriodMeasure" in self._d:
            return self._d["previousPeriodMeasure"]["measureIdentifier"]

        return None

    def as_computable(self):
        return _convert_metric_to_computable(self._metric)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"metric(local_id={self.local_id})"


class InsightAttribute:
    def __init__(self, attribute):
        self._attribute = attribute
        self._a = attribute["attribute"]

    @property
    def local_id(self):
        return self._a["localIdentifier"]

    @property
    def label_id(self):
        return self._a["displayForm"]["identifier"]["id"]

    @property
    def alias(self):
        return self._a["alias"] if "alias" in self._a else None

    @property
    def label(self):
        return self._a["displayForm"]

    def as_computable(self):
        return Attribute(local_id=self.local_id, label=_ref_extract(self.label))

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"attribute(local_id={self.local_id})"


class InsightFilter:
    def __init__(self, f=None):
        self._filter = f

    def as_computable(self):
        return _convert_filter_to_computable(self._filter)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self._filter


class InsightBucket:
    def __init__(self, bucket=None):
        self._b = bucket
        self._metrics = None
        self._attributes = None

    @property
    def local_id(self):
        return self._b["localIdentifier"]

    @property
    def items(self):
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

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"bucket(local_id={self.local_id}, items_count={len(self.items)})"


class Insight:
    def __init__(self, from_vis_obj=None, sideloads=None):
        if sideloads is None:
            sideloads: Sideloads = Sideloads([])

        self._vo = from_vis_obj
        self._sideloads = sideloads

    @property
    def id(self):
        return self._vo["id"]

    @property
    def title(self):
        return self._vo["attributes"]["title"]

    @property
    def description(self):
        return self._vo["attributes"]["description"]

    @property
    def buckets(self) -> list[InsightBucket]:
        return [InsightBucket(b) for b in self._vo["attributes"]["content"]["buckets"]]

    @property
    def filters(self):
        return [InsightFilter(f) for f in self._vo["attributes"]["content"]["filters"]]

    @property
    def sorts(self):
        return self._vo["attributes"]["content"]["sorts"]

    @property
    def properties(self):
        return self._vo["attributes"]["content"]["properties"]

    @property
    def vis_url(self):
        return self._vo["attributes"]["content"]["visualizationUrl"]

    @property
    def metrics(self) -> list[InsightMetric]:
        return [m for b in self.buckets for m in b.metrics]

    @property
    def attributes(self):
        return [a for b in self.buckets for a in b.attributes]

    @property
    def sideloads(self):
        return self._sideloads

    def get_metadata(self, id_obj):
        if not self._sideloads:
            return None

        # otherwise try to use the id object as is
        return self._sideloads.find(id_obj)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
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

    def __init__(self, api_client: GoodDataApiClient):
        self._api = metadata_apis.WorkspaceObjectControllerApi(api_client.metadata_client)

    def get_insights(self, workspace_id) -> List[Insight]:
        """
        Gets all insights for a workspace. The insights will contain sideloaded metadata for all execution entities
        that they reference.

        :param workspace_id: identifier of workspace to load insights from
        :return: all available insights, each insight will contain sideloaded metadata about the entities it references
        :rtype: list[Insight]
        """
        get_func = functools.partial(
            self._api.get_all_entities_visualization_objects,
            workspace_id,
            include=["ALL"],
            _check_return_type=False,
        )

        vis_objects = load_all_entities(get_func)
        sideloads = Sideloads(vis_objects.included)

        return [Insight(vis_obj, sideloads) for vis_obj in vis_objects.data]

    def get_insight(self, workspace_id, insight_id) -> Insight:
        """
        Gets a single insight from a workspace.

        :param workspace_id: identifier of workspace to load insight from
        :param insight_id: identifier of the insight
        :return: single insight; the insight will contain sideloaded metadata about the entities it references
        :rtype: Insight
        """
        vis_obj = self._api.get_entity_visualization_objects(
            workspace_id,
            object_id=insight_id,
            include=["ALL"],
            _check_return_type=False,
        )
        sideloads = Sideloads(vis_obj.included)

        return Insight(vis_obj.data, sideloads)
