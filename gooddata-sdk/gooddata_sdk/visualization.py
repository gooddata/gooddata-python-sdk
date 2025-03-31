# (C) 2021 GoodData Corporation
from __future__ import annotations

import functools
from collections import defaultdict
from enum import Enum
from typing import Any, Optional, Union, cast

from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.compute.model.attribute import Attribute
from gooddata_sdk.compute.model.base import ObjId
from gooddata_sdk.compute.model.filter import (
    AbsoluteDateFilter,
    AllMetricValueFilter,
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
from gooddata_sdk.utils import IdObjType, SideLoads, load_all_entities, ref_extract, ref_extract_obj_id, safeget

#
# Conversion from types stored in visualization into the gooddata_afm_client models.
# Visualization is created by GD.UI SDK
# and is persisted in the freeform 'vis object' in the metadata.
# The types from SDK model are stored there.
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


class BucketType(Enum):
    """
    Enum used for differentiating between types of Visualization buckets.
    """

    UNDEFINED = 0
    MEASURES = 1
    ROWS = 2
    COLS = 3


_LOCAL_ID_TO_BUCKET_TYPE = defaultdict(
    lambda: BucketType.UNDEFINED,
    {
        "measures": BucketType.MEASURES,
        "attribute": BucketType.ROWS,
        "columns": BucketType.COLS,
    },
)
"""Mapping of bucket localIdentifiers to their respective BucketType counterparts."""

_BUCKET_TYPE_TO_LOCAL_ID = {
    BucketType.UNDEFINED: "undefined",
    BucketType.MEASURES: "measures",
    BucketType.ROWS: "attribute",
    BucketType.COLS: "columns",
}
"""Mapping of bucket BucketTypes to their respective localIdentifier counterparts."""


class SortType(Enum):
    """
    Enum used for differentiating between SortItem API objects used in conjunction with _SORT_KEY_TO_SORT_TYPE.
    """

    UNDEFINED = 0
    ATTRIBUTE = 1
    MEASURE = 2


_SORT_KEY_TO_SORT_TYPE = defaultdict(
    lambda: SortType.UNDEFINED,
    {
        "attributeSortItem": SortType.ATTRIBUTE,
        "measureSortItem": SortType.MEASURE,
    },
)
"""Mapping of SortItem key values to their respective Enum types."""


class SortDirection(str, Enum):
    """
    Enum used for differentiating between ascending and descending order direction.
    """

    ASC = "asc"
    DESC = "desc"


class LocatorItemType(str, Enum):
    """
    Enum used for differentiating between dataColumnLocators API objects.
    """

    MEASURE = "measureLocatorItem"
    ATTRIBUTE = "attributeLocatorItem"


class AttributeSortType(Enum):
    """
    Enum used for differentiating between different AttributeSortKey sort types.
    """

    UNDEFINED = 0
    DEFAULT = 1
    AREA = 2


#
#
#


def _convert_filter_to_computable(filter_obj: dict[str, Any]) -> Filter:
    if "positiveAttributeFilter" in filter_obj:
        f = filter_obj["positiveAttributeFilter"]
        # fallback to use URIs; SDK may be able to create filter with attr elements as uris...
        in_values = f["in"]["values"] if "values" in f["in"] else f["in"]["uris"]

        return PositiveAttributeFilter(label=ref_extract(f["displayForm"]), values=in_values)

    elif "negativeAttributeFilter" in filter_obj:
        f = filter_obj["negativeAttributeFilter"]
        # fallback to use URIs; SDK may be able to create filter with attr elements as uris...
        not_in_values = f["notIn"]["values"] if "values" in f["notIn"] else f["notIn"]["uris"]

        return NegativeAttributeFilter(label=ref_extract(f["displayForm"]), values=not_in_values)
    elif "relativeDateFilter" in filter_obj:
        f = filter_obj["relativeDateFilter"]

        # there is filter present, but uses all time
        if ("from" not in f) or ("to" not in f):
            return AllTimeFilter(ref_extract_obj_id(f["dataSet"]))

        return RelativeDateFilter(
            dataset=ref_extract_obj_id(f["dataSet"]),
            granularity=_GRANULARITY_CONVERSION[f["granularity"]],
            from_shift=f["from"],
            to_shift=f["to"],
        )

    elif "absoluteDateFilter" in filter_obj:
        f = filter_obj["absoluteDateFilter"]

        return AbsoluteDateFilter(dataset=ref_extract_obj_id(f["dataSet"]), from_date=f["from"], to_date=f["to"])
    elif "measureValueFilter" in filter_obj:
        f = filter_obj["measureValueFilter"]

        # no condition means no limitation
        if "condition" not in f:
            return AllMetricValueFilter(metric=ref_extract(f["measure"]))

        condition = f["condition"]

        if "comparison" in condition:
            c = condition["comparison"]
            treat_values_as_null = c.get("treatNullValuesAs")

            return MetricValueFilter(
                metric=ref_extract(f["measure"]),
                operator=c["operator"],
                values=c["value"],
                treat_nulls_as=treat_values_as_null,
            )
        elif "range" in condition:
            c = condition["range"]
            treat_values_as_null = c.get("treatNullValuesAs")
            return MetricValueFilter(
                metric=ref_extract(f["measure"]),
                operator=c["operator"],
                values=(c["from"], c["to"]),
                treat_nulls_as=treat_values_as_null,
            )
    elif "rankingFilter" in filter_obj:
        f = filter_obj["rankingFilter"]
        # mypy is unable to automatically convert Union[str, ObjId] to Union[str, ObjId, Attribute, Metric]
        # so use explicit cast here
        dimensionality = (
            [cast(Union[str, ObjId, Attribute, Metric], ref_extract(a)) for a in f["attributes"]]
            if "attributes" in f
            else None
        )

        return RankingFilter(
            metrics=[ref_extract(f["measure"])],
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
        compute_ratio = d.get("computeRatio", False)

        filters = [_convert_filter_to_computable(f) for f in d["filters"]] if "filters" in d else None

        return SimpleMetric(
            local_id=local_id,
            item=ref_extract_obj_id(d["item"]),
            aggregation=aggregation,
            compute_ratio=compute_ratio,
            filters=filters,
        )

    elif "popMeasureDefinition" in measure_def:
        d = measure_def["popMeasureDefinition"]
        date_attributes = [PopDate(attribute=ref_extract_obj_id(d["popAttribute"]), periods_ago=1)]

        return PopDateMetric(
            local_id=local_id,
            metric=d["measureIdentifier"],
            date_attributes=date_attributes,
        )

    elif "previousPeriodMeasure" in measure_def:
        d = measure_def["previousPeriodMeasure"]

        date_datasets = [PopDateDataset(ref_extract(dd["dataSet"]), dd["periodsAgo"]) for dd in d["dateDataSets"]]

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


class VisualizationMetric:
    """
    Represents metric placed on a visualization.

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


class VisualizationAttribute:
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
        return self._a.get("alias")

    @property
    def label(self) -> dict[str, Any]:
        return self._a["displayForm"]

    @property
    def show_all_values(self) -> Optional[bool]:
        return self._a.get("showAllValues")

    def as_computable(self) -> Attribute:
        return Attribute(local_id=self.local_id, label=ref_extract(self.label), show_all_values=self.show_all_values)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"attribute(local_id={self.local_id}, show_all_values={self.show_all_values})"


class VisualizationTotal:
    def __init__(self, total: dict[str, Any]) -> None:
        self._t = total

    @property
    def type(self) -> str:
        return self._t["type"]

    @property
    def measure_id(self) -> str:
        return self._t["measureIdentifier"]

    @property
    def attribute_id(self) -> str:
        return self._t["attributeIdentifier"]

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"total(type={self.type}, measureIdentifier={self.measure_id}, attributeIdentifier={self.attribute_id})"


class VisualizationFilter:
    def __init__(self, f: dict[str, Any]) -> None:
        self._filter = f

    def as_computable(self) -> Filter:
        return _convert_filter_to_computable(self._filter)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return repr(self._filter)


class VisualizationAttributeFilterConfig:
    """
    Represents attribute filter configuration used by a visualization.
    """

    def __init__(self, afc: tuple[str, Any]) -> None:
        local_id, data = afc
        self._local_id = local_id
        self._data = data

    @property
    def local_id(self) -> str:
        return self._local_id

    @property
    def label_id(self) -> str:
        return self._data["displayAsLabel"]["identifier"]["id"]

    @property
    def type(self) -> str:
        return self._data["displayAsLabel"]["identifier"]["type"]

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return (
            f"VisualizationAttributeFilterConfig(local_id='{self.local_id}', label_id='{self.label_id}', "
            f"type='{self.type}')"
        )


class VisualizationSortLocator:
    def __init__(self, locator: dict[str, str], locator_type: LocatorItemType) -> None:
        self._locator = locator
        self.type = locator_type

    @property
    def locator(self) -> dict[str, str]:
        return self._locator


class VisualizationSort:
    def __init__(self, sort: dict[str, Any]) -> None:
        sort_keys = list(sort.keys())
        sort_key = sort_keys[0] if sort_keys else ""
        self._sort = sort[sort_key] if sort_key else {}
        self._locators: Optional[list[VisualizationSortLocator]] = None
        self.type = _SORT_KEY_TO_SORT_TYPE[sort_key]

    @property
    def direction(self) -> SortDirection:
        return SortDirection(self._sort["direction"])

    @property
    def attribute_identifier(self) -> str:
        return self._sort["attributeIdentifier"] if self.type == SortType.ATTRIBUTE else ""

    @property
    def aggregation(self) -> Optional[str]:
        return self._sort.get("aggregation")

    @property
    def attribute_sort_type(self) -> AttributeSortType:
        if self.type != SortType.ATTRIBUTE:
            return AttributeSortType.UNDEFINED
        return AttributeSortType.AREA if self.aggregation else AttributeSortType.DEFAULT

    def _create_locator(self, locator: dict[str, dict[str, str]]) -> VisualizationSortLocator:
        # Single key-value pair is expected in the locator param
        ((locator_key, locator_val),) = locator.items()
        return VisualizationSortLocator(
            locator=locator_val,
            locator_type=LocatorItemType(locator_key),
        )

    @property
    def locators(self) -> list[VisualizationSortLocator]:
        if self._locators is None:
            self._locators = (
                [self._create_locator(locator) for locator in self._sort["locators"] if locator]
                if self.type == SortType.MEASURE
                else []
            )
        return self._locators


class VisualizationBucket:
    def __init__(self, bucket: dict[str, Any]) -> None:
        self._b = bucket
        self._metrics: Optional[list[VisualizationMetric]] = None
        self._attributes: Optional[list[VisualizationAttribute]] = None
        self._totals: Optional[list[VisualizationTotal]] = None
        self.type = _LOCAL_ID_TO_BUCKET_TYPE[self.local_id]

    @property
    def local_id(self) -> str:
        return self._b["localIdentifier"]

    @property
    def items(self) -> list[dict[str, Any]]:
        return self._b["items"]

    @property
    def metrics(self) -> list[VisualizationMetric]:
        if self._metrics is None:
            self._metrics = [VisualizationMetric(item) for item in self.items if "measure" in item]

        return self._metrics

    @property
    def attributes(self) -> list[VisualizationAttribute]:
        if self._attributes is None:
            self._attributes = [VisualizationAttribute(item) for item in self.items if "attribute" in item]

        return self._attributes

    @property
    def totals(self) -> list[VisualizationTotal]:
        if self._totals is None:
            self._totals = [VisualizationTotal(total) for total in self._b["totals"]] if "totals" in self._b else []

        return self._totals

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"bucket(local_id={self.local_id}, items_count={len(self.items)}, total_count={len(self.totals)})"


class Visualization:
    def __init__(
        self,
        from_vis_obj: dict[str, Any],
        side_loads: Optional[SideLoads] = None,
    ) -> None:
        self._vo = from_vis_obj
        self._attribute_filter_configs: Optional[list[VisualizationAttributeFilterConfig]] = None
        self._buckets: Optional[list[VisualizationBucket]] = None
        self._filters: Optional[list[VisualizationFilter]] = None
        self._sorts: Optional[list[VisualizationSort]] = None
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
    def attribute_filter_configs(self) -> Optional[list[VisualizationAttributeFilterConfig]]:
        visualization_attribute_filter_configs = safeget(self._vo, ["attributes", "content", "attributeFilterConfigs"])
        if self._attribute_filter_configs is None and visualization_attribute_filter_configs is not None:
            self._attribute_filter_configs = [
                VisualizationAttributeFilterConfig(afc) for afc in visualization_attribute_filter_configs.items()
            ]
        return self._attribute_filter_configs

    @property
    def buckets(self) -> list[VisualizationBucket]:
        if self._buckets is None:
            self._buckets = [VisualizationBucket(b) for b in self._vo["attributes"]["content"]["buckets"]]
        return self._buckets

    @property
    def filters(self) -> list[VisualizationFilter]:
        if self._filters is None:
            self._filters = [VisualizationFilter(f) for f in self._vo["attributes"]["content"]["filters"]]
        return self._filters

    @filters.setter
    def filters(self, filters: list[VisualizationFilter]) -> None:
        self._filters = filters

    @property
    def sorts(self) -> list[VisualizationSort]:
        if self._sorts is None:
            self._sorts = (
                [VisualizationSort(s) for s in self._vo["attributes"]["content"]["sorts"]]
                if "sorts" in self._vo["attributes"]["content"]
                else []
            )
        return self._sorts

    @property
    def properties(self) -> dict[str, Any]:
        return self._vo["attributes"]["content"]["properties"]

    @property
    def vis_url(self) -> str:
        return self._vo["attributes"]["content"]["visualizationUrl"]

    @property
    def metrics(self) -> list[VisualizationMetric]:
        return [m for b in self.buckets for m in b.metrics]

    @property
    def attributes(self) -> list[VisualizationAttribute]:
        return [a for b in self.buckets for a in b.attributes]

    def get_bucket_of_type(self, bucket_type: BucketType) -> VisualizationBucket:
        for b in self.buckets:
            if b.type == bucket_type:
                return b
        # Return empty bucket if not found
        return VisualizationBucket({"items": [], "localIdentifier": _BUCKET_TYPE_TO_LOCAL_ID[bucket_type]})

    def has_bucket_of_type(self, bucket_type: BucketType) -> bool:
        return any(b.type == bucket_type for b in self.buckets)

    def has_row_and_col_totals(self) -> bool:
        row_bucket = self.get_bucket_of_type(BucketType.ROWS)
        col_bucket = self.get_bucket_of_type(BucketType.COLS)
        return len(row_bucket.totals) > 0 and len(col_bucket.totals) > 0

    @property
    def side_loads(self) -> SideLoads:
        return self._side_loads

    def get_metadata(self, id_obj: IdObjType) -> Optional[Any]:
        if not self._side_loads:
            return None

        # otherwise, try to use the id object as is
        return self._side_loads.find(id_obj)

    def get_labels_and_formats(self) -> tuple[dict[str, str], dict[str, str]]:
        """
        Extracts labels and custom measure formats from the visualization.

        :return: tuple of labels dict ({"label_id":"Label"}) and formats dict ({"measure_id":"#,##0.00"})
        """
        labels = {}
        formats = {}
        for bucket in self.buckets:
            for item in bucket.items:
                for item_values in item.values():
                    label = item_values.get("alias", item_values.get("title", None))
                    if label is not None:
                        labels[item_values["localIdentifier"]] = label
                    if "format" in item_values:
                        formats[item_values["localIdentifier"]] = item_values["format"]
        return labels, formats

    def get_filters_description(self, labels: dict[str, str], format_locale: Optional[str] = None) -> list[str]:
        return [f.as_computable().description(labels, format_locale) for f in self.filters]

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"visualization(title='{self.title}', id='{self.id}', buckets='{str(self.buckets)}')'"


class VisualizationService:
    """
    Visualization Service allows retrieval of visualizations from a local GD workspace.
    The visualizations are returned as instances of
    Visualization,
    which allows convenient introspection and necessary functions to convert the visualization into a form where it
    can be sent for computation.

    Note: the visualizations are created using GD Analytical Designer or using GoodData.UI SDK.
    They are stored as
    visualization objects with a free-form body.
    This body is specific for AD & SDK.
    The Visualization wrapper exists to take care of these discrepancies.
    """

    # Note on the disabled checking:
    # generated client has issues parsing the vis objects; .. have to avoid return type checks
    #
    # note: the parsing is done lazily so it does not necessarily bomb on the next line but when trying to
    #  access returned object's properties

    def __init__(self, api_client: GoodDataApiClient) -> None:
        self._entities_api = api_client.entities_api

    def get_visualizations(self, workspace_id: str) -> list[Visualization]:
        """
        Gets all visualizations for a workspace.
        The visualizations will contain side loaded metadata for all execution entities
        that they reference.

        Args:
             workspace_id (str):
                Workspace identification string e.g. "demo"
        Returns:
             list[Visualization]:
                All available visualizations,
                each visualization will contain side loaded metadata about the entities it references
        """
        get_func = functools.partial(
            self._entities_api.get_all_entities_visualization_objects,
            workspace_id,
            include=["ALL"],
            _check_return_type=False,
        )

        vis_objects = load_all_entities(get_func)
        side_loads = SideLoads(vis_objects.included)

        return [Visualization(vis_obj, side_loads) for vis_obj in vis_objects.data]

    def get_visualization(
        self, workspace_id: str, visualization_id: str, timeout: Optional[Union[int, float, tuple]] = None
    ) -> Visualization:
        """Gets a single visualization from a workspace.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"
            visualization_id (str):
                Visualization identifier string e.g. "bikes"
            timeout (int | float | tuple):
                Timeout in seconds for the request. If a tuple is provided, the first element is the connect timeout
                and the second element is the read timeout. If a single value is provided, it is used as both connect
                and read timeout. If None, the default timeout is used.

        Returns:
            Visualization:
                A single visualization object contains side loaded metadata about the entities it references
        """
        vis_obj = self._entities_api.get_entity_visualization_objects(
            workspace_id,
            object_id=visualization_id,
            include=["ALL"],
            _check_return_type=False,
            _request_timeout=timeout,
        )
        side_loads = None
        if hasattr(vis_obj, "included"):
            side_loads = SideLoads(vis_obj.included)

        return Visualization(vis_obj.data, side_loads)
