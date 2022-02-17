Services
********

All the services are accessible by class ``gooddata_sdk.GoodDataSdk``. The class forms an entry-point to the SDK. All other
examples assume you have an entry-point to the GoodDataSdk instance already initialized.

Example of how to create an instance of GoodDataSdk:

.. code-block:: python

    import gooddata_sdk

    # GoodData.CN host in the form of uri eg. "http://localhost:3000"
    host = "http://localhost:3000"
    # GoodData.CN user token
    token = "some_user_token"
    sdk = gooddata_sdk.GoodDataSdk.create(host, token)

Catalog Workspace Service
=========================

The ``gooddata_sdk.catalog_workspace`` service enables you to list, create, update and delete workspaces.

.. code-block:: python

    # list workspaces
    workspaces = sdk.catalog_workspace.list_workspaces()

    # create or update workspace
    sdk.catalog_workspace.create_or_update(workspace_obj)

    # get workspace
    workspace = sdk.catalog_workspace.get_workspace("demo")

    # delete workspace
    sdk.catalog_workspace.delete_workspace("demo")


Catalog Workspace Content Service
==================================

The ``gooddata_sdk.catalog_workspace_content`` service enables you to list catalog objects from a workspace. It contains all the datasets and
metrics registered in the workspace. Each dataset consists of attributes, their labels and facts.
There is also a special type of dataset - date dataset. It contains attribute(label) for each date granularity (year, month, ...).

Example of how to read all datasets and metrics in a workspace:

.. code-block:: python

    workspace_id = "demo"

    # read catalog for demo workspace
    catalog = sdk.catalog_workspace_content.get_full_catalog(workspace_id)

    # print all dataset in the workspace
    for dataset in catalog.datasets:
        print(str(dataset))

    # print all metrics in the workspace
    for metric in catalog.metrics:
        print(str(metric))

Catalog Data Source Service
==================================

The ``gooddata_sdk.catalog_data_source`` service enables you to manage data sources and list their tables.
Data source object represents your database, which you integrate with GoodData.CN.

Generally there are two way how to register data sources:

1. Default, works for all data source types.

   - You specify jdbc url, data source type and relevant credentials.

2. Custom per data source types.

   - You specify custom attributes relevant for your data source and data source type and url are set in background.

Example of how you can manipulate with data sources:

.. code-block:: python

    # create (or update) data source using general interface - can be used for any type of data source
    # if data source already exists, it is updated
    sdk.catalog_data_source.create_or_update_data_source(
        CatalogDataSource(
            id="test",
            name="Test2",
            url="jdbc:postgres://localhost:5432/demo",
            schema="demo",
            credentials=BasicCredentials(
                username="demouser",
                password="demopass",
            ),
            enable_caching=False,
            url_params=[("param", "value")]
        )
    )

    # use Postgres specific interface
    sdk.catalog_data_source.create_or_update_data_source(
        CatalogDataSourcePostgres(
            id="test",
            name="Test2",
            db_specific_attributes=PostgresAttributes(
                host="localhost", db_name="demo"
            ),
            schema="demo",
            credentials=BasicCredentials(
                username="demouser",
                password="demopass",
            ),
            enable_caching=False,
            url_params=[("param", "value")]
        )
    )

    # create Snowflake data source using specialized interface
    sdk.catalog_data_source.create_or_update_data_source(
        CatalogDataSourceSnowflake(
            id="test",
            name="Test2",
            db_specific_attributes=SnowflakeAttributes(
                account="mycompany", warehouse="MYWAREHOUSE", db_name="MYDATABASE"
            ),
            schema="demo",
            credentials=BasicCredentials(
                username="demouser",
                password="demopass",
            ),
            enable_caching=False,
            url_params=[("param", "value")]
        )
    )

    # BigQuery requires path to credentials file, where service account definition is stored
    sdk.catalog_data_source.create_or_update_data_source(
        CatalogDataSourceBigQuery(
            id="test",
            name="Test",
            db_specific_attributes=BigQueryAttributes(
                project_id="project_id"
            ),
            schema="demo",
            credentials=TokenCredentialsFromFile(
                file_path=Path("credentials") / "bigquery_service_account.json"
            ),
            enable_caching=True,
            cache_path=["cache_schema"],
            url_params=[("param", "value")]
        )
    )

    # Look for other CatalogDataSource classes to find your data source type
    #

    # list data sources
    data_sources = sdk.catalog_data_source.list_data_sources()

    # get single data source
    data_sources = sdk.catalog_data_source.get_entity_data_sources('ds_id')

    # delete data source
    sdk.catalog_data_source.delete_data_source(data_source_id='ds_id')

    # patch data source attribute(s)
    sdk.catalog_data_source.patch_data_source_attributes(data_source_id="ds_id", attributes={"name": "Name2"})


Insights Service
================

The ``gooddata_sdk.insights`` service gives you access to insights stored in a workspace. It can retrieve all the insights from a workspace or one
insight based on its name. Insight instance is the input for other services like a `Table service`_

Example of how to read all insights in a workspace:

.. code-block:: python

    workspace_id = "demo"

    # reads insights from workspace
    insights = sdk.insights.get_insights(workspace_id)
    # print all fetched insights
    for insight in insights:
        print(str(insight))

Compute Service
===============

The ``gooddata_sdk.compute`` service drives computation of analytics for GoodData.CN workspaces. The prescription of what to compute
is encapsulated by the ExecutionDefinition which consists of attributes, metrics, filters and definition of
dimensions that influence how to organize the data in the result.

Higher level services like `Table service`_ use Compute service to execute computation in GoodData.CN.
Higher level service is also responsible for results presentation to the user e.g. in tabular form.


Table Service
=============

The ``gooddata_sdk.table`` service allows you to consume analytics in typical tabular format. The service allows free-form
computations and computations of data for GoodData.CN Insights.

For example look at how you can get tabular data for an insight defined on your GoodData.CN server:

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
