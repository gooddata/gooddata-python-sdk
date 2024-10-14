# (C) 2022 GoodData Corporation
from __future__ import annotations

import copy
import json
from pathlib import Path

from gooddata_sdk import (
    CatalogAssigneeIdentifier,
    CatalogDeclarativeUser,
    CatalogDeclarativeUserGroup,
    CatalogDeclarativeUserGroups,
    CatalogDeclarativeUsersUserGroups,
    CatalogPermissionsAssignment,
    CatalogUser,
    CatalogUserGroup,
    GoodDataApiClient,
    GoodDataSdk,
)
from gooddata_sdk.utils import recreate_directory
from tests_support.vcrpy_utils import get_vcr

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures" / "users"


# ENTITY USERS


@gd_vcr.use_cassette(str(_fixtures_dir / "list_users.yaml"))
def test_list_users(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    users = sdk.catalog_user.list_users()
    assert len(users) == 3
    assert set(user.id for user in users) == {"demo2", "admin", "demo"}


@gd_vcr.use_cassette(str(_fixtures_dir / "get_user.yaml"))
def test_get_user(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    user = sdk.catalog_user.get_user(test_config["test_user"])
    assert user.id == test_config["test_user"]
    assert [i.id for i in user.user_groups] == [test_config["test_user_group"]]


@gd_vcr.use_cassette(str(_fixtures_dir / "create_delete_user.yaml"))
def test_create_delete_user(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    user_id = test_config["test_new_user"]
    firstname = "john"
    lastname = "doe"
    email = "john.doe@email.com"
    authentication_id = f"{user_id}_auth_id"
    user_group_ids = [test_config["test_user_group"]]

    try:
        assert len(sdk.catalog_user.list_users()) == 3
        user_e = CatalogUser.init(
            user_id=user_id,
            firstname=firstname,
            lastname=lastname,
            email=email,
            authentication_id=authentication_id,
            user_group_ids=user_group_ids,
        )
        sdk.catalog_user.create_or_update_user(user_e)
        user = sdk.catalog_user.get_user(user_id)
        assert len(sdk.catalog_user.list_users()) == 4
        assert user.id == user_id
        assert [i.id for i in user.user_groups] == user_group_ids
        assert user.attributes.firstname == firstname
        assert user.attributes.lastname == lastname
        assert user.attributes.email == email
        assert user.attributes.authentication_id == authentication_id
    finally:
        sdk.catalog_user.delete_user(user_id)
        assert len(sdk.catalog_user.list_users()) == 3


@gd_vcr.use_cassette(str(_fixtures_dir / "update_user.yaml"))
def test_update_user(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    user_id = test_config["test_user"]
    user = sdk.catalog_user.get_user(user_id)
    new_firstname = "Michael"
    new_lastname = "Scott"
    new_email = "m.scott@dundermifflin.us"
    new_auth_id = f"{user_id}_123"
    user_group_ids = ["demoGroup", "visitorsGroup"]
    try:
        user_e = CatalogUser.init(
            user_id=user_id,
            firstname=new_firstname,
            lastname=new_lastname,
            email=new_email,
            authentication_id=new_auth_id,
            user_group_ids=user_group_ids,
        )
        sdk.catalog_user.create_or_update_user(user_e)
        updated_user = sdk.catalog_user.get_user(user_id)
        assert updated_user.attributes.firstname == new_firstname
        assert updated_user.attributes.lastname == new_lastname
        assert updated_user.attributes.email == new_email
        assert updated_user.attributes.authentication_id == new_auth_id
        assert len(updated_user.user_groups) == len(user_group_ids)
        assert set([i.id for i in updated_user.user_groups]) == set(user_group_ids)

    finally:
        sdk.catalog_user.delete_user(user_id)
        sdk.catalog_user.create_or_update_user(user)
        assert len(sdk.catalog_user.list_users()) == 3


# ENTITY USER GROUPS


@gd_vcr.use_cassette(str(_fixtures_dir / "list_user_groups.yaml"))
def test_list_user_groups(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    user_groups = sdk.catalog_user.list_user_groups()
    assert len(user_groups) == 4
    assert set(user_group.id for user_group in user_groups) == {
        "adminGroup",
        "demoGroup",
        "adminQA1Group",
        "visitorsGroup",
    }
    assert set(user_group.name for user_group in user_groups) == {"demo group", "visitors", None}


@gd_vcr.use_cassette(str(_fixtures_dir / "get_user_group.yaml"))
def test_get_user_group(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    user_group = sdk.catalog_user.get_user_group(test_config["test_user_group"])
    assert user_group.id == test_config["test_user_group"]


@gd_vcr.use_cassette(str(_fixtures_dir / "create_delete_user_group.yaml"))
def test_create_delete_user_group(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    user_group_id = test_config["test_new_user_group"]
    user_group_parent_ids = [test_config["test_user_group"]]

    try:
        current_user_groups = sdk.catalog_user.list_user_groups()
        assert len(current_user_groups) == 4
        assert set(ug.name for ug in current_user_groups) == {"demo group", "visitors", None}
        user_group_e = CatalogUserGroup.init(
            user_group_id=user_group_id,
            user_group_name=user_group_id.upper(),
            user_group_parent_ids=user_group_parent_ids,
        )
        sdk.catalog_user.create_or_update_user_group(user_group_e)
        user_group = sdk.catalog_user.get_user_group(user_group_id)
        assert len(sdk.catalog_user.list_user_groups()) == 5
        assert user_group.id == user_group_id
        assert user_group.name == user_group_id.upper()
        assert [p.id for p in user_group.relationships.parents.data] == user_group_parent_ids
    finally:
        sdk.catalog_user.delete_user_group(user_group_id)
        assert len(sdk.catalog_user.list_user_groups()) == 4


@gd_vcr.use_cassette(str(_fixtures_dir / "update_user_group.yaml"))
def test_update_user_group(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    user_group_id = test_config["test_user_group"]
    user_group = sdk.catalog_user.get_user_group(user_group_id)
    user_group_parent_ids = []
    new_user_group_name = "test_update_user_group"
    assert len(sdk.catalog_user.list_user_groups()) == 4

    try:
        user_group_e = CatalogUserGroup.init(
            user_group_id=user_group_id,
            user_group_name=new_user_group_name,
            user_group_parent_ids=user_group_parent_ids,
        )
        sdk.catalog_user.create_or_update_user_group(user_group_e)
        updated_user_group = sdk.catalog_user.get_user_group(user_group_id)
        assert user_group.id == updated_user_group.id
        assert updated_user_group.name == new_user_group_name
        assert user_group.relationships == updated_user_group.relationships
        assert len(updated_user_group.get_parents) == len(user_group_parent_ids)
        assert set(updated_user_group.get_parents) == set(user_group_parent_ids)
    finally:
        sdk.catalog_user.create_or_update_user_group(user_group)
        assert len(sdk.catalog_user.list_user_groups()) == 4


# DECLARATIVE USERS


@gd_vcr.use_cassette(str(_fixtures_dir / "get_declarative_users.yaml"))
def test_get_declarative_users(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    client = GoodDataApiClient(host=test_config["host"], token=test_config["token"])
    layout_api = client.layout_api

    users = sdk.catalog_user.get_declarative_users()

    _assert_users_default(users.users)
    assert users.to_dict(camel_case=True) == layout_api.get_users_layout().to_dict(camel_case=True)


@gd_vcr.use_cassette(str(_fixtures_dir / "store_declarative_users.yaml"))
def test_store_declarative_users(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "store"
    recreate_directory(path)

    users_e = sdk.catalog_user.get_declarative_users()
    _assert_users_default(users_e.users)

    sdk.catalog_user.store_declarative_users(path)
    users_o = sdk.catalog_user.load_declarative_users(path)

    assert users_e == users_o
    assert users_e.to_dict(camel_case=True) == users_o.to_dict(camel_case=True)


@gd_vcr.use_cassette(str(_fixtures_dir / "put_declarative_users.yaml"))
def test_put_declarative_users(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    users_e = sdk.catalog_user.get_declarative_users()
    _assert_users_default(users_e.users)

    try:
        _clear_users(sdk)

        sdk.catalog_user.put_declarative_users(users_e)
        users_o = sdk.catalog_user.get_declarative_users()
        assert users_e == users_o
        assert users_e.to_dict(camel_case=True) == users_o.to_dict(camel_case=True)
    finally:
        sdk.catalog_user.put_declarative_users(users_e)


@gd_vcr.use_cassette(str(_fixtures_dir / "load_and_put_declarative_users.yaml"))
def test_load_and_put_declarative_users(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "load"
    users_e = sdk.catalog_user.get_declarative_users()
    _assert_users_default(users_e.users)

    try:
        _clear_users(sdk)

        sdk.catalog_user.load_and_put_declarative_users(path)
        users_o = sdk.catalog_user.get_declarative_users()
        assert set(user.id for user in users_e.users) == set(user.id for user in users_o.users)
        assert [user.user_groups for user in users_e.users] == [user.user_groups for user in users_o.users]
    finally:
        sdk.catalog_user.put_declarative_users(users_e)


# DECLARATIVE USER GROUPS


@gd_vcr.use_cassette(str(_fixtures_dir / "get_declarative_user_groups.yaml"))
def test_get_declarative_user_groups(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    client = GoodDataApiClient(host=test_config["host"], token=test_config["token"])
    layout_api = client.layout_api

    user_groups = sdk.catalog_user.get_declarative_user_groups()

    _assert_user_groups_default(user_groups.user_groups)
    assert user_groups.to_dict(camel_case=True) == layout_api.get_user_groups_layout().to_dict(camel_case=True)


@gd_vcr.use_cassette(str(_fixtures_dir / "store_declarative_user_groups.yaml"))
def test_store_declarative_user_groups(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "store"
    recreate_directory(path)

    user_groups_e = sdk.catalog_user.get_declarative_user_groups()
    _assert_user_groups_default(user_groups_e.user_groups)

    sdk.catalog_user.store_declarative_user_groups(path)
    user_groups_o = sdk.catalog_user.load_declarative_user_groups(path)

    assert user_groups_e == user_groups_o
    assert user_groups_e.to_dict(camel_case=True) == user_groups_o.to_dict(camel_case=True)


@gd_vcr.use_cassette(str(_fixtures_dir / "put_declarative_user_groups.yaml"))
def test_put_declarative_user_groups(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    user_groups_path = _current_dir / "expected" / "declarative_user_groups.json"
    user_groups_e = sdk.catalog_user.get_declarative_user_groups()
    users_e = sdk.catalog_user.get_declarative_users()

    _assert_user_groups_default(user_groups_e.user_groups)
    _assert_users_default(users_e.users)

    try:
        _clear_users(sdk)
        _clear_user_groups(sdk)

        sdk.catalog_user.put_declarative_user_groups(user_groups_e)
        user_groups_o = sdk.catalog_user.get_declarative_user_groups()
        assert user_groups_e == user_groups_o
        assert user_groups_e.to_dict(camel_case=True) == user_groups_o.to_dict(camel_case=True)
    finally:
        with open(user_groups_path) as f:
            data = json.load(f)
        user_groups_o = CatalogDeclarativeUserGroups.from_dict(data, camel_case=True)
        sdk.catalog_user.put_declarative_user_groups(user_groups_o)

        sdk.catalog_user.put_declarative_users(users_e)


@gd_vcr.use_cassette(str(_fixtures_dir / "load_and_put_declarative_user_groups.yaml"))
def test_load_and_put_declarative_user_groups(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "load"
    expected_json_path = _current_dir / "expected" / "declarative_user_groups.json"
    users_e = sdk.catalog_user.get_declarative_users()
    user_groups_e = sdk.catalog_user.get_declarative_user_groups()

    _assert_user_groups_default(user_groups_e.user_groups)
    _assert_users_default(users_e.users)

    try:
        _clear_users(sdk)
        _clear_user_groups(sdk)

        sdk.catalog_user.load_and_put_declarative_user_groups(path)
        user_groups_o = sdk.catalog_user.get_declarative_user_groups()
        assert user_groups_e == user_groups_o
        assert user_groups_e.to_dict(camel_case=True) == user_groups_o.to_dict(camel_case=True)
    finally:
        with open(expected_json_path) as f:
            data = json.load(f)
        user_groups_o = CatalogDeclarativeUserGroups.from_dict(data, camel_case=True)
        sdk.catalog_user.put_declarative_user_groups(user_groups_o)

        sdk.catalog_user.put_declarative_users(users_e)


# DECLARATIVE USERS AND USER GROUPS
@gd_vcr.use_cassette(str(_fixtures_dir / "get_declarative_users_user_groups.yaml"))
def test_get_declarative_users_user_groups(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    client = GoodDataApiClient(host=test_config["host"], token=test_config["token"])
    layout_api = client.layout_api

    users_user_groups = sdk.catalog_user.get_declarative_users_user_groups()

    _assert_users_user_groups_default(users_user_groups)
    assert users_user_groups.to_dict(camel_case=True) == layout_api.get_users_user_groups_layout().to_dict(
        camel_case=True
    )


@gd_vcr.use_cassette(str(_fixtures_dir / "store_declarative_users_user_groups.yaml"))
def test_store_declarative_users_user_groups(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "store"
    recreate_directory(path)

    users_user_groups_e = sdk.catalog_user.get_declarative_users_user_groups()
    _assert_users_user_groups_default(users_user_groups_e)

    sdk.catalog_user.store_declarative_users_user_groups(path)
    users_user_groups_o = sdk.catalog_user.load_declarative_users_user_groups(path)

    assert users_user_groups_e == users_user_groups_o
    assert users_user_groups_e.to_dict(camel_case=True) == users_user_groups_o.to_dict(camel_case=True)


@gd_vcr.use_cassette(str(_fixtures_dir / "put_declarative_users_user_groups.yaml"))
def test_put_declarative_users_user_groups(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    users_user_groups_e = sdk.catalog_user.get_declarative_users_user_groups()
    _assert_users_user_groups_default(users_user_groups_e)

    try:
        _clear_users(sdk)
        _clear_user_groups(sdk)

        sdk.catalog_user.put_declarative_users_user_groups(users_user_groups_e)
        users_user_groups_o = sdk.catalog_user.get_declarative_users_user_groups()
        assert users_user_groups_e == users_user_groups_o
        assert users_user_groups_e.to_dict(camel_case=True) == users_user_groups_o.to_dict(camel_case=True)
    finally:
        sdk.catalog_user.put_declarative_users_user_groups(users_user_groups_e)


@gd_vcr.use_cassette(str(_fixtures_dir / "load_and_put_declarative_users_user_groups.yaml"))
def test_load_and_put_declarative_users_user_groups(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "load"
    users_user_groups_e = sdk.catalog_user.get_declarative_users_user_groups()
    _assert_users_user_groups_default(users_user_groups_e)

    try:
        _clear_users(sdk)
        _clear_user_groups(sdk)

        sdk.catalog_user.load_and_put_declarative_users_user_groups(path)
        users_user_groups_o = sdk.catalog_user.get_declarative_users_user_groups()
        _assert_users_user_groups_default(users_user_groups_o)
    finally:
        sdk.catalog_user.put_declarative_users_user_groups(users_user_groups_e)


@gd_vcr.use_cassette(str(_fixtures_dir / "test_user_add_user_group.yaml"))
def test_user_add_user_group(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    user_1 = sdk.catalog_user.get_user(test_config["test_user"])
    user_2 = CatalogUser(id="x")

    user_group = CatalogUserGroup(id="xyz")

    # existing user with user groups
    assert user_1.id == test_config["test_user"]
    assert [i.id for i in user_1.user_groups] == [test_config["test_user_group"]]

    user_1.add_user_group(user_group)
    expected_1 = [test_config["test_user_group"]] + [user_group.id]
    assert [i.id for i in user_1.user_groups] == expected_1

    # base user without user groups
    assert user_2.user_groups == []

    user_2.add_user_group(user_group)
    assert [i.id for i in user_2.user_groups] == [user_group.id]


@gd_vcr.use_cassette(str(_fixtures_dir / "test_user_add_user_groups.yaml"))
def test_user_add_user_groups(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    user_1 = sdk.catalog_user.get_user(test_config["test_user"])
    user_2 = CatalogUser(id="x")

    user_group_1 = CatalogUserGroup(id="abc")
    user_group_2 = CatalogUserGroup(id="xyz")
    user_groups = [user_group_1, user_group_2]
    user_groups_id = [user_group_1.id, user_group_2.id]

    # existing user with user groups
    assert user_1.id == test_config["test_user"]
    assert [i.id for i in user_1.user_groups] == [test_config["test_user_group"]]

    user_1.add_user_groups(user_groups)
    expected = [test_config["test_user_group"]] + user_groups_id
    assert [i.id for i in user_1.user_groups] == expected

    # base user without user groups
    assert user_2.user_groups == []

    user_2.add_user_groups(user_groups)
    assert [i.id for i in user_2.user_groups] == user_groups_id


@gd_vcr.use_cassette(str(_fixtures_dir / "test_user_remove_user_groups.yaml"))
def test_user_remove_user_groups(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    user_1 = sdk.catalog_user.get_user(test_config["test_user"])
    user_2 = CatalogUser(id="x")

    # existing user with user groups
    assert user_1.id == test_config["test_user"]
    assert [i.id for i in user_1.user_groups] == [test_config["test_user_group"]]

    user_1.remove_user_groups()

    assert user_1.user_groups == []

    # base user without user groups
    user_2.remove_user_groups()

    assert user_1.user_groups == []


@gd_vcr.use_cassette(str(_fixtures_dir / "test_user_replace_user_groups.yaml"))
def test_user_replace_user_groups(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    user_1 = sdk.catalog_user.get_user(test_config["test_user"])
    user_2 = CatalogUser(id="x")

    user_group_1 = CatalogUserGroup(id="abc")
    user_group_2 = CatalogUserGroup(id="xyz")
    user_groups = [user_group_1, user_group_2]

    # existing user with user groups
    assert user_1.id == test_config["test_user"]
    assert [i.id for i in user_1.user_groups] == [test_config["test_user_group"]]

    user_1.replace_user_groups(user_groups)
    assert user_1.user_groups == user_groups

    # base user without user groups
    user_2.replace_user_groups(user_groups)
    assert user_2.user_groups == user_groups


@gd_vcr.use_cassette(str(_fixtures_dir / "test_get_user_permissions.yaml"))
def test_get_user_permissions(test_config):
    """
    TODO: tests above corrupts result for permissions tests – the fix is required
    """
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    user_id = test_config["test_user"]
    workspace_id = test_config["workspace"]
    workspace_name = test_config["workspace_name"]
    data_source_id = test_config["data_source"]

    permissions = sdk.catalog_user.get_user_permissions(user_id)
    assert len(permissions.workspaces) == 1
    assert permissions.workspaces[0].id == workspace_id
    assert permissions.workspaces[0].name == workspace_name
    assert permissions.workspaces[0].permissions == ["ANALYZE"]
    assert permissions.workspaces[0].hierarchy_permissions == ["MANAGE"]

    assert len(permissions.data_sources) == 1
    assert permissions.data_sources[0].id == data_source_id
    assert permissions.data_sources[0].name == data_source_id
    assert permissions.data_sources[0].permissions == ["MANAGE"]


@gd_vcr.use_cassette(str(_fixtures_dir / "test_manage_user_permissions.yaml"))
def test_manage_user_permissions(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    user_id = test_config["test_user"]

    origin_permissions = sdk.catalog_user.get_user_permissions(user_id)
    try:
        new_permissions = copy.deepcopy(origin_permissions)
        new_permissions.data_sources[0].permissions = ["USE"]
        new_permissions.workspaces[0].permissions = ["MANAGE"]
        sdk.catalog_user.manage_user_permissions(user_id, new_permissions)
        updated_permissions = sdk.catalog_user.get_user_permissions(user_id)

        assert updated_permissions.data_sources[0].permissions == ["USE"]
        assert updated_permissions.workspaces[0].permissions == ["MANAGE"]
        assert updated_permissions.workspaces[0].hierarchy_permissions == ["MANAGE"]
    finally:
        sdk.catalog_user.manage_user_permissions(user_id, origin_permissions)


@gd_vcr.use_cassette(str(_fixtures_dir / "test_get_user_group_permissions.yaml"))
def test_get_user_group_permissions(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    group_id = test_config["test_user_group"]
    workspace_id = test_config["workspace"]
    workspace_name = test_config["workspace_name"]
    data_source_id = test_config["data_source"]

    permissions = sdk.catalog_user.get_user_group_permissions(group_id)
    assert len(permissions.workspaces) == 1
    assert permissions.workspaces[0].id == workspace_id
    assert permissions.workspaces[0].name == workspace_name
    assert permissions.workspaces[0].permissions == ["VIEW"]
    assert permissions.workspaces[0].hierarchy_permissions == ["ANALYZE"]

    assert len(permissions.data_sources) == 1
    assert permissions.data_sources[0].id == data_source_id
    assert permissions.data_sources[0].name == data_source_id
    assert permissions.data_sources[0].permissions == ["USE"]


@gd_vcr.use_cassette(str(_fixtures_dir / "test_manage_user_group_permissions.yaml"))
def test_manage_user_group_permissions(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    group_id = test_config["test_user_group"]

    origin_permissions = sdk.catalog_user.get_user_group_permissions(group_id)
    try:
        new_permissions = copy.deepcopy(origin_permissions)
        new_permissions.data_sources[0].permissions = ["MANAGE"]
        new_permissions.workspaces[0].permissions = ["VIEW"]
        sdk.catalog_user.manage_user_group_permissions(group_id, new_permissions)
        updated_permissions = sdk.catalog_user.get_user_group_permissions(group_id)

        assert updated_permissions.data_sources[0].permissions == ["MANAGE"]
        assert updated_permissions.workspaces[0].permissions == ["VIEW"]
        assert updated_permissions.workspaces[0].hierarchy_permissions == ["ANALYZE"]
    finally:
        sdk.catalog_user.manage_user_group_permissions(group_id, origin_permissions)


@gd_vcr.use_cassette(str(_fixtures_dir / "test_assign_permissions_bulk.yaml"))
def test_assign_permissions_bulk(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    user_id = test_config["test_user"]
    group_id = test_config["test_user_group"]

    origin_permissions_user = sdk.catalog_user.get_user_permissions(user_id)
    origin_permissions_user_group = sdk.catalog_user.get_user_group_permissions(group_id)
    try:
        permission_assignment = CatalogPermissionsAssignment(
            assignees=[
                CatalogAssigneeIdentifier(id=user_id, type="user"),
                CatalogAssigneeIdentifier(id=group_id, type="userGroup"),
            ],
            workspaces=origin_permissions_user_group.workspaces,
            data_sources=origin_permissions_user.data_sources,
        )
        sdk.catalog_user.assign_permissions_bulk(permission_assignment)

        new_user_permissions = sdk.catalog_user.get_user_permissions(user_id)
        new_group_permissions = sdk.catalog_user.get_user_permissions(user_id)

        # we can compare permissions like this, because user and group have permissions to the same
        # workspaces and data sources, we only modify permissions itself
        assert new_group_permissions.workspaces == new_user_permissions.workspaces
        assert new_group_permissions.data_sources == new_user_permissions.data_sources

    finally:
        sdk.catalog_user.manage_user_permissions(user_id, origin_permissions_user)
        sdk.catalog_user.manage_user_group_permissions(group_id, origin_permissions_user_group)


@gd_vcr.use_cassette(str(_fixtures_dir / "test_revoke_permissions_bulk.yaml"))
def test_revoke_permissions_bulk(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    user_id = test_config["test_user"]

    origin_permissions = sdk.catalog_user.get_user_permissions(user_id)
    try:
        sdk.catalog_user.revoke_permissions_bulk(
            CatalogPermissionsAssignment(
                assignees=[CatalogAssigneeIdentifier(id=user_id, type="user")],
                workspaces=origin_permissions.workspaces,
                data_sources=origin_permissions.data_sources,
            )
        )
        permissions = sdk.catalog_user.get_user_permissions(user_id)
        assert len(permissions.workspaces) == 0
        assert len(permissions.data_sources) == 0
    finally:
        sdk.catalog_user.manage_user_permissions(user_id, origin_permissions)


@gd_vcr.use_cassette(str(_fixtures_dir / "test_api_tokens.yaml"))
def test_api_tokens(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    tokens = sdk.catalog_user.list_user_api_tokens(test_config["demo_user"])
    assert len(tokens) == 0

    token_id = "test_token"
    try:
        token = sdk.catalog_user.create_user_api_token(test_config["demo_user"], "test_token")
        assert token.id == token_id
        assert token.bearer_token is not None

        token = sdk.catalog_user.get_user_api_token(test_config["demo_user"], token_id)
        assert token.id == token_id
        assert token.bearer_token is None

        tokens = sdk.catalog_user.list_user_api_tokens(test_config["demo_user"])
        assert len(tokens) == 1
        assert tokens[0].id == token_id
        assert tokens[0].bearer_token is None
    finally:
        sdk.catalog_user.delete_user_api_token(test_config["demo_user"], token_id)
        tokens = sdk.catalog_user.list_user_api_tokens(test_config["demo_user"])
        assert len(tokens) == 0


# Help functions


def _assert_users_default(users: list[CatalogDeclarativeUser]):
    assert len(users) == 3
    assert [user.id for user in users] == ["admin", "demo", "demo2"]


def _assert_user_groups_default(user_groups: list[CatalogDeclarativeUserGroup]):
    assert len(user_groups) == 4
    assert set(user_group.id for user_group in user_groups) == {
        "adminGroup",
        "demoGroup",
        "adminQA1Group",
        "visitorsGroup",
    }
    assert set(user_group.name for user_group in user_groups) == {"demo group", "visitors", None}


def _assert_users_user_groups_default(users_user_groups: CatalogDeclarativeUsersUserGroups):
    _assert_users_default(users_user_groups.users)
    _assert_user_groups_default(users_user_groups.user_groups)


def _clear_users(sdk: GoodDataSdk) -> None:
    users = sdk.catalog_user.list_users()
    for user in users:
        if user.id not in ["admin", "demo"]:
            sdk.catalog_user.delete_user(user.id)


def _clear_user_groups(sdk: GoodDataSdk) -> None:
    sdk.catalog_user.put_declarative_user_groups(
        CatalogDeclarativeUserGroups(user_groups=[CatalogDeclarativeUserGroup(id="adminGroup")])
    )
