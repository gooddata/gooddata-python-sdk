Catalog Permission Service
==========================

The ``gooddata_sdk.catalog_permission`` service enables you to perform the following actions
on permissions:

* Get and set declarative permissions

Declarative methods
*******************
The *gooddata_sdk.catalog_permission* supports the following declarative API calls:

* ``get_declarative_permissions(workspace_id: str)``

    Returns *CatalogDeclarativeWorkspacePermissions*.

    Retrieve current set of permissions of the workspace in a declarative form.

* ``put_declarative_permissions(workspace_id: str, declarative_workspace_permissions: CatalogDeclarativeWorkspacePermissions)``

    Set effective permissions for the workspace.

**Example Usage**

.. code-block:: python

    from gooddata_sdk import GoodDataSdk

    # GoodData.CN host in the form of uri eg. "http://localhost:3000"
    host = "http://localhost:3000"
    # GoodData.CN user token
    token = "some_user_token"
    sdk = GoodDataSdk.create(host, token)

    workspace_id = "demo"

    # Get permissions in declarative from
    declarative_permissions = sdk.catalog_permission.get_declarative_permissions(workspace_id=workspace_id)

    declarative_permissions.permissions = []

    # Update permissions on the server with your changes
    sdk.catalog_permission.put_declarative_permissions(workspace_id=workspace_id,
                                                       declarative_workspace_permissions=declarative_permissions)
