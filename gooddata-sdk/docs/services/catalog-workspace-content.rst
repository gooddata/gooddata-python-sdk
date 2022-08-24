Catalog Workspace Content Service
=================================

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
**************

The *gooddata_sdk.catalog_workspace_content* supports the following entity API calls:

* ``get_full_catalog(workspace_id: str)``

    Returns *CatalogWorkspaceContent*.

    Retrieve all datasets with attributes, facts, and metrics for a workspace.

* ``get_attributes_catalog(workspace_id: str)``

    Returns *list[CatalogAttribute]*

    Retrieve all attributes for a workspace.

* ``get_labels_catalog(workspace_id: str)``

    Returns *list[CatalogLabel]*

    Retrieve all labels for a workspace.

* ``get_metrics_catalog(workspace_id: str)``

    Returns *list[CatalogMetric]*

    Retrieve all metrics for a workspace.

* ``get_facts_catalog(workspace_id: str)``

    Returns *list[CatalogFact]*

    Retrieve all facts for a workspace.

* ``get_dependent_entities_graph(workspace_id: str)``

    Returns *CatalogDependentEntitiesResponse*

    | There are dependencies among all catalog objects, the chain is the following:
    | fact/attribute/label -> dataset -> metric -> insight -> dashboard

    | Some steps can be skipped, e.g. fact -> insight
    | We do not support table -> dataset dependency yet.

* ``get_dependent_entities_graph_from_entry_points(workspace_id: str, dependent_entities_request: CatalogDependentEntitiesRequest)``

    Returns *CatalogDependentEntitiesResponse*

    Extends *get_dependent_entities_graph* with the entry point from which the graph is created.

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
*******************

The *gooddata_sdk.catalog_workspace_content* supports the following declarative API calls:

Logical data model (LDM)
^^^^^^^^^^^^^^^^^^^^^^^^

* ``get_declarative_ldm(workspace_id: str)``

    Returns *CatalogDeclarativeModel*.

    Retrieve a logical model layout. On CatalogDeclarativeModel user can call ``modify_mapped_data_source(data_source_mapping: dict)`` method, which substitutes data source id in datasets.

* ``put_declarative_ldm(workspace_id: str, ldm: CatalogDeclarativeModel, validator: Optional[DataSourceValidator])``

    Put a logical data model into a given workspace. You can pass an additional validator parameter which checks that for every data source id in the logical data model the corresponding data source exists.

* ``store_declarative_ldm(workspace_id: str, layout_root_path: Path = Path.cwd())``

    Store logical data model layout in directory hierarchy.

    ::

        gooddata_layouts
        └── organization_id
                └── workspaces
                        └── workspace_id
                                └── analytics_model
                                        └── ldm
                                            ├── datasets
                                            │       └── dataset.yaml
                                            └── date_instances
                                                    └── date_instance.yaml

* ``load_declarative_ldm(workspace_id: str, layout_root_path: Path = Path.cwd())``

    Returns *CatalogDeclarativeModel*.

    Load declarative LDM layout, which was stored using *store_declarative_ldm*.

* ``load_and_put_declarative_ldm(workspace_id: str, layout_root_path: Path = Path.cwd(), validator: Optional[DataSourceValidator])``

    This method combines *load_declarative_ldm* and *put_declarative_ldm*
    methods to load and set layouts stored using *store_declarative_ldm*. You can pass an additional validator parameter which checks that for every data source id in the logical data model the corresponding data source exists.

Analytics Model
^^^^^^^^^^^^^^^

* ``get_declarative_analytics_model(workspace_id: str)``

    Returns *CatalogDeclarativeAnalytics*.

    Retrieve an analytics model layout.

* ``put_declarative_analytics_model(workspace_id: str, analytics_model: CatalogDeclarativeAnalytics)``

    Put an analytics model into a given workspace.

* ``store_declarative_analytics_model(workspace_id: str, layout_root_path: Path = Path.cwd())``

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



* ``load_declarative_analytics_model(workspace_id: str, layout_root_path: Path = Path.cwd())``

    Returns *CatalogDeclarativeAnalytics*.

    Load declarative LDM layout, which was stored using *store_declarative_analytics_model*.

* ``load_and_put_declarative_analytics_model(workspace_id: str, layout_root_path: Path = Path.cwd())``

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

    workspace_id = "demo"

    # Get ldm object afterward you can modify it
    ldm = sdk.catalog_workspace_content.get_declarative_ldm(workspace_id=workspace_id)

    # Modify data source id for datasets
    ldm.modify_mapped_data_source({"demo-test-ds": "demo-prod-ds"})

    # Put ldm object back to server
    sdk.catalog_workspace_content.put_declarative_ldm(workspace_id=workspace_id, ldm=ldm)

    # Get analytics model object afterward you can modify it
    analytics_model = sdk.catalog_workspace_content.get_declarative_analytics_model(workspace_id=workspace_id)

    # Put analytics model object back to server
    sdk.catalog_workspace_content.put_declarative_analytics_model(workspace_id=workspace_id,
                                                                  analytics_model=analytics_model)
