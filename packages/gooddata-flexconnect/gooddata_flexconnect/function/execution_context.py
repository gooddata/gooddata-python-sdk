# (C) 2024 GoodData Corporation
import enum
from dataclasses import dataclass
from typing import Callable, Optional, Union

from gooddata_sdk import (
    AbsoluteDateFilter,
    Attribute,
    CatalogDependsOn,
    CatalogDependsOnDateFilter,
    CatalogFilterBy,
    CatalogValidateByItem,
    ComputeToSdkConverter,
    Filter,
    Metric,
    RelativeDateFilter,
)
from typing_extensions import TypeAlias, TypeVar

TInput = TypeVar("TInput")
TResult = TypeVar("TResult")


def none_safe(func: Callable[[TInput], TResult]) -> Callable[[Optional[TInput]], Optional[TResult]]:
    """
    Decorator that makes the unary function safe for None input.
    If the only argument is None, the function returns None.
    """

    def wrapper(arg: Optional[TInput]) -> Optional[TResult]:
        if arg is None:
            return None
        return func(arg)

    return wrapper


def _dict_to_request_attributes(attributes: list[dict]) -> list[Attribute]:
    return [ComputeToSdkConverter.convert_attribute(a) for a in attributes]


def _dict_to_request_metrics(metrics: list[dict]) -> list[Metric]:
    return [ComputeToSdkConverter.convert_metric(m) for m in metrics]


def _dict_to_request_filters(filters: list[dict]) -> list[Filter]:
    return [ComputeToSdkConverter.convert_filter(f) for f in filters]


class ExecutionType(enum.Enum):
    """
    Type of the execution.
    """

    REPORT = "REPORT"
    """
    Execution of the report.
    """

    LABEL_ELEMENTS = "LABEL_ELEMENTS"
    """
    Collect label elements execution.
    """


@dataclass
class ExecutionContextAttributeSorting:
    """
    Information about the sorting of an attribute.
    """

    sort_column: str
    """
    Column to sort by.
    """

    sort_direction: str
    """
    Direction of the sorting.
    """


@none_safe
def _dict_to_execution_context_attribute_sorting(d: dict) -> ExecutionContextAttributeSorting:
    return ExecutionContextAttributeSorting(
        sort_column=d["sortColumn"],
        sort_direction=d["sortDirection"],
    )


@dataclass
class ExecutionContextAttribute:
    """
    Information about an attribute used in the execution.
    """

    attribute_identifier: str
    """
    Identifier of the attribute used.
    """

    attribute_title: str
    """
    Title of the attribute used.
    """

    label_identifier: str
    """
    Identifier of the particular label used.
    """

    label_title: str
    """
    Title of the particular label used.
    """

    date_granularity: Optional[str]
    """
    Date granularity of the attribute if it is a date attribute.
    """

    sorting: Optional[ExecutionContextAttributeSorting]
    """
    Sorting of the attribute. If not present, the attribute is not sorted.
    """

    @staticmethod
    def from_dict(d: Optional[dict]) -> Optional["ExecutionContextAttribute"]:
        """
        Create ExecutionContextAttribute from a dictionary.
        :param d: the dictionary to parse
        """
        if not d:
            return None
        return ExecutionContextAttribute(
            attribute_title=d["attributeTitle"],
            attribute_identifier=d["attributeIdentifier"],
            label_title=d["labelTitle"],
            label_identifier=d["labelIdentifier"],
            date_granularity=d.get("dateGranularity"),
            sorting=_dict_to_execution_context_attribute_sorting(d.get("sorting")),
        )


@dataclass
class ExecutionContextPositiveAttributeFilter:
    """
    Information about the positive attribute filter.
    """

    label_identifier: str
    """
    Identifier of the label used.
    """

    values: list[Optional[str]]
    """
    Values of the filter.
    """


@dataclass
class ExecutionContextNegativeAttributeFilter:
    """
    Information about the negative attribute filter.
    """

    label_identifier: str
    """
    Identifier of the label used.
    """

    values: list[Optional[str]]
    """
    Values of the filter.
    """


@dataclass
class ExecutionContextRelativeDateFilter:
    """
    Information about the relative date filter.
    """

    dataset_identifier: str
    """
    Identifier of the dataset used.
    """

    granularity: str
    """
    Granularity of the filter.
    """

    from_shift: int
    """
    Shift from the start of the period.
    """

    to_shift: int
    """
    Shift from the end of the period.
    """


@dataclass
class ExecutionContextAbsoluteDateFilter:
    """
    Information about the absolute date filter.
    """

    dataset_identifier: str
    """
    Identifier of the dataset used.
    """

    from_date: str
    """
    Start date of the filter.
    """

    to_date: str
    """
    End date of the filter.
    """


ExecutionContextFilter: TypeAlias = Union[
    ExecutionContextPositiveAttributeFilter,
    ExecutionContextNegativeAttributeFilter,
    ExecutionContextRelativeDateFilter,
    ExecutionContextAbsoluteDateFilter,
]


@dataclass
class ExecutionRequest:
    """
    Information about the execution request that is sent to the FlexConnect function.
    DEPRECATED: Use ReportExecutionRequest instead.
    """

    attributes: list[Attribute]
    """
    All the attributes that are part of the execution request.
    """

    metrics: list[Metric]
    """
    All the metrics that are part of the execution request.
    """

    filters: list[Filter]
    """
    All the filters that are part of the execution request.
    """

    @staticmethod
    def from_dict(d: dict) -> "ExecutionRequest":
        """
        Create ExecutionRequest from a dictionary.
        :param d: the dictionary to parse
        """
        return ExecutionRequest(
            attributes=_dict_to_request_attributes(d.get("attributes", [])),
            metrics=_dict_to_request_metrics(d.get("measures", [])),
            filters=_dict_to_request_filters(d.get("filters", [])),
        )


@dataclass
class ReportExecutionRequest:
    """
    Information about the report execution request.
    """

    attributes: list[Attribute]
    """
    All the attributes that are part of the execution request.
    """

    metrics: list[Metric]
    """
    All the metrics that are part of the execution request.
    """

    filters: list[Filter]
    """
    All the filters that are part of the execution request.
    """

    @staticmethod
    @none_safe
    def from_dict(d: dict) -> "ReportExecutionRequest":
        """
        Create ReportExecutionRequest from a dictionary.
        :param d: the dictionary to parse
        """
        return ReportExecutionRequest(
            attributes=_dict_to_request_attributes(d.get("attributes", [])),
            metrics=_dict_to_request_metrics(d.get("measures", [])),
            filters=_dict_to_request_filters(d.get("filters", [])),
        )


DependsOn: TypeAlias = Union[CatalogDependsOn, CatalogDependsOnDateFilter]


def _dict_to_depends_on(d: dict) -> DependsOn:
    if "label" in d:
        return CatalogDependsOn(
            label=d["label"],
            values=d["values"],
            complement_filter=d.get("complementFilter", False),
        )

    date_filter = d["dateFilter"]
    if "from" in date_filter:
        return CatalogDependsOnDateFilter(
            date_filter=AbsoluteDateFilter(
                dataset=date_filter["dataset"],
                from_date=date_filter["from"],
                to_date=date_filter["to"],
            )
        )

    return CatalogDependsOnDateFilter(
        date_filter=RelativeDateFilter(
            dataset=date_filter["dataset"],
            granularity=date_filter["granularity"],
            from_shift=date_filter["from"],
            to_shift=date_filter["to"],
        )
    )


@none_safe
def _list_to_depends_on(src: list[dict]) -> list[DependsOn]:
    return [_dict_to_depends_on(i) for i in src]


@none_safe
def _dict_to_filter_by(src: dict) -> CatalogFilterBy:
    return CatalogFilterBy(label_type=src.get("labelType"))


@none_safe
def _list_to_validate_by(validate_by: list[dict]) -> list[CatalogValidateByItem]:
    return [
        CatalogValidateByItem(
            id=i["id"],
            type=i["type"],
        )
        for i in validate_by
    ]


@dataclass
class LabelElementsExecutionRequest:
    """
    Information about the label elements execution request.
    """

    label: str
    """
    The label to get the elements for.
    """

    offset: Optional[int]
    """
    The number of elements to skip before returning.
    """

    limit: Optional[int]
    """
    The maximum number of elements to return.
    """

    exclude_primary_label: Optional[bool]
    """
    Excludes items from the result that differ only by primary label

    * false - return items with distinct primary label
    * true - return items with distinct requested label
    """

    exact_filter: Optional[list[str]]
    """
    Exact values to filter the elements by.
    """

    pattern_filter: Optional[str]
    """
    Filter the elements by a pattern. The pattern is matched against the element values in a case-insensitive way.
    """

    complement_filter: Optional[bool]
    """
    Whether to invert the effects of exact_filter amd pattern_filter.
    """

    depends_on: Optional[list[DependsOn]]
    """
    Other labels or date filters that should be used to limit the elements.
    """

    filter_by: Optional[CatalogFilterBy]
    """
    Which label is used for filtering - primary or requested.
    If omitted the server will use the default value of "REQUESTED".
    """

    validate_by: Optional[list[CatalogValidateByItem]]
    """
    Other metrics, attributes, labels or facts used to validate the elements.
    """

    @staticmethod
    @none_safe
    def from_dict(d: dict) -> "LabelElementsExecutionRequest":
        """
        Create LabelElementsExecutionRequest from a dictionary.
        :param d: the dictionary to parse
        """
        return LabelElementsExecutionRequest(
            label=d["label"],
            offset=d.get("offset"),
            limit=d.get("limit"),
            exclude_primary_label=d.get("excludePrimaryLabel"),
            exact_filter=d.get("exactFilter"),
            pattern_filter=d.get("patternFilter"),
            complement_filter=d.get("complementFilter"),
            depends_on=_list_to_depends_on(d.get("dependsOn")),
            filter_by=_dict_to_filter_by(d.get("filterBy")),
            validate_by=_list_to_validate_by(d.get("validateBy")),
        )


def _dict_to_filter(d: dict) -> ExecutionContextFilter:
    filter_type = d.get("filterType")
    if filter_type == "positiveAttributeFilter":
        return ExecutionContextPositiveAttributeFilter(label_identifier=d["labelIdentifier"], values=d["values"])

    if filter_type == "negativeAttributeFilter":
        return ExecutionContextNegativeAttributeFilter(label_identifier=d["labelIdentifier"], values=d["values"])

    if filter_type == "relativeDateFilter":
        return ExecutionContextRelativeDateFilter(
            dataset_identifier=d["datasetIdentifier"],
            granularity=d["granularity"],
            from_shift=d["from"],
            to_shift=d["to"],
        )

    if filter_type == "absoluteDateFilter":
        return ExecutionContextAbsoluteDateFilter(
            dataset_identifier=d["datasetIdentifier"], from_date=d["from"], to_date=d["to"]
        )

    raise ValueError(f"Unsupported filter definition type: {d}")


def _dict_to_filters(filters: list[dict]) -> list[ExecutionContextFilter]:
    return [_dict_to_filter(f) for f in filters]


def _dict_to_attributes(attributes: list[dict]) -> list[ExecutionContextAttribute]:
    return [
        ExecutionContextAttribute(
            attribute_title=i["attributeTitle"],
            attribute_identifier=i["attributeIdentifier"],
            label_title=i["labelTitle"],
            label_identifier=i["labelIdentifier"],
            date_granularity=i.get("dateGranularity"),
            sorting=i.get("sorting"),
        )
        for i in attributes
    ]


@dataclass
class ExecutionContext:
    """
    Execution context of the FlexConnect function
    """

    execution_type: ExecutionType
    """
    Type of the execution.
    """

    organization_id: str
    """
    The ID of the organization that the FlexConnect function is executed in.
    """

    workspace_id: str
    """
    The ID of the workspace that the FlexConnect function is executed in.
    """

    user_id: str
    """
    The ID of the user that invoked the FlexConnect function.
    """

    timestamp: Optional[str]
    """
    The timestamp of the execution used as "now" in date filters.
    For example 2020-06-03T10:15:30+01:00.
    """

    timezone: Optional[str]
    """
    The timezone of the execution.
    """

    week_start: Optional[str]
    """
    The start of the week. Either "monday" or "sunday".
    """

    attributes: list[ExecutionContextAttribute]
    """
    All the attributes that are part of the execution request.
    """

    filters: list[ExecutionContextFilter]
    """
    All the attribute and date filters that are part of the execution request.
    """

    report_execution_request: Optional[ReportExecutionRequest]
    """
    The report execution request that the FlexConnect function should process.
    Only present if the execution type is "REPORT".
    """

    label_elements_execution_request: Optional[LabelElementsExecutionRequest]
    """
    The label elements execution request that the FlexConnect function should process.
    Only present if the execution type is "LABEL_ELEMENTS".
    """

    @staticmethod
    @none_safe
    def from_dict(d: dict) -> "ExecutionContext":
        """
        Create ExecutionContext from a dictionary.
        :param d: the dictionary to parse
        """
        return ExecutionContext(
            execution_type=ExecutionType[d["executionType"]],
            organization_id=d["organizationId"],
            workspace_id=d["workspaceId"],
            user_id=d["userId"],
            timestamp=d.get("timestamp"),
            timezone=d.get("timezone"),
            week_start=d.get("weekStart"),
            report_execution_request=ReportExecutionRequest.from_dict(d.get("reportExecutionRequest")),
            label_elements_execution_request=LabelElementsExecutionRequest.from_dict(
                d.get("labelElementsExecutionRequest")
            ),
            attributes=_dict_to_attributes(d.get("attributes", [])),
            filters=_dict_to_filters(d.get("filters", [])),
        )

    @staticmethod
    def from_parameters(parameters: dict) -> Optional["ExecutionContext"]:
        """
        Create ExecutionContext from FlexConnect function parameters.

        :param parameters: the parameters dictionary of the FlexConnect function invocation
        :return: None if the parameters do not contain the execution context, otherwise the execution context
        """
        return ExecutionContext.from_dict(parameters["executionContext"]) if "executionContext" in parameters else None
