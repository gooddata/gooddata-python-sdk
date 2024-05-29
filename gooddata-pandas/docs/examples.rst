
Examples
********

Here are a couple of introductory examples how to create indexed and not-indexed series and data frames:

Series
======

.. code-block:: python

    from gooddata_pandas import GoodPandas

    # GoodData.CN host in the form of uri eg. "http://localhost:3000"
    host = "http://localhost:3000"
    # GoodData.CN user token
    token = "some_user_token"
    # initialize the adapter to work on top of GD.CN host and use the provided authentication token
    gp = GoodPandas(host, token)

    workspace_id = "demo"
    series = gp.series(workspace_id)

    # create indexed series
    indexed_series = series.indexed(index_by="label/label_id", data_by="fact/measure_id")

    # create non-indexed series containing just the values of measure sliced by elements of the label
    non_indexed = series.not_indexed(data_by="fact/measure_id", granularity="label/label_id")

Data Frames
===========

.. code-block:: python

    from gooddata_pandas import GoodPandas

    # GoodData.CN host in the form of uri eg. "http://localhost:3000"
    host = "http://localhost:3000"
    # GoodData.CN user token
    token = "some_user_token"
    # initialize the adapter to work on top of GD.CN host and use the provided authentication token
    gp = GoodPandas(host, token)

    workspace_id = "demo"
    frames = gp.data_frames(workspace_id)

    # create indexed data frame
    indexed_df = frames.indexed(
        index_by="label/label_id",
        columns=dict(
            first_label='label/first_label_id',
            second_label='label/second_label_id',
            first_metric='metric/first_metric_id',
            second_metric='fact/fact_id'
        )
    )

    # create data frame with hierarchical index
    indexed_df = frames.indexed(
        index_by=dict(first_label='label/first_label_id', second_label='label/second_label_id'),
        columns=dict(first_metric='metric/first_metric_id', second_metric='fact/fact_id')
    )

    # create non-indexed data frame
    non_indexed_df = frames.not_indexed(
        columns=dict(
            first_label='label/first_label_id',
            second_label='label/second_label_id',
            first_metric='metric/first_metric_id',
            second_metric='fact/fact_id'
        )
    )

    # create data frame based on the contents of the visualization. if the visualization contains labels and
    #  measures, the data frame will contain index or hierarchical index.
    visualization_df = frames.for_visualization('visualization_id')

    # create data frame based on the content of the items dict. if the dict contains both labels
    # and measures, the frame will contain index or hierarchical index.
    df = frames.for_items(
        items=dict(
            first_label='label/first_label_id',
            second_label='label/second_label_id',
            first_metric='metric/first_metric_id',
            second_metric='fact/fact_id'
        )
    )

    # create data frame from custom execution definition
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
        dimensions=[
            TableDimension(item_ids=["state", "region"]),
            TableDimension(item_ids=["product_category", "measureGroup"]),
        ],
    )
    df, df_metadata = frames.for_exec_def(exec_def=exec_def)

    # use result ID from computation above and generate dataframe just from it
    df_from_result_id, df_metadata_from_result_id = frames.for_exec_result_id(
        result_id=df_metadata.execution_response.result_id,
    )
