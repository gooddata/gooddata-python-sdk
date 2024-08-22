# (C) 2024 GoodData Corporation
from typing import Optional

from attrs import define, field
from gooddata_sdk import Attribute, ComputeToSdkConverter, Filter, Metric


def _dict_to_attributes(attributes: list[dict]) -> list[Attribute]:
    return [ComputeToSdkConverter.convert_attribute(a) for a in attributes]


def _dict_to_metrics(metrics: list[dict]) -> list[Metric]:
    return [ComputeToSdkConverter.convert_metric(m) for m in metrics]


def _dict_to_filters(filters: list[dict]) -> list[Filter]:
    return [ComputeToSdkConverter.convert_filter(f) for f in filters]


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
class ExecutionRequest:
    """
    Information about the execution request that is sent to the FlexFun.
    """

    attributes: list[Attribute] = field(converter=_dict_to_attributes)
    """
    All the attributes that are part of the execution request.
    """

    metrics: list[Metric] = field(converter=_dict_to_metrics)
    """
    All the metrics that are part of the execution request.
    """

    filters: list[Filter] = field(converter=_dict_to_filters)
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
class ExecutionContext:
    """
    Execution context of the FlexFun
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
    """

    attributes: list[ExecutionContextAttribute]
    """
    All the attributes that are part of the execution request.
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
            organization_id=d["organization_id"],
            workspace_id=d["workspace_id"],
            user_id=d["user_id"],
            timestamp=d.get("timestamp"),
            timezone=d.get("timezone"),
            week_start=d.get("week_start"),
            execution_request=ExecutionRequest.from_dict(d["execution_request"]),
            attributes=d.get("attributes", []),
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
