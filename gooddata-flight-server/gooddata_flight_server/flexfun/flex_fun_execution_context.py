# (C) 2024 GoodData Corporation
from dataclasses import dataclass
from typing import Optional

from gooddata_sdk import Attribute, ComputeToSdkConverter, Filter, Metric


@dataclass
class ExecutionRequest:
    """
    Information about the execution request that is sent to the FlexFun.
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
            attributes=[ComputeToSdkConverter.convert_attribute(a) for a in d.get("attributes", [])],
            metrics=[ComputeToSdkConverter.convert_metric(m) for m in d.get("measures", [])],
            filters=[ComputeToSdkConverter.convert_filter(f) for f in d.get("filters", [])],
        )


@dataclass
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

    execution_request: ExecutionRequest
    """
    The execution request that the FlexFun should process.
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
            execution_request=ExecutionRequest.from_dict(d["execution_request"]),
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
