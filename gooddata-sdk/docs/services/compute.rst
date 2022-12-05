Compute Service
===============

The ``gooddata_sdk.compute`` service drives computation of analytics for GoodData.CN workspaces. The prescription of what to compute
is encapsulated by the ExecutionDefinition which consists of attributes, metrics, filters and definition of
dimensions that influence how to organize the data in the result.

Higher level services like Table service use Compute service to execute computation in GoodData.CN.
Higher level service is also responsible for results presentation to the user e.g. in tabular form.


The *gooddata_sdk.compute* supports the following entity API calls:

* ``for_exec_def(workspace_id: str, exec_def: ExecutionDefinition)``

    Returns *Execution*.

    Starts computation in GoodData.CN workspace, using the provided execution definition.

    Example:
.. code-block:: python

    from gooddata_sdk import GoodDataSdk, ExecutionDefinition, Attribute, SimpleMetric, ObjId

    sdk = GoodDataSdk.create(host, token)
    workspace_id = "demo"

    exec_def = ExecutionDefinition(
        attributes=[
            Attribute(local_id="region", label="region"),
            Attribute(local_id="product_category", label="products.category"),
            Attribute(local_id="state", label="state"),
        ],
        metrics=[
            SimpleMetric(local_id="price", item=ObjId(id="price", type="fact")),
            SimpleMetric(local_id="order_amount", item=ObjId(id="order_amount", type="metric")),
        ],
        filters=[],
        dimensions=[["region", "state"], ["product_category", "measureGroup"]],
    )
    execution = sdk.compute.for_exec_def(workspace_id, exec_def)

    # currently there is no dedicated service for exporting *Execution* results into XLSX/CSV, however it's possible to run it this way:

    from gooddata_api_client.model.tabular_export_request import TabularExportRequest

    filename = "export.xlsx"
    export_request = sdk.client.actions_api.create_tabular_export(
        workspace_id,
        TabularExportRequest(
            execution_result=execution.result_id,
            file_name=filename,
            format="XLSX",
        )
    )

    while response := sdk.client.actions_api.get_tabular_export(workspace_id, export_request.export_result, _preload_content=False):
        if (response.status == 202):
            time.sleep(2)
            continue
        elif (response.status == 200):
            with open(filename, 'wb') as out_file:
                out_file.write(response.data)
                break


* ``retrieve_result_cache_metadata(workspace_id: str, result_id: str)``

    Returns *ResultCacheMetadata*.

    Gets execution result's metadata from GoodData.CN workspace for given execution result ID.
