####################
  Services
####################

All services are accessible by class ``gooddata_sdk.GoodDataSdk``. The class forms an entry-point to the SDK.

To create an instance of GoodDataSdk:

.. code-block:: python

    from gooddata_sdk import GoodDataSdk

    # GoodData.CN host in the form of uri eg. "http://localhost:3000"
    host = "http://localhost:3000"
    # GoodData.CN user token
    token = "some_user_token"
    sdk = GoodDataSdk.create(host, token)

    # Now you can start calling services.
    # For example, get a list of all workspaces from my GoodData.CN project
    workspaces = sdk.catalog_workspace.list_workspaces()

**Supported services:**

* :doc:`Catalog Workspace <catalog-workspace>`: ``gooddata_sdk.catalog_workspace``

   Read, update, create and delete workspaces.

* :doc:`Catalog Workspace Content <catalog-workspace-content>`: ``gooddata_sdk.catalog_workspace_content``

   Read catalog objects (datasets and metrics) from a workspace.

* :doc:`Catalog Data Source <catalog-data-source>`: ``gooddata_sdk.catalog_data_source``

   Read, update, create and delete data sources and read their tables.

* :doc:`Insights <insight>`: ``gooddata_sdk.insights``

   Read insights stored in a workspace.

* :doc:`Compute <compute>`: ``gooddata_sdk.compute``

    Drives computation of analytics for GoodData.CN workspaces. Used by higher level services such as the Table service.

* :doc:`Table <table>`: ``gooddata_sdk.table``

   Compute and read analytics in typical tabular format.

**All service-related articles:**

.. toctree::
   :maxdepth: 2

   catalog-workspace
   catalog-workspace-content
   catalog-data-source
   insight
   compute
   table
