# (C) 2024 GoodData Corporation
import enum
from typing import Optional, Union

from attrs import define, field
from gooddata_sdk import (
    Attribute,
    CatalogDependsOn,
    CatalogDependsOnDateFilter,
    CatalogFilterBy,
    CatalogValidateByItem,
    ComputeToSdkConverter,
    Filter,
    Metric,
)
from typing_extensions import TypeAlias


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


@define
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


@define
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

    date_granularity: str
    """
    Date granularity of the attribute if it is a date attribute.
    """

    sorting: Optional[ExecutionContextAttributeSorting]
    """
    Sorting of the attribute. If not present, the attribute is not sorted.
    """


@define
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


@define
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


@define
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


@define
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


@define
class ExecutionRequest:
    """
    Information about the execution request that is sent to the FlexFun.
    DEPRECATED: Use ReportExecutionRequest instead.
    """

    attributes: list[Attribute] = field(converter=_dict_to_request_attributes)
    """
    All the attributes that are part of the execution request.
    """

    metrics: list[Metric] = field(converter=_dict_to_request_metrics)
    """
    All the metrics that are part of the execution request.
    """

    filters: list[Filter] = field(converter=_dict_to_request_filters)
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
            attributes=d.get("attributes", []),
            metrics=d.get("measures", []),
            filters=d.get("filters", []),
        )


@define
class ReportExecutionRequest:
    """
    Information about the report execution request.
    """

    attributes: list[Attribute] = field(converter=_dict_to_request_attributes)
    """
    All the attributes that are part of the execution request.
    """

    metrics: list[Metric] = field(converter=_dict_to_request_metrics)
    """
    All the metrics that are part of the execution request.
    """

    filters: list[Filter] = field(converter=_dict_to_request_filters)
    """
    All the filters that are part of the execution request.
    """

    @staticmethod
    def from_dict(d: dict) -> "ReportExecutionRequest":
        """
        Create ReportExecutionRequest from a dictionary.
        :param d: the dictionary to parse
        """
        return ReportExecutionRequest(
            attributes=d.get("attributes", []),
            metrics=d.get("measures", []),
            filters=d.get("filters", []),
        )


@define
class LabelElementsExecutionRequest:
    """
    Information about the label elements execution request.
    """

    label: str
    """
    The label to get the elements for.
    """

    offset: Optional[int] = None
    """
    The offset of the elements.
    """

    limit: Optional[int] = None
    """
    The limit of the elements.
    """

    exclude_primary_label: Optional[bool] = None
    """
    Whether to exclude primary label from the result.
    """

    depends_on: Optional[list[Union[CatalogDependsOn, CatalogDependsOnDateFilter]]] = None
    """
    Other labels or date filters that should be used to limit the elements.
    """

    validate_by: Optional[list[CatalogValidateByItem]] = None
    """
    Other metrics, attributes, labels or facts used to validate the elements.
    """

    exact_filter: Optional[list[str]] = None
    """
    Exact values to filter the elements by.
    """

    pattern_filter: Optional[str] = None
    """
    Filter the elements by a pattern. The pattern is matched against the element values in a case-insensitive way.
    """

    filter_by: Optional[CatalogFilterBy] = None
    """
    Which label is used for filtering - primary or requested.
    If omitted the server will use the default value of "REQUESTED".
    """

    complement_filter: Optional[bool] = None
    """
    Whether to invert the effects of exact_filter amd pattern_filter.
    """

    @staticmethod
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
            depends_on=d.get("dependsOn"),
            validate_by=d.get("validateBy"),
            exact_filter=d.get("exactFilter"),
            pattern_filter=d.get("patternFilter"),
            filter_by=d.get("filterBy"),
            complement_filter=d.get("complementFilter"),
        )


def _dict_to_filter(d: dict) -> ExecutionContextFilter:
    filter_type = d.get("filter_type")
    if filter_type == "positiveAttributeFilter":
        return ExecutionContextPositiveAttributeFilter(label_identifier=d["label_identifier"], values=d["values"])

    if filter_type == "negativeAttributeFilter":
        return ExecutionContextNegativeAttributeFilter(label_identifier=d["label_identifier"], values=d["values"])

    if filter_type == "relativeDateFilter":
        return ExecutionContextRelativeDateFilter(
            dataset_identifier=d["dataset_identifier"],
            granularity=d["granularity"],
            from_shift=d["from"],
            to_shift=d["to"],
        )

    if filter_type == "absoluteDateFilter":
        return ExecutionContextAbsoluteDateFilter(
            dataset_identifier=d["dataset_identifier"], from_date=d["from"], to_date=d["to"]
        )

    raise ValueError(f"Unsupported filter definition type: {d}")


def _dict_to_filters(filters: list[dict]) -> list[ExecutionContextFilter]:
    return [_dict_to_filter(f) for f in filters]


@define
class ExecutionContext:
    """
    Execution context of the FlexFun
    """

    execution_type: ExecutionType
    """
    Type of the execution.
    """

    organization_id: str
    """
    The ID of the organization that the FlexFun is executed in.
    """

    workspace_id: str
    """
    The ID of the workspace that the FlexFun is executed in.
    """

    user_id: str
    """
    The ID of the user that invoked the FlexFun.
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

    execution_request: ExecutionRequest
    """
    The execution request that the FlexFun should process.
    DEPRECATED: Use ReportExecutionRequest or LabelElementsExecutionRequest instead.
    """

    report_execution_request: Optional[ReportExecutionRequest]
    """
    The report execution request that the FlexFun should process.
    Only present if the execution type is "REPORT".
    """

    label_elements_execution_request: Optional[LabelElementsExecutionRequest]
    """
    The label elements execution request that the FlexFun should process.
    Only present if the execution type is "LABEL_ELEMENTS".
    """

    attributes: list[ExecutionContextAttribute]
    """
    All the attributes that are part of the execution request.
    """

    filters: list[ExecutionContextFilter] = field(converter=_dict_to_filters)
    """
    All the attribute and date filters that are part of the execution request.
    """

    @staticmethod
    def from_dict(d: dict) -> Optional["ExecutionContext"]:
        """
        Create ExecutionContext from a dictionary.
        :param d: the dictionary to parse
        """
        if not d:
            return None

        report_execution_request_raw = d.get("report_execution_request")
        label_elements_execution_request_raw = d.get("label_elements_execution_request")

        return ExecutionContext(
            execution_type=ExecutionType(d["execution_type"]),
            organization_id=d["organization_id"],
            workspace_id=d["workspace_id"],
            user_id=d["user_id"],
            timestamp=d.get("timestamp"),
            timezone=d.get("timezone"),
            week_start=d.get("week_start"),
            execution_request=ExecutionRequest.from_dict(d["execution_request"]),
            report_execution_request=ReportExecutionRequest.from_dict(report_execution_request_raw)
            if report_execution_request_raw
            else None,
            label_elements_execution_request=LabelElementsExecutionRequest.from_dict(
                label_elements_execution_request_raw
            )
            if label_elements_execution_request_raw
            else None,
            attributes=d.get("attributes", []),
            filters=d.get("filters", []),
        )

    @staticmethod
    def from_parameters(parameters: dict) -> Optional["ExecutionContext"]:
        """
        Create ExecutionContext from FlexFun parameters.
        :param parameters: the parameters dictionary of the FlexFun invocation
        :return: None if the parameters do not contain the execution context, otherwise the execution context
        """
        return (
            ExecutionContext.from_dict(parameters["execution_context"]) if "execution_context" in parameters else None
        )
