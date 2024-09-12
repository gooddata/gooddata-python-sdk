# (C) 2024 GoodData Corporation
import enum
from typing import Optional, Union

from attrs import define, field
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


def _dict_to_execution_context_attribute_sorting(d: Optional[dict]) -> Optional[ExecutionContextAttributeSorting]:
    if not d:
        return None
    return ExecutionContextAttributeSorting(
        sort_column=d["sort_column"],
        sort_direction=d["sort_direction"],
    )


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

    date_granularity: Optional[str]
    """
    Date granularity of the attribute if it is a date attribute.
    """

    sorting: Optional[ExecutionContextAttributeSorting] = field(converter=_dict_to_execution_context_attribute_sorting)
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
            attribute_title=d["attribute_title"],
            attribute_identifier=d["attribute_identifier"],
            label_title=d["label_title"],
            label_identifier=d["label_identifier"],
            date_granularity=d.get("date_granularity"),
            sorting=d.get("sorting"),
        )


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
    def from_dict(d: Optional[dict]) -> Optional["ReportExecutionRequest"]:
        """
        Create ReportExecutionRequest from a dictionary.
        :param d: the dictionary to parse
        """
        if not d:
            return None
        return ReportExecutionRequest(
            attributes=d.get("attributes", []),
            metrics=d.get("measures", []),
            filters=d.get("filters", []),
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


def _list_to_depends_on(src: Optional[list[dict]]) -> Optional[list[DependsOn]]:
    if not src:
        return None
    return [_dict_to_depends_on(i) for i in src]


def _list_to_filter_by(src: Optional[dict]) -> Optional[CatalogFilterBy]:
    if not src:
        return None
    return CatalogFilterBy(label_type=src.get("filterBy", "REQUESTED"))


def _list_to_validate_by(validate_by: Optional[list[dict]]) -> list[CatalogValidateByItem]:
    if not validate_by:
        return []
    return [
        CatalogValidateByItem(
            id=i["id"],
            type=i["type"],
        )
        for i in validate_by
    ]


@define
class LabelElementsExecutionRequest:
    """
    Information about the label elements execution request.
    """

    label: str
    """
    The label to get the elements for.
    """

    depends_on: Optional[list[DependsOn]] = field(converter=_list_to_depends_on)
    """
    Other labels or date filters that should be used to limit the elements.
    """

    filter_by: Optional[CatalogFilterBy] = field(converter=_list_to_filter_by)
    """
    Which label is used for filtering - primary or requested.
    If omitted the server will use the default value of "REQUESTED".
    """

    validate_by: Optional[list[CatalogValidateByItem]] = field(converter=_list_to_validate_by)
    """
    Other metrics, attributes, labels or facts used to validate the elements.
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

    exact_filter: Optional[list[str]] = None
    """
    Exact values to filter the elements by.
    """

    pattern_filter: Optional[str] = None
    """
    Filter the elements by a pattern. The pattern is matched against the element values in a case-insensitive way.
    """

    complement_filter: Optional[bool] = None
    """
    Whether to invert the effects of exact_filter amd pattern_filter.
    """

    @staticmethod
    def from_dict(d: Optional[dict]) -> Optional["LabelElementsExecutionRequest"]:
        """
        Create LabelElementsExecutionRequest from a dictionary.
        :param d: the dictionary to parse
        """
        if not d:
            return None
        return LabelElementsExecutionRequest(
            label=d["label"],
            depends_on=d.get("dependsOn"),
            filter_by=d.get("filterBy"),
            validate_by=d.get("validateBy"),
            offset=d.get("offset"),
            limit=d.get("limit"),
            exclude_primary_label=d.get("excludePrimaryLabel"),
            exact_filter=d.get("exactFilter"),
            pattern_filter=d.get("patternFilter"),
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


def _dict_to_attributes(attributes: list[dict]) -> list[ExecutionContextAttribute]:
    return [
        ExecutionContextAttribute(
            attribute_title=i["attribute_title"],
            attribute_identifier=i["attribute_identifier"],
            label_title=i["label_title"],
            label_identifier=i["label_identifier"],
            date_granularity=i.get("date_granularity"),
            sorting=i.get("sorting"),
        )
        for i in attributes
    ]


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

    attributes: list[ExecutionContextAttribute] = field(converter=_dict_to_attributes)
    """
    All the attributes that are part of the execution request.
    """

    filters: list[ExecutionContextFilter] = field(converter=_dict_to_filters)
    """
    All the attribute and date filters that are part of the execution request.
    """

    report_execution_request: Optional[ReportExecutionRequest] = None
    """
    The report execution request that the FlexFun should process.
    Only present if the execution type is "REPORT".
    """

    label_elements_execution_request: Optional[LabelElementsExecutionRequest] = None
    """
    The label elements execution request that the FlexFun should process.
    Only present if the execution type is "LABEL_ELEMENTS".
    """

    @staticmethod
    def from_dict(d: dict) -> Optional["ExecutionContext"]:
        """
        Create ExecutionContext from a dictionary.
        :param d: the dictionary to parse
        """
        if not d:
            return None

        return ExecutionContext(
            execution_type=ExecutionType[d["execution_type"]],
            organization_id=d["organization_id"],
            workspace_id=d["workspace_id"],
            user_id=d["user_id"],
            timestamp=d.get("timestamp"),
            timezone=d.get("timezone"),
            week_start=d.get("week_start"),
            execution_request=ExecutionRequest.from_dict(d["execution_request"]),
            report_execution_request=ReportExecutionRequest.from_dict(d.get("report_execution_request")),
            label_elements_execution_request=LabelElementsExecutionRequest.from_dict(
                d.get("label_elements_execution_request")
            ),
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
