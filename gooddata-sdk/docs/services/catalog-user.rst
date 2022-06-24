:orphan:

Catalog User Service
********************

The ``gooddata_sdk.catalog_user`` service enables you to perform the following actions
on users and user groups:

* Get and list existing users and user groups
* Update or delete existing users and user groups
* Create new users and user groups
* Store and restore users and user groups from directory layout structure

The service supports two types of methods:

* Entity methods let you work with users and user groups on a high level using simplified *CatalogUser* and *CatalogUserGroup*  entities.
* Declarative methods allow you to work with users and user groups on a more granular level by fetching entire users and user groups layouts.

.. _u entity methods:

Entity methods for users
^^^^^^^^^^^^^^^^^^^^^^^^

The *gooddata_sdk.catalog_user* supports the following user entity API calls:

* ``get_user(user_id: str)``

    Returns *CatalogUser*.

    Get an individual user.

* ``list_users()``

    Returns *List[CatalogUser]*.

    Get a list of all existing users.

* ``create_or_update_user(user: CatalogUser)``

    Create a new user or overwrite an existing user.

* ``delete_user(user_id: str)``

    Delete a user.

**Example Usage**

.. code-block:: python

    from gooddata_sdk import GoodDataSdk, CatalogUser

    # GoodData.CN host in the form of uri eg. "http://localhost:3000"
    host = "http://localhost:3000"
    # GoodData.CN user token
    token = "some_user_token"
    sdk = GoodDataSdk.create(host, token)

    # List users
    users = sdk.catalog_user.list_users()

    print(users)
    # [
    #   CatalogUser(id='demo2',
    #               attributes=CatalogUserAttributes(authentication_id='CiRmYmNhNDkwOS04YzYxLTRmMTYtODI3NC1iNzI0Njk1Y2FmNTESBWxvY2Fs'),
    #               relationships=CatalogUserRelationships(user_groups=CatalogUserGroupsData(data=[CatalogUserGroup(id='demoGroup', relationships=None)]))),
    #   ...
    # ]

    # Define user
    user = CatalogUser.init(user_id="abc", authentication_id="xyz",user_group_ids=["demoGroup"])

    # Create user
    sdk.catalog_user.create_or_update_user(user=user)

    # Delete user
    sdk.catalog_user.delete_user(user_id=user.id)


.. _ug entity methods:

Entity methods for user groups
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The *gooddata_sdk.catalog_user* supports the following user groups entity API calls:

* ``get_user_group(user_group_id: str)``

    Returns *CatalogUserGroup*.

    Get an individual user group.

* ``list_user_groups()``

    Returns *List[CatalogUserGroup]*.

    Get a list of all existing user groups.

* ``create_or_update_user_group(user_group: CatalogUserGroup)``

    Create a new user group or overwrite an existing user group.

* ``delete_user_group(user_group_id: str)``

    Delete a user group.

**Example Usage**

.. code-block:: python

    from gooddata_sdk import GoodDataSdk, CatalogUserGroup

    # GoodData.CN host in the form of uri eg. "http://localhost:3000"
    host = "http://localhost:3000"
    # GoodData.CN user token
    token = "some_user_token"
    sdk = GoodDataSdk.create(host, token)

    # List user groups
    user_groups = sdk.catalog_user.list_user_groups()

    print(user_groups)
    #[
    #    CatalogUserGroup(id='adminGroup', relationships=None),
    #    CatalogUserGroup(id='adminQA1Group',
    #                     relationships=CatalogUserGroupRelationships(parents=CatalogUserGroupParents(data=[CatalogUserGroup(id='adminGroup', relationships=None)])))
    #    ...
    #]

    # Define user
    user_group = CatalogUserGroup.init(user_group_id="xyz", user_group_parent_ids=["demoGroup"])

    # Create user
    sdk.catalog_user.create_or_update_user_group(user_group=user_group)

    # Delete user
    sdk.catalog_user.delete_user_group(user_group_id=user_group.id)

.. _u declarative methods:

Declarative methods for users
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The *gooddata_sdk.catalog_user* supports the following declarative user API calls:

* ``get_declarative_users()``

    Returns *CatalogDeclarativeUsers*.

    Retrieve all users including authentication properties.

* ``put_declarative_users(users: CatalogDeclarativeUsers)``

    Set all users and their authentication properties.

* ``store_declarative_users(layout_root_path: Path = Path.cwd())``

    Store users in directory hierarchy.

    ::

        gooddata_layouts
        └── organization_id
                └── users
                        └── users.yaml

* ``load_declarative_users(layout_root_path: Path = Path.cwd())``

    Load users from directory hierarchy.

* ``load_and_put_declarative_users(layout_root_path: Path = Path.cwd())``

    This method combines *load_declarative_users* and *put_declarative_users* methods to load and
    set users stored using *store_declarative_users*.

**Example Usage**

.. code-block:: python

    from gooddata_sdk import GoodDataSdk

    # GoodData.CN host in the form of uri eg. "http://localhost:3000"
    host = "http://localhost:3000"
    # GoodData.CN user token
    token = "some_user_token"
    sdk = GoodDataSdk.create(host, token)

    # Get user layout
    user_layout = sdk.catalog_user.get_declarative_users()

    print(user_layout)
    # CatalogDeclarativeUsers(
    #          users=[
    #                   CatalogDeclarativeUser(id='admin',
    #                                          auth_id=None,
    #                                          user_groups=[CatalogUserGroupIdentifier(id='adminGroup', type='userGroup')]),
    #                   CatalogDeclarativeUser(id='demo',...
    # ...

    # Modify user layout
    user_layout.users = []

    # Update user layout
    sdk.catalog_user.put_declarative_users(users=user_layout)

.. _ug declarative methods:

Declarative methods for user groups
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The *gooddata_sdk.catalog_user* supports the following declarative user groups API calls:

* ``get_declarative_user_groups()``

    Returns *CatalogDeclarativeUserGroups*.

    Retrieve all user-groups eventually with parent group.

* ``put_declarative_user_groups(user_groups: CatalogDeclarativeUserGroups)``

    Set all user groups with their parents eventually.

* ``store_declarative_user_groups(layout_root_path: Path = Path.cwd())``

    Store user groups in directory hierarchy.

    ::

        gooddata_layouts
        └── organization_id
                └── user_groups
                        └── user_groups.yaml


* ``load_declarative_user_groups(layout_root_path: Path = Path.cwd())``

    Returns *CatalogDeclarativeUserGroups*.

    Load user groups from directory hierarchy.

* ``load_and_put_declarative_user_groups(layout_root_path: Path = Path.cwd())``

    This method combines *load_declarative_user_groups* and *put_declarative_user_groups* methods to load and
    set user groups stored using *store_declarative_user_groups*.

**Example Usage**

.. code-block:: python

    from gooddata_sdk import GoodDataSdk

    # GoodData.CN host in the form of uri eg. "http://localhost:3000"
    host = "http://localhost:3000"
    # GoodData.CN user token
    token = "some_user_token"
    sdk = GoodDataSdk.create(host, token)

    # Get user layout
    user_group_layout = sdk.catalog_user.get_declarative_user_groups()

    print(user_group_layout)
    # CatalogDeclarativeUserGroups(
    #          user_groups=[
    #                   CatalogDeclarativeUserGroup(id='adminGroup', parents=None),
    # ...

    # Modify user group layout
    user_group_layout.user_groups = []

    # Update user group layout
    sdk.catalog_user.put_declarative_users(users=user_group_layout)

.. _uug declarative methods:

Declarative methods for users and user groups
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The *gooddata_sdk.catalog_user* supports the following declarative users and user groups API calls:

* ``get_declarative_users_user_groups()``

    Returns *CatalogDeclarativeUsersUserGroups*.

    Retrieve all users and all user-groups.

* ``put_declarative_users_user_groups(users_user_groups: CatalogDeclarativeUsersUserGroups)``

    Set all users and user groups.

* ``store_declarative_users_user_groups(layout_root_path: Path = Path.cwd())``

    Store users and user groups in directory hierarchy.

    ::

        gooddata_layouts
        └── organization_id
                ├── users
                │      └── users.yaml
                └── user_groups
                        └── user_groups.yaml


* ``load_declarative_users_user_groups(layout_root_path: Path = Path.cwd())``

    Returns *CatalogDeclarativeUsersUserGroups*.

    Load users and user groups from directory hierarchy.

* ``load_and_put_declarative_users_user_groups(layout_root_path: Path = Path.cwd())``

    This method combines *load_declarative_users_user_groups* and *put_declarative_users_user_groups* methods to load and
    set users and user groups stored using *store_declarative_users_user_groups*.
