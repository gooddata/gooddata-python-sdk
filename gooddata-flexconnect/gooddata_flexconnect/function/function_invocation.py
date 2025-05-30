#  (C) 2025 GoodData Corporation
from dataclasses import dataclass
from typing import Optional, Union

import orjson
import pyarrow.flight
from gooddata_flight_server import ErrorInfo


@dataclass(frozen=True)
class RetryInvocation:
    """
    Indicates that the getting the results of the given task should be retried.
    """

    task_id: str


@dataclass(frozen=True)
class CancelInvocation:
    """
    Indicates that the given task should be cancelled.
    """

    task_id: str


@dataclass(frozen=True)
class SubmitInvocation:
    """
    Indicates that the given task should be submitted for processing.
    """

    command: bytes
    """
    The raw command that was sent to the Flight Server.
    """

    function_name: str
    """
    The name of the FlexConnect function to invoke.
    """

    parameters: dict
    """
    Parameters to pass to the FlexConnect function.
    """

    columns: Optional[tuple[str, ...]]
    """
    Columns to get from the FlexConnect function result.
    This may be used for column trimming by the function: the function must return at least those columns.
    """


def extract_submit_invocation_from_descriptor(descriptor: pyarrow.flight.FlightDescriptor) -> SubmitInvocation:
    """
    Given a flight descriptor, extract the invocation information from it.
    Do not allow the polling-related variants.
    """
    try:
        payload = orjson.loads(descriptor.command)
    except Exception:
        raise ErrorInfo.bad_argument(
            "Incorrect FlexConnect function invocation. The invocation payload is not a valid JSON."
        )

    function_name = payload.get("functionName")
    if function_name is None or not len(function_name):
        raise ErrorInfo.bad_argument(
            "Incorrect FlexConnect function invocation. The invocation payload does not specify 'functionName'."
        )

    parameters = payload.get("parameters") or {}
    columns = parameters.get("columns")

    return SubmitInvocation(
        function_name=function_name, parameters=parameters, columns=columns, command=descriptor.command
    )


def extract_pollable_invocation_from_descriptor(
    descriptor: pyarrow.flight.FlightDescriptor,
) -> Union[RetryInvocation, CancelInvocation, SubmitInvocation]:
    """
    Given a flight descriptor, extract the invocation information from it.
    Allow also the polling-related variants.
    """
    if descriptor.command is None or not len(descriptor.command):
        raise ErrorInfo.bad_argument(
            "Incorrect FlexConnect function invocation. Flight descriptor must contain command "
            "with the invocation payload."
        )

    # we are in the polling-enabled realm: try parsing the retry and cancel descriptors first
    if descriptor.command.startswith(b"c:"):
        task_id = descriptor.command[2:].decode()
        return CancelInvocation(task_id)
    elif descriptor.command.startswith(b"r:"):
        task_id = descriptor.command[2:].decode()
        return RetryInvocation(task_id)

    return extract_submit_invocation_from_descriptor(descriptor)
