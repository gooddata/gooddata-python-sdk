#  (C) 2024 GoodData Corporation

import pyarrow
from gooddata_flexfun.flex_fun import FlexFun
from gooddata_flight_server.server.base import ServerContext
from gooddata_flight_server.tasks.base import ArrowData


class Fun1(FlexFun):
    Name = "fun1"
    Schema = pyarrow.schema(fields=[pyarrow.field("col", pyarrow.int64())])

    def call(
        self,
        parameters: dict,
        columns: tuple[str, ...],
        headers: dict[str, list[str]],
    ) -> ArrowData:
        pass


class Fun2(FlexFun):
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
