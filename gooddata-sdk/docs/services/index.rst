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

* :doc:`Catalog Workspace <catalog-workspace>`: Read, update, create and delete workspaces.

   * :ref:`w entity methods`
   * :ref:`w declarative methods`

* :doc:`Catalog Workspace Content <catalog-workspace-content>`: Read catalog objects (datasets and metrics) from a workspace.

   * :ref:`wc entity methods`
   * :ref:`wc declarative methods`

* :doc:`Catalog Data Source <catalog-data-source>`: Read, update, create and delete data sources and read their tables.

   * :ref:`ds entity methods`
   * :ref:`ds declarative methods`
   * :ref:`ds action methods`

* :doc:`Insights <insight>`: Read insights stored in a workspace.

   * :ref:`i entity methods`

* :doc:`Compute <compute>`: Drives computation of analytics for GoodData.CN workspaces. Used by higher level services such as the Table service.

   * :ref:`c entity methods`

* :doc:`Table <table>`: Compute and read analytics in typical tabular format.

   * :ref:`t entity methods`
