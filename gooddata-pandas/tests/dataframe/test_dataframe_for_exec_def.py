# (C) 2022 GoodData Corporation
from gooddata_pandas import DataFrameFactory
from gooddata_sdk import Attribute, ExecutionDefinition, ObjId, SimpleMetric, TotalDefinition, TotalDimension


def test_dataframe_for_exec_def_two_dim1(gdf: DataFrameFactory):
    exec_def = ExecutionDefinition(
        attributes=[
            Attribute(local_id="region", label="region"),
            Attribute(local_id="state", label="state"),
            Attribute(local_id="product_category", label="products.category"),
        ],
        metrics=[
            SimpleMetric(local_id="price", item=ObjId(id="price", type="fact")),
            SimpleMetric(local_id="order_amount", item=ObjId(id="order_amount", type="metric")),
        ],
        filters=[],
        dimensions=[["state", "region"], ["product_category", "measureGroup"]],
    )

    result = gdf.for_exec_def(exec_def=exec_def)
    print(str(result))


def test_dataframe_for_exec_def_two_dim2(gdf: DataFrameFactory):
    exec_def = ExecutionDefinition(
        attributes=[
            Attribute(local_id="region", label="region"),
            Attribute(local_id="state", label="state"),
            Attribute(local_id="product_category", label="products.category"),
        ],
        metrics=[
            SimpleMetric(local_id="price", item=ObjId(id="price", type="fact")),
            SimpleMetric(local_id="order_amount", item=ObjId(id="order_amount", type="metric")),
        ],
        filters=[],
        dimensions=[["region", "state", "product_category"], ["measureGroup"]],
    )

    result = gdf.for_exec_def(exec_def=exec_def)
    print(str(result))


def test_dataframe_for_exec_def_two_dim3(gdf: DataFrameFactory):
    exec_def = ExecutionDefinition(
        attributes=[
            Attribute(local_id="region", label="region"),
            Attribute(local_id="state", label="state"),
            Attribute(local_id="product_category", label="products.category"),
        ],
        metrics=[
            SimpleMetric(local_id="price", item=ObjId(id="price", type="fact")),
            SimpleMetric(local_id="order_amount", item=ObjId(id="order_amount", type="metric")),
        ],
        filters=[],
        dimensions=[["product_category"], ["region", "state", "measureGroup"]],
    )

    result = gdf.for_exec_def(exec_def=exec_def)
    print(str(result))


def test_dataframe_for_exec_def_totals1(gdf: DataFrameFactory):
    """
    Execution with column totals; the row dimension has single label
    """
    exec_def = ExecutionDefinition(
        attributes=[
            Attribute(local_id="region", label="region"),
            Attribute(local_id="state", label="state"),
            Attribute(local_id="product_category", label="products.category"),
        ],
        metrics=[
            SimpleMetric(local_id="price", item=ObjId(id="price", type="fact")),
            SimpleMetric(local_id="order_amount", item=ObjId(id="order_amount", type="metric")),
        ],
        filters=[],
        dimensions=[["product_category"], ["region", "state", "measureGroup"]],
        totals=[
            TotalDefinition(
                local_id="grand_total1",
                aggregation="sum",
                total_dims=[TotalDimension(idx=1, items=["region", "state", "measureGroup"])],
                metric_local_id="price",
            ),
            TotalDefinition(
                local_id="grand_total2",
                aggregation="max",
                total_dims=[TotalDimension(idx=1, items=["region", "state", "measureGroup"])],
                metric_local_id="order_amount",
            ),
        ],
    )

    result = gdf.for_exec_def(exec_def=exec_def)
    print(str(result))


def test_dataframe_for_exec_def_totals2(gdf: DataFrameFactory):
    """
    Execution with column totals; the row dimension has two labels; this exercises that the index is
    padded appropriately
    """
    exec_def = ExecutionDefinition(
        attributes=[
            Attribute(local_id="region", label="region"),
            Attribute(local_id="state", label="state"),
            Attribute(local_id="product_category", label="products.category"),
        ],
        metrics=[
            SimpleMetric(local_id="price", item=ObjId(id="price", type="fact")),
            SimpleMetric(local_id="order_amount", item=ObjId(id="order_amount", type="metric")),
        ],
        filters=[],
        dimensions=[["region", "product_category"], ["state", "measureGroup"]],
        totals=[
            TotalDefinition(
                local_id="grand_total1",
                aggregation="sum",
                total_dims=[TotalDimension(idx=1, items=["state", "measureGroup"])],
                metric_local_id="price",
            ),
            TotalDefinition(
                local_id="grand_total2",
                aggregation="max",
                total_dims=[TotalDimension(idx=1, items=["state", "measureGroup"])],
                metric_local_id="order_amount",
            ),
        ],
    )

    result = gdf.for_exec_def(exec_def=exec_def)
    print(str(result))


def test_dataframe_for_exec_def_totals3(gdf: DataFrameFactory):
    """
    Execution with row totals; the column dimension has single label.
    """
    exec_def = ExecutionDefinition(
        attributes=[
            Attribute(local_id="region", label="region"),
            Attribute(local_id="state", label="state"),
            Attribute(local_id="product_category", label="products.category"),
        ],
        metrics=[
            SimpleMetric(local_id="price", item=ObjId(id="price", type="fact")),
            SimpleMetric(local_id="order_amount", item=ObjId(id="order_amount", type="metric")),
        ],
        filters=[],
        dimensions=[["region", "state", "measureGroup"], ["product_category"]],
        totals=[
            TotalDefinition(
                local_id="grand_total1",
                aggregation="sum",
                total_dims=[TotalDimension(idx=0, items=["region", "state", "measureGroup"])],
                metric_local_id="price",
            ),
            TotalDefinition(
                local_id="grand_total2",
                aggregation="max",
                total_dims=[TotalDimension(idx=0, items=["region", "state", "measureGroup"])],
                metric_local_id="order_amount",
            ),
        ],
    )

    result = gdf.for_exec_def(exec_def=exec_def)
    print(str(result))


def test_dataframe_for_exec_def_totals4(gdf: DataFrameFactory):
    """
    Execution with row totals; the column dimension has two label; this
    """
    exec_def = ExecutionDefinition(
        attributes=[
            Attribute(local_id="region", label="region"),
            Attribute(local_id="state", label="state"),
            Attribute(local_id="product_category", label="products.category"),
        ],
        metrics=[
            SimpleMetric(local_id="price", item=ObjId(id="price", type="fact")),
            SimpleMetric(local_id="order_amount", item=ObjId(id="order_amount", type="metric")),
        ],
        filters=[],
        dimensions=[["state", "measureGroup"], ["region", "product_category"]],
        totals=[
            TotalDefinition(
                local_id="grand_total1",
                aggregation="sum",
                total_dims=[TotalDimension(idx=0, items=["state", "measureGroup"])],
                metric_local_id="price",
            ),
            TotalDefinition(
                local_id="grand_total2",
                aggregation="max",
                total_dims=[TotalDimension(idx=0, items=["state", "measureGroup"])],
                metric_local_id="order_amount",
            ),
        ],
    )

    result = gdf.for_exec_def(exec_def=exec_def)
    print(str(result))


def test_dataframe_for_exec_def_one_dim1(gdf: DataFrameFactory):
    exec_def = ExecutionDefinition(
        attributes=[
            Attribute(local_id="region", label="region"),
            Attribute(local_id="state", label="state"),
            Attribute(local_id="product_category", label="products.category"),
        ],
        metrics=[
            SimpleMetric(local_id="price", item=ObjId(id="price", type="fact")),
            SimpleMetric(local_id="order_amount", item=ObjId(id="order_amount", type="metric")),
        ],
        filters=[],
        dimensions=[["region", "state", "product_category", "measureGroup"]],
    )

    result = gdf.for_exec_def(exec_def=exec_def)
    print(str(result))


def test_dataframe_for_exec_def_one_dim2(gdf: DataFrameFactory):
    exec_def = ExecutionDefinition(
        attributes=[
            Attribute(local_id="region", label="region"),
            Attribute(local_id="state", label="state"),
            Attribute(local_id="product_category", label="products.category"),
        ],
        metrics=[
            SimpleMetric(local_id="price", item=ObjId(id="price", type="fact")),
            SimpleMetric(local_id="order_amount", item=ObjId(id="order_amount", type="metric")),
        ],
        filters=[],
        dimensions=[[], ["region", "state", "product_category", "measureGroup"]],
    )

    result = gdf.for_exec_def(exec_def=exec_def)
    print(str(result))
