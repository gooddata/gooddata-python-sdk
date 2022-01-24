.. (C) 2022 GoodData Corporation

.. _index_root:

Welcome to GoodData SDK's documentation!
****************************************

GoodData Python SDK
===================

The ``gooddata-sdk`` package aims to provide clean and convenient Python APIs to interact with GoodData.CN.

At the moment the SDK provides services to inspect and interact with the Semantic Model and consume analytics.

Services
--------

All the services are accessible by class ``gooddata_sdk.GoodDataSdk``. The class forms entry-point to the sdk. All other
examples expect user has access to initialized GoodDataSdk instance.

Here is an example how to create an instance of GoodDataSdk:

.. code-block:: python

    import gooddata_sdk

    # GoodData.CN host in the form of uri eg. "http://localhost:3000"
    host = "http://localhost:3000"
    # GoodData.CN user token
    token = "some_user_token"
    sdk = gooddata_sdk.GoodDataSdk.create(host, token)

Catalog Service
^^^^^^^^^^^^^^^

Catalog service provides an ability to list catalog objects of given workspace. It contains all the datasets and
metrics registered there.

.. code-block:: python

    workspace_id = "demo"

    # read catalog for demo workspace
    catalog = sdk.catalog.get_full_catalog(workspace_id)

    # print all dataset in the workspace
    for dataset in catalog.datasets:
        print(str(dataset))

    # print all metrics in the workspace
    for metric in catalog.metrics:
        print(str(metric))

Insights Service
^^^^^^^^^^^^^^^^

A service which gives access to Insights stored in workspace. It can retrieve all the insights from workspace or one
insight based on its name. Insight instance is the input for other services like a `Table service`_

.. code-block:: python

    workspace_id = "demo"

    # reads insights from workspace
    insights = sdk.insights.get_insights(workspace_id)
    # print all fetched insights
    for insight in insights:
        print(str(insight))

Compute Service
^^^^^^^^^^^^^^^

Compute service drives computation of analytics for a GoodData.CN workspaces. The prescription of what to compute
is encapsulated by the ExecutionDefinition which consists of attributes, metrics, filters and definition of
dimensions that influence how to organize the data in the result.

Higher level services like `Table service`_ use Compute service to execute computation in GoodData.CN.
Higher level service is also responsible for results presentation to the user e.g. in tabular form.


Table Service
^^^^^^^^^^^^^

A convenience service that allows you to consume analytics in typical tabular format. The service allows free-form
computations and computations of data for GoodData.CN Insights.

For instance behold how it is possible to get tabular data for an insight defined on your GD.CN server:

.. code-block:: python

    workspace_id = "demo"
    insight_id = "some_insight_id_in_demo_workspace"

    # reads insight from workspace
    insight = sdk.insights.get_insight(workspace_id, insight_id)

    # triggers computation for the insight. the result will be returned in a tabular form
    table = sdk.tables.for_insight(workspace_id, insight)

    # and this is how you can read data row-by-row and do something with it
    for row in table.read_all():
        print(row)

.. _index_api:

API documentation
-----------------
Check out the :doc:`api` section for further information.

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
