:orphan:

Catalog Workspace Service
*************************

The ``gooddata_sdk.catalog_workspace`` service enables you to perform the following actions
on workspaces:

* Get and list existing workspaces
* Update or delete existing workspaces
* Create new workspaces
* Store and restore workspaces from directory layout structure

The service supports two types of methods:

* Entity methods let you work with workspaces on a high level using simplified *CatalogWorkspace* entities.
* Declarative methods allow you to work with workspaces on a more granular level by fetching entire workspace layouts, including all of their nested objects.

.. _w entity methods:

Entity methods
^^^^^^^^^^^^^^

The *gooddata_sdk.catalog_workspace* supports the following entity API calls:

* ``get_workspace(workspace_id: str)``

    Returns *CatalogWorkspace*.

    Get an individual workspace.

* ``list_workspaces()``

    Returns *List[CatalogWorkspace]*.

    Get a list of all existing workspaces.

* ``create_or_update(workspace: CatalogWorkspace)``

    Create a new workspace or overwrite an existing workspace with the same id.

* ``delete_workspace(workspace_id: str)``

    Delete a workspace.

**Example Usage**

.. code-block:: python

    from gooddata_sdk import GoodDataSdk, CatalogWorkspace

    # GoodData.CN host in the form of uri eg. "http://localhost:3000"
    host = "http://localhost:3000"
    # GoodData.CN user token
    token = "some_user_token"
    sdk = GoodDataSdk.create(host, token)

    # List workspaces
    workspaces = sdk.catalog_workspace.list_workspaces()

    print(workspaces)
    # [
    #   CatalogWorkspace(id=demo, name=Demo),
    #   CatalogWorkspace(id=demo_west, name=Demo West),
    #   CatalogWorkspace(id=demo_west_california, name=Demo West California)
    # ]

    # Create new workspace entity locally
    my_workspace_object = CatalogWorkspace(workspace_id="test_demo",
                                           name="Test demo",
                                           parent_id="demo")

    # Create workspace
    sdk.catalog_workspace.create_or_update(workspace=my_workspace_object)

    # Edit local workspace entity
    my_workspace_object.name = "Test"

    # Update workspace
    sdk.catalog_workspace.create_or_update(workspace=my_workspace_object)

    # Get workspace
    workspace = sdk.catalog_workspace.get_workspace(workspace_id="test_demo")

    print(workspace)
    # CatalogWorkspace(id=test_demo, name=Test)

    # Delete workspace
    sdk.catalog_workspace.delete_workspace(workspace_id="test_demo")

.. _w declarative methods:

Declarative methods
^^^^^^^^^^^^^^^^^^^

The *gooddata_sdk.catalog_workspace* supports the following declarative API calls:

* ``get_declarative_workspace(workspace_id: str)``

    Returns *CatalogDeclarativeWorkspaceModel*.

    Retrieve a workspace layout.

* ``put_declarative_workspace(workspace_id: str)``

    Set a workspace layout.

* ``get_declarative_workspaces()``

    Returns *CatalogDeclarativeWorkspaces*.

    Retrieve layout of all workspaces and their hierarchy.

* ``put_declarative_workspaces(workspace: CatalogDeclarativeWorkspaces)``

    Set layout of all workspaces and their hierarchy.

* ``store_declarative_workspaces(layout_root_path: Path = Path.cwd())``

    Store workspaces layouts in directory hierarchy.

    ::

        gooddata_layouts
        └── organization_id
                ├── workspaces
                │       ├── workspace_a
                │       │       ├── analytics_model
                │       │       │   ├── analytical_dashboards
                │       │       │   │       └── analytical_dashboard.yaml
                │       │       │   ├── dashboard_plugins
                │       │       │   │       └── dashboard_plugin.yaml
                │       │       │   ├── filter_contexts
                │       │       │   │       └── filter_context.yaml
                │       │       │   ├── metrics
                │       │       │   │       └── metric.yaml
                │       │       │   └── visualization_objects
                │       │       │           └── visualization_object.yaml
                │       │       ├── ldm
                │       │       │   ├── datasets
                │       │       │   │       └── dataset.yaml
                │       │       │   └── date_instances
                │       │       │           └── date_instance.yaml
                │       │       └── workspace_a.yaml
                │       └── workspace_b
                │               └── ...
                │
                └── workspaces_data_filters
                        ├── filter_1.yaml
                        └── filter_2.yaml


* ``load_declarative_workspaces(layout_root_path: Path = Path.cwd())``

    Returns *CatalogDeclarativeWorkspaces*.

    Load declarative workspaces layout, which was stored using *store_declarative_workspaces*.

* ``load_and_put_declarative_workspaces(layout_root_path: Path = Path.cwd())``

    This method combines *load_declarative_workspaces* and *put_declarative_workspaces* methods to load and
    set layouts stored using *store_declarative_workspaces*.

**Example Usage**

.. code-block:: python

    from gooddata_sdk import GoodDataSdk
    from pathlib import Path

    # GoodData.CN host in the form of uri eg. "http://localhost:3000"
    host = "http://localhost:3000"
    # GoodData.CN user token
    token = "some_user_token"
    sdk = GoodDataSdk.create(host, token)

    backup_path = Path("workspace_hierarchy_backup")

    # First create a backup of all workspace layout
    sdk.catalog_workspace.store_declarative_workspaces(layout_root_path=backup_path)

    # Get workspace layout
    workspace_layout = sdk.catalog_workspace.get_declarative_workspace(workspace_id="demo")

    # Modify workspace layout
    workspace_layout.ldm.datasets[0].description = "This is test"

    # Update the workspace layout on the server with your changes
    sdk.catalog_workspace.put_declarative_workspace(workspace_id="demo",
                                                    workspace=workspace_layout)

    # If something goes wrong, use your backup to restore your workspaces from backup
    sdk.catalog_workspace.load_and_put_declarative_workspaces(layout_root_path=backup_path)
