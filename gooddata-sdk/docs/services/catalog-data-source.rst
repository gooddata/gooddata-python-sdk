Catalog Data Source Service
***************************

The ``gooddata_sdk.catalog_data_source`` service enables you to manage data sources and
list their tables. Data source object represents your database, which you integrate with
GoodData.CN.

Generally there are two ways how to register data sources:

* The default way works for all data source types: You specify jdbc url, data source type and relevant credentials.

* Customized way for each of the different data source types. You specify custom attributes relevant for your data source and data source type and the url is set in background.

The service supports three types of methods:

* Entity methods let you work with data sources on a high level using simplified *CatalogDataSource* entities.
* Declarative methods allow you to work with data sources on a more granular level by fetching entire workspace layouts, including all of their nested objects.
* Action methods let you perform an execution of some form of computation.

Entity methods
^^^^^^^^^^^^^^

The *gooddata_sdk.catalog_data_source* supports the following entity API calls:

* ``create_or_update_data_source(data_source: CatalogDataSource)``

    Create or update data source.

* ``list_data_sources()``

    Returns *List[CatalogDataSource]*.

    Lists all data sources.

* ``get_data_source(data_source_id: str)``

    Returns *CatalogDataSource*.

    Retrieve data source using data source id.

* ``delete_data_source(data_source_id: str)``

    Delete data source using data source id.

* ``patch_data_source_attributes(data_source_id: str, attributes: dict)``

    Allows you to apply changes to the given data source.

**Example Usage**

.. code-block:: python

    from gooddata_sdk import GoodDataSdk

    # GoodData.CN host in the form of uri eg. "http://localhost:3000"
    host = "http://localhost:3000"
    # GoodData.CN user token
    token = "some_user_token"
    sdk = GoodDataSdk.create(host, token)

    # Create (or update) data source using general interface - can be used for any type of data source
    # If data source already exists, it is updated
    sdk.catalog_data_source.create_or_update_data_source(
        CatalogDataSource(
            id="test",
            name="Test2",
            data_source_type="POSTGRESQL",
            url="jdbc:postgresql://localhost:5432/demo",
            schema="demo",
            credentials=BasicCredentials(
                username="demouser",
                password="demopass",
            ),
            enable_caching=False,
            url_params=[("param", "value")]
        )
    )

    # Use Postgres specific interface
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

    # Create Snowflake data source using specialized interface
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

    # List data sources
    data_sources = sdk.catalog_data_source.list_data_sources()

    # Get single data source
    data_sources = sdk.catalog_data_source.get_data_source('ds_id')

    # Delete data source
    sdk.catalog_data_source.delete_data_source(data_source_id='ds_id')

    # Patch data source attribute(s)
    sdk.catalog_data_source.patch_data_source_attributes(data_source_id="ds_id", attributes={"name": "Name2"})

Declarative methods
^^^^^^^^^^^^^^^^^^^

The *gooddata_sdk.catalog_data_source* supports the following declarative API calls:

* ``get_declarative_data_sources()``

    Returns *CatalogDeclarativeDataSources*.

    Retrieve all data sources, including their related physical model.

* ``put_declarative_data_sources(declarative_data_sources: CatalogDeclarativeDataSources, credentials_path: Optional[Path] = None, test_data_sources: bool = False)``

    Set all data sources, including their related physical model.

* ``store_declarative_data_sources(layout_root_path: Path = Path.cwd())``

    Store data sources layouts in directory hierarchy.

    ::

        gooddata_layouts
        └── organization_id
                └── data_sources
                        ├── data_source_a
                        │       ├── pdm
                        │       │   ├── table_A.yaml
                        │       │   └── table_B.yaml
                        │       └── data_source_a.yaml
                        └── data_source_b
                                └── pdm
                                │   ├── table_X.yaml
                                │   └── table_Y.yaml
                                └── data_source_b.yaml

* ``load_declarative_data_sources(layout_root_path: Path = Path.cwd())``

    Returns *CatalogDeclarativeDataSources*.

    Load declarative data sources layout, which was stored using *store_declarative_data_sources*.

* ``load_and_put_declarative_data_sources(layout_root_path: Path = Path.cwd(), credentials_path: Optional[Path] = None, test_data_sources: bool = False)``

    This method combines *load_declarative_data_sources* and
    *put_declarative_data_sources* methods to load and set
    layouts stored using *store_declarative_data_sources*.

**Example usage:**

.. code-block:: python

    from gooddata_sdk import GoodDataSdk
    from pathlib import Path

    # GoodData.CN host in the form of uri eg. "http://localhost:3000"
    host = "http://localhost:3000"
    # GoodData.CN user token
    token = "some_user_token"
    sdk = GoodDataSdk.create(host, token)

    # Get all data sources
    ds_objects = sdk.catalog_data_source.get_declarative_data_sources()

    print(ds_objects.data_sources[0])
    # CatalogDeclarativeDataSource(id=demo-test-ds, type=POSTGRESQL)

    # Put data sources with credentials and test data source connection before put
    sdk.catalog_data_source.put_declarative_data_sources(data_sources, Path("credentials"), True)

Action methods
^^^^^^^^^^^^^^

The *gooddata_sdk.catalog_data_source* supports the following action API calls:

* ``generate_logical_model(data_source_id: str, generate_ldm_request: CatalogGenerateLdmRequest)``

    Returns *CatalogDeclarativeModel*.

    Generate logical data model for a data source.

* ``register_upload_notification(data_source_id: str)``

    Invalidate cache of your computed reports to force your analytics to be recomputed.

* ``scan_data_source(data_source_id: str, scan_request: CatalogScanModelRequest = CatalogScanModelRequest(), report_warnings: bool = False)``

    Returns *CatalogScanResultPdm*.

    Scan data source specified by its id and optionally by specified scan request. *CatalogScanResultPdm* contains PDM and warnings. Warnings contain information about columns which were not added to the PDM because their data types are not supported. Additional parameter report_warnings can be passed to suppress or to report warnings. By default warnings are returned but not reported to STDOUT. If you set report_warnings to True, warnings are reported to STDOUT.

* ``scan_and_put_pdm(data_source_id: str, scan_request: CatalogScanModelRequest = CatalogScanModelRequest())``

    This method combines *scan_data_source* and *put_declarative_pdm* methods.

* ``scan_schemata(data_source_id: str)``

    Returns *list[str]*.

    Returns a list of schemas that exist in the database and can be configured in the data source entity. Data source managers like Dremio or Drill can work with multiple schemas and schema names can be injected into scan_request to filter out tables stored in the different schemas.

**Example usage:**

.. code-block:: python

    from gooddata_sdk import GoodDataSdk, CatalogGenerateLdmRequest

    # GoodData.CN host in the form of uri eg. "http://localhost:3000"
    host = "http://localhost:3000"
    # GoodData.CN user token
    token = "some_user_token"
    sdk = GoodDataSdk.create(host, token)

    # Scan schemata of the data source
    schemata = sdk.catalog_data_source.scan_schemata("demo-test-ds")
    print(schemata)
    # ['demo']

    # Scan and put pdm
    sdk.catalog_data_source.scan_and_put_pdm("demo-test-ds")

    # Define request for generating ldm
    generate_ldm_request = CatalogGenerateLdmRequest(separator="__")

    # Generate ldm
    declarative_model = sdk.catalog_data_source.generate_logical_model("demo-test-ds", generate_ldm_request)

    # Invalidate cache of your computed reports
    sdk.catalog_data_source.register_upload_notification("demo-test-ds")
