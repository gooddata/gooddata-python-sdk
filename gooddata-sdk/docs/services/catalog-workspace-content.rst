Catalog Workspace Content Service
*********************************

The ``gooddata_sdk.catalog_workspace_content`` service enables you to
list catalog all objects from a workspace. These objects include:

* Datasets
* Metrics
* Facts
* Attributes

The service enables read, put, load and store of declarative layout for LDM (logical data model) and analytics model.

The service supports two types of methods:

* Entity methods let you work with workspace content on a high level using simplified entities.
* Declarative methods allow you to work with workspace content on a more granular level by fetching entire workspace content layouts, including all of their nested objects.

Entity methods
^^^^^^^^^^^^^^

The *gooddata_sdk.catalog_workspace_content* supports the following entity API calls:

* ``get_full_catalog(workspace_id: str)``

    Returns *CatalogWorkspaceContent*.

    Retrieve all datasets with attributes, facts, and metrics for a workspace.

**Example Usage**

.. code-block:: python

    from gooddata_sdk import GoodDataSdk

    # GoodData.CN host in the form of uri eg. "http://localhost:3000"
    host = "http://localhost:3000"
    # GoodData.CN user token
    token = "some_user_token"
    sdk = GoodDataSdk.create(host, token)

    workspace_id = "demo"

    # Read catalog for demo workspace
    catalog = sdk.catalog_workspace_content.get_full_catalog(workspace_id)

    # Print all dataset in the workspace
    for dataset in catalog.datasets:
        print(str(dataset))

    # Print all metrics in the workspace
    for metric in catalog.metrics:
        print(str(metric))

    # Read list of attributes for demo workspace
    attributes = sdk.catalog_workspace_content.get_attributes_catalog(workspace_id)

    # Read list of facts for demo workspace
    facts = sdk.catalog_workspace_content.get_facts_catalog(workspace_id)

Declarative methods
^^^^^^^^^^^^^^^^^^^

The *gooddata_sdk.catalog_workspace_content* supports the following declarative API calls:

**Logical Data Model:**

* ``get_declarative_ldm(workspace_id: str)``

    Returns *CatalogDeclarativeModel*.

    Retrieve a logical model layout. On CatalogDeclarativeModel user can call ``modify_mapped_data_source(data_source_mapping: dict)`` method, which substitues data source id in datasets.

* ``put_declarative_ldm(workspace_id: str, ldm: CatalogDeclarativeModel)``

    Set a logical model layout.

* ``store_declarative_ldm(workspace_id: str, layout_root_path: Path = Path(os.path.curdir))``

    Store logical data model layout in directory hierarchy.

    ::

        gooddata_layouts
        └── organization_id
                └── workspaces
                        └── workspace_id
                                └── analytics_model
                                        ├── ldm
                                        │    └── datasets
                                        │           └── dataset.yaml
                                        └── date_instaces
                                                    └── date_instace.yaml

* ``load_declarative_ldm(workspace_id: str, layout_root_path: Path = Path(os.path.curdir))``

    Returns *CatalogDeclarativeModel*.

    Load declarative LDM layout, which was stored using *store_declarative_ldm*.

* ``load_and_put_declarative_ldm(workspace_id: str, layout_root_path: Path = Path(os.path.curdir))``

    This method combines *load_declarative_ldm* and *put_declarative_ldm*
    methods to load and set layouts stored using *store_declarative_ldm*.

**Analytics Model:**

* ``get_declarative_analytics_model(workspace_id: str)``

    Returns *CatalogDeclarativeAnalytics*.

    Retrieve an analytics model layout.

* ``put_declarative_analytics_model(workspace_id: str, analytics_model: CatalogDeclarativeAnalytics)``

    Set an analytics model layout.

* ``store_declarative_analytics_model(workspace_id: str, layout_root_path: Path = Path(os.path.curdir))``

    Store declarative analytics model layout in directory hierarchy.

    ::

        gooddata_layouts
        └── organization_id
                └── workspaces
                        └── workspace_id
                                └── analytics_model
                                        ├── analytical_dashboards
                                        │       └── analytical_dashboard.yaml
                                        ├── dashboard_plugins
                                        │       └── dashboard_plugin.yaml
                                        ├── filter_contexts
                                        │       └── filter_context.yaml
                                        ├── metrics
                                        │       └── metric.yaml
                                        └── visualization_objects
                                                └── visualization_object.yaml



* ``load_declarative_analytics_model(workspace_id: str, layout_root_path: Path = Path(os.path.curdir))``

    Returns *CatalogDeclarativeAnalytics*.

    Load declarative LDM layout, which was stored using *store_declarative_analytics_model*.

* ``load_and_put_declarative_analytics_model(workspace_id: str, layout_root_path: Path = Path(os.path.curdir))``

    This method combines *load_declarative_analytics_model* and
    *put_declarative_analytics_model* methods to load and set
    layouts stored using *store_declarative_analytics_model*.

**Example usage:**

.. code-block:: python

    from gooddata_sdk import GoodDataSdk

    # GoodData.CN host in the form of uri eg. "http://localhost:3000"
    host = "http://localhost:3000"
    # GoodData.CN user token
    token = "some_user_token"
    sdk = GoodDataSdk.create(host, token)

    # Get ldm object afterward you can modify it
    ldm = sdk.catalog_workspace_content.get_declarative_ldm("demo")

    # Modify data source id for datasets
    ldm.modify_mapped_data_source({"demo-test-ds": "demo-prod-ds"})

    # Put ldm object back to server
    sdk.catalog_workspace_content.put_declarative_ldm("demo", ldm)

    # Get analytics model object afterward you can modify it
    analytics_model = sdk.catalog_workspace_content.get_declarative_analytics_model("demo")

    # Put analytics model object back to server
    sdk.catalog_workspace_content.put_declarative_analytics_model("demo", analytics_model)
