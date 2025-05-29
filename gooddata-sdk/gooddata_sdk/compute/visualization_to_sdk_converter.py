# (C) 2025 GoodData Corporation
from typing import Any

from gooddata_sdk.compute.model.attribute import Attribute
from gooddata_sdk.compute.model.base import ObjId
from gooddata_sdk.compute.model.filter import (
    AbsoluteDateFilter,
    AllTimeFilter,
    Filter,
    NegativeAttributeFilter,
    PositiveAttributeFilter,
    RelativeDateFilter,
)
from gooddata_sdk.compute.model.metric import Metric, SimpleMetric


class VisualizationToSdkConverter:
    """
    Provides functions to convert visualization objects (dicts) to the SDK Compute model.
    The input should be a visualization object as returned by `ai_chat`.
    """

    @staticmethod
    def convert_attribute(attr_dict: dict[str, Any]) -> Attribute:
        """
        Converts a visualization attribute dict to an SDK Attribute.
        Expects keys:
            - id: str - The identifier of the attribute
            - title: str - The display title/label for the attribute
        Returns:
            Attribute: An SDK Attribute object with local_id and label set
        """
        local_id = attr_dict["id"]
        label = attr_dict["id"]
        return Attribute(local_id=local_id, label=label)

    @staticmethod
    def convert_filter(filter_dict: dict[str, Any]) -> Filter:
        """
        Converts a visualization filter dict to an SDK Filter.
        Expects keys:
            - using: str - The identifier of the attribute/dataset to filter on
            - include: list[str] (optional) - Values to include in positive filter
            - exclude: list[str] (optional) - Values to exclude in negative filter
            - from: str (optional) - Start date/shift for date filters
            - to: str (optional) - End date/shift for date filters
            - granularity: str (optional) - Time granularity for relative date filters
        Returns:
            Filter: One of:
                - PositiveAttributeFilter: When include values specified
                - NegativeAttributeFilter: When exclude values specified
                - RelativeDateFilter: When granularity and from/to shifts specified
                - AbsoluteDateFilter: When from/to dates specified
                - AllTimeFilter: When no date range specified
        """
        using = filter_dict["using"]
        include = filter_dict.get("include")
        exclude = filter_dict.get("exclude")
        _from = filter_dict.get("from")
        _to = filter_dict.get("to")
        granularity = filter_dict.get("granularity")

        if include is not None:
            return PositiveAttributeFilter(label=ObjId(using, "label"), values=include)
        elif exclude is not None:
            return NegativeAttributeFilter(label=ObjId(using, "label"), values=exclude)
        elif granularity is not None and _from is not None and _to is not None:
            return RelativeDateFilter(
                dataset=ObjId(using, "dataset"), granularity=granularity, from_shift=_from, to_shift=_to
            )
        elif _from is not None and _to is not None:
            return AbsoluteDateFilter(dataset=ObjId(using, "dataset"), from_date=_from, to_date=_to)
        else:
            return AllTimeFilter(dataset=ObjId(using, "dataset"))

    @staticmethod
    def convert_metric(metric_dict: dict[str, Any]) -> Metric:
        """
        Converts a visualization metric dict to an SDK Metric.
        Expects keys:
            - id: str - The identifier of the metric/fact/attribute
            - type: str - The type of object ("metric", "fact", or "attribute")
            - aggFunction: str (optional) - Aggregation function for facts/attributes
        Returns:
            Metric: One of:
                - SimpleMetric with no aggregation for metrics
                - SimpleMetric with aggregation for facts
                - SimpleMetric with "count" aggregation for attributes
        """
        local_id = metric_dict["id"]
        item = ObjId(metric_dict["id"], metric_dict["type"])

        if metric_dict["type"] in ["metric", "fact"]:
            aggregation = metric_dict.get("aggFunction")
            return SimpleMetric(local_id=local_id, item=item, aggregation=aggregation)

        elif metric_dict["type"] == "attribute":
            aggregation = "count"
            return SimpleMetric(local_id=local_id, item=item, aggregation=aggregation)

        else:
            raise ValueError(f"Unsupported metric type: {metric_dict['type']}")
