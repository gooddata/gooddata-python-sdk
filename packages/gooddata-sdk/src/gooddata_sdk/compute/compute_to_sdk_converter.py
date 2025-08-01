# (C) 2024 GoodData Corporation
from typing import Any, Union, cast

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
from gooddata_sdk.utils import ref_extract, ref_extract_obj_id


class ComputeToSdkConverter:
    """
    Provides functions to convert Compute API model objects represented as dictionaries to the SDK Compute model.
    We cannot use the Visualization converter as the Compute API model is different:
    - there are differences in naming: e.g. "label" vs "displayForm", "dataset" vs "dataSet"
    - there are differences in structure: e.g. "measure" vs "measureDefinition"

    The inputs to this converter should be dictionaries that come from parsing the JSON payloads
    used with the backend's /execute API endpoint.
    """

    @staticmethod
    def convert_attribute(attribute_dict: dict[str, Any]) -> Attribute:
        """
        Converts attribute dictionary to the SDK Compute model.
        :param attribute_dict: the attribute dictionary to convert
        :return: the converted attribute
        """
        return Attribute(
            local_id=attribute_dict["localIdentifier"],
            label=attribute_dict["label"]["identifier"]["id"],
            show_all_values=attribute_dict["showAllValues"],
        )

    @staticmethod
    def convert_filter(filter_dict: dict[str, Any]) -> Filter:
        """
        Converts filter dictionary to the SDK Compute model.
        :param filter_dict: the filter dictionary to convert
        :return: the converted filter
        """
        if "positiveAttributeFilter" in filter_dict:
            f = filter_dict["positiveAttributeFilter"]
            return PositiveAttributeFilter(label=ref_extract(f["label"]), values=f["in"]["values"])

        if "negativeAttributeFilter" in filter_dict:
            f = filter_dict["negativeAttributeFilter"]
            return NegativeAttributeFilter(label=ref_extract(f["label"]), values=f["notIn"]["values"])

        if "relativeDateFilter" in filter_dict:
            f = filter_dict["relativeDateFilter"]

            # there is a filter present, but means all time
            if ("from" not in f) or ("to" not in f):
                return AllTimeFilter(ref_extract_obj_id(f["dataset"]))

            return RelativeDateFilter(
                dataset=ref_extract_obj_id(f["dataset"]),
                granularity=f["granularity"],
                from_shift=f["from"],
                to_shift=f["to"],
            )

        if "absoluteDateFilter" in filter_dict:
            f = filter_dict["absoluteDateFilter"]

            return AbsoluteDateFilter(dataset=ref_extract_obj_id(f["dataset"]), from_date=f["from"], to_date=f["to"])

        if "comparisonMeasureValueFilter" in filter_dict:
            f = filter_dict["comparisonMeasureValueFilter"]

            return MetricValueFilter(
                metric=ref_extract(f["measure"]),
                operator=f["operator"],
                values=f["value"],
                treat_nulls_as=f.get("treatNullValuesAs"),
            )

        if "rangeMeasureValueFilter" in filter_dict:
            f = filter_dict["rangeMeasureValueFilter"]

            return MetricValueFilter(
                metric=ref_extract(f["measure"]),
                operator=f["operator"],
                values=(f["from"], f["to"]),
                treat_nulls_as=f.get("treatNullValuesAs"),
            )

        if "rankingFilter" in filter_dict:
            f = filter_dict["rankingFilter"]

            # mypy is unable to automatically convert Union[str, ObjId] to Union[str, ObjId, Attribute, Metric]
            # so use explicit cast here
            dimensionality = (
                [cast(Union[str, ObjId, Attribute, Metric], ref_extract(a)) for a in f["dimensionality"]]
                if "dimensionality" in f
                else None
            )

            return RankingFilter(
                metrics=[ref_extract(m) for m in f["measures"]],
                dimensionality=dimensionality,
                operator=f["operator"],
                value=f["value"],
            )

        raise ValueError(f"Unsupported filter definition type: {filter_dict}")

    @staticmethod
    def convert_metric(metric_dict: dict[str, Any]) -> Metric:
        """
        Converts metric dictionary to the SDK Compute model.
        :param metric_dict: the metric dictionary to convert
        :return: the converted metric
        """
        definition = metric_dict["definition"]
        local_id = metric_dict["localIdentifier"]

        if "measure" in definition:
            d = definition["measure"]
            aggregation = d.get("aggregation", None)
            compute_ratio = d.get("computeRatio", False)

            filters = [ComputeToSdkConverter.convert_filter(f) for f in d["filters"]] if "filters" in d else None

            return SimpleMetric(
                local_id=local_id,
                item=ref_extract_obj_id(d["item"]),
                aggregation=aggregation,
                compute_ratio=compute_ratio,
                filters=filters,
            )

        if "arithmeticMeasure" in definition:
            d = definition["arithmeticMeasure"]
            return ArithmeticMetric(
                local_id=local_id,
                operator=d["operator"],
                operands=[o["localIdentifier"] for o in d["measureIdentifiers"]],
            )

        if "overPeriodMeasure" in definition:
            d = definition["overPeriodMeasure"]
            date_attributes = [
                PopDate(attribute=ref_extract_obj_id(item["attribute"]), periods_ago=item["periodsAgo"])
                for item in d["dateAttributes"]
            ]

            return PopDateMetric(
                local_id=local_id,
                metric=d["measureIdentifier"]["localIdentifier"],
                date_attributes=date_attributes,
            )

        if "previousPeriodMeasure" in definition:
            d = definition["previousPeriodMeasure"]

            date_datasets = [PopDateDataset(ref_extract(dd["dataset"]), dd["periodsAgo"]) for dd in d["dateDatasets"]]

            return PopDatesetMetric(
                local_id=local_id,
                metric=d["measureIdentifier"]["localIdentifier"],
                date_datasets=date_datasets,
            )

        raise ValueError(f"Unsupported metric definition type: {metric_dict}")
