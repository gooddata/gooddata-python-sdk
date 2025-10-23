#  (C) 2024 GoodData Corporation
from typing import Optional

import pyarrow
from gooddata_flexconnect.function.function import FlexConnectFunction
from gooddata_flight_server import ArrowData, ServerContext

_DATA: Optional[pyarrow.Table] = None


class _SimpleFun2(FlexConnectFunction):
    Name = "SimpleFun2"
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
        assert _DATA is not None
        return _DATA

    @staticmethod
    def on_load(ctx: ServerContext) -> None:
        # on load emulates some kid of one-off setup
        global _DATA
        _DATA = pyarrow.table(
            data={
                "col1": [1, 2, 3],
                "col2": ["a", "b", "c"],
                "col3": [True, False, True],
            },
            schema=_SimpleFun2.Schema,
        )
