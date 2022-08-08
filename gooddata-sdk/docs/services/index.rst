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

.. toctree::
   :maxdepth: 2
   :caption: Supported services:

   Catalog Workspace <catalog-workspace>
   Catalog Workspace Content <catalog-workspace-content>
   Catalog Data Source <catalog-data-source>
   Catalog User <catalog-user>
   Catalog Permission <catalog-permission>
   Catalog Organization <catalog-organization>
   Insights <insight>
   Compute <compute>
   Table <table>
