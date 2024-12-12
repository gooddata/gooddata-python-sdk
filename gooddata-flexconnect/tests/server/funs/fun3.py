#  (C) 2024 GoodData Corporation
import time
from typing import Optional

import pyarrow
from gooddata_flexconnect.function.function import FlexConnectFunction
from gooddata_flight_server import ArrowData

_DATA: Optional[pyarrow.Table] = None


class _LongRunningFun(FlexConnectFunction):
    Name = "LongRunningFun"
    Schema = pyarrow.schema(
        fields=[
            pyarrow.field("col1", pyarrow.int64()),
            pyarrow.field("col2", pyarrow.string()),
            pyarrow.field("col3", pyarrow.bool_()),
        ]
    )

    def call(
        self,
        parameters: dict,
        columns: tuple[str, ...],
        headers: dict[str, list[str]],
    ) -> ArrowData:
        # sleep is intentionally setup to be longer than the deadline for
        # the function invocation (see conftest.py // flexconnect_server fixture)
        time.sleep(1)

        return pyarrow.table(
            data={
                "col1": [1, 2, 3],
                "col2": ["a", "b", "c"],
                "col3": [True, False, True],
            },
            schema=self.Schema,
        )
