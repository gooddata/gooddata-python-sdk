#  (C) 2024 GoodData Corporation
import dataclasses
from dataclasses import dataclass
from typing import Callable, Optional

import pyarrow.flight

from gooddata_flight_server.errors.error_info import ErrorInfo


@dataclass(frozen=True)
class TaskError:
    """
    Detail about failed task execution. The original Exception that was raised and
    failed the task is intentionally _not_ stored here.

    That is because by storing the exception and the included traceback, the code
    would also hold onto stack frames and all local variables bound to them - which
    can in return hold onto _a lot_ of memory.

    See: https://cosmicpercolator.com/2016/01/13/exception-leaks-in-python-2-and-3/
    See also: https://github.com/apache/arrow/issues/36540

    Also note, that clearing the traceback as hinted in above article helps somewhat
    but is not ideal when working with FlightErrors. While testing and measuring, I
    have found that even a freshly constructed FlightError (for example a freshly constructed
    copy of the original exception's message + extra_info) has some non-trivial overhead.
    Unsure why is that, and I'm not going to spend more time to investigate :)

    Therefore, I have converged to this approach where the task error contains a
    ErrorInfo (all essential detail) and a factory function to create the
    actual FlightError.

    The code that is supposed to raise the actual exception to the client will
    instantiate the exception when needed.
    """

    error_info: ErrorInfo
    error_factory: Callable[[str, Optional[bytes]], pyarrow.flight.FlightError]

    client_error: bool = False
    """
    indicates whether the task failed because client provided invalid input.

    this will be used purely for logging / tracking purposes. e.g. tasks failed due to client
    providing bad input are logged as info and the task executor does not bump error counter
    metrics
    """

    def as_flight_error(self) -> pyarrow.flight.FlightError:
        """
        :return: new instance of FlightError that should be raised
        """
        return self.error_info.to_flight_error(self.error_factory)

    def to_client_error(self) -> "TaskError":
        """
        :return: creates a copy of this instance with `client_error` indicator set to True
        """
        return dataclasses.replace(self, client_error=True)
