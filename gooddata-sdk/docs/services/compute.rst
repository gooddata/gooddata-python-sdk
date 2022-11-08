Compute Service
===============

The ``gooddata_sdk.compute`` service drives computation of analytics for GoodData.CN workspaces. The prescription of what to compute
is encapsulated by the ExecutionDefinition which consists of attributes, metrics, filters and definition of
dimensions that influence how to organize the data in the result.

Higher level services like Table service use Compute service to execute computation in GoodData.CN.
Higher level service is also responsible for results presentation to the user e.g. in tabular form.

Entity methods
**************

The *gooddata_sdk.compute* supports the following entity API calls:

* ``for_exec_def(workspace_id: str, exec_def: ExecutionDefinition)``

    Returns *Execution*.

    Starts computation in GoodData.CN workspace, using the provided execution definition.

* ``retrieve_result_cache_metadata(workspace_id: str, result_id: str)``

    Returns *ResultCacheMetadata*.

    Gets execution result's metadata from GoodData.CN workspace for given execution result ID.
