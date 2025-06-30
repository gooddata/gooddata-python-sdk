#  (C) 2024 GoodData Corporation

import pyarrow
from gooddata_flexconnect.function.function import FlexConnectFunction
from gooddata_flight_server import ArrowData, ServerContext


class Fun1(FlexConnectFunction):
    Name = "fun1"
    Schema = pyarrow.schema(fields=[pyarrow.field("col", pyarrow.int64())])

    def call(
        self,
        parameters: dict,
        columns: tuple[str, ...],
        headers: dict[str, list[str]],
    ) -> ArrowData:
        pass


class Fun2(FlexConnectFunction):
    Name = "fun2"
    Schema = pyarrow.schema(fields=[pyarrow.field("col", pyarrow.string())])

    OnLoadCalled = False

    def call(
        self,
        parameters: dict,
        columns: tuple[str, ...],
        headers: dict[str, list[str]],
    ) -> ArrowData:
        pass

    @staticmethod
    def on_load(ctx: ServerContext):
        Fun2.OnLoadCalled = True
