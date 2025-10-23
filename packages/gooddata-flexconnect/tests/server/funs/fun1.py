#  (C) 2024 GoodData Corporation

import pyarrow
from gooddata_flexconnect.function.function import FlexConnectFunction
from gooddata_flight_server import ArrowData


class _SimpleFun1(FlexConnectFunction):
    Name = "SimpleFun1"
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
        return pyarrow.table(
            data={
                "col1": [1, 2, 3],
                "col2": ["a", "b", "c"],
                "col3": [True, False, True],
            },
            schema=self.Schema,
        )
