# (C) 2022 GoodData Corporation
"""
Test module for catalog user service.

TEST INDEPENDENCE NOTES:
========================
Some tests in this module have dependencies on shared state (demo2 user and demoGroup
permissions). The following tests assume specific permission state:

- test_get_user_permissions: Expects demo2 to have ANALYZE workspace permission,
  MANAGE hierarchy permission, and MANAGE data source permission
- test_get_user_group_permissions: Expects demoGroup to have VIEW workspace permission,
  ANALYZE hierarchy permission, and USE data source permission

When regenerating VCR cassettes, ensure these tests run with fresh state or call
`_ensure_demo2_permissions_state()` at the start of each affected test.

Tests that modify shared state (demo2, demoGroup) should call `_restore_demo2_permissions()`
in their finally blocks to restore permissions.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
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
    """Test updating user attributes.

    This test creates a temporary user for testing updates to ensure test independence.
    We don't modify demo2 (test_user) directly because:
    1. demo2 has permission references that would be cascade-deleted
    2. Deleting/recreating demo2 in cleanup is complex and error-prone
    3. VCR cassette timing issues can cause state corruption

    The test flow:
    1. Create a temporary test user with initial attributes
    2. Update the user's attributes
    3. Verify updates were applied
    4. Clean up by deleting the temporary user
    """
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    # Use a temporary user ID that won't have permission references
    temp_user_id = "test_update_user_temp"
    test_user_group = test_config["test_user_group"]

    # Initial values
    initial_firstname = "Temp"
    initial_lastname = "User"
    initial_email = "temp.user@example.com"
    initial_auth_id = f"{temp_user_id}_auth"
    initial_user_group_ids = [test_user_group]

    # Updated values
    new_firstname = "Michael"
    new_lastname = "Scott"
    new_email = "m.scott@dundermifflin.us"
    new_auth_id = f"{temp_user_id}_123"
    new_user_group_ids = ["demoGroup", "visitorsGroup"]

    initial_user_count = len(sdk.catalog_user.list_users())

    try:
        # Create temporary user
        initial_user = CatalogUser.init(
            user_id=temp_user_id,
            firstname=initial_firstname,
            lastname=initial_lastname,
            email=initial_email,
            authentication_id=initial_auth_id,
            user_group_ids=initial_user_group_ids,
        )
        sdk.catalog_user.create_or_update_user(initial_user)
        assert len(sdk.catalog_user.list_users()) == initial_user_count + 1

        # Update the user
        updated_user_request = CatalogUser.init(
            user_id=temp_user_id,
            firstname=new_firstname,
            lastname=new_lastname,
            email=new_email,
            authentication_id=new_auth_id,
            user_group_ids=new_user_group_ids,
        )
        sdk.catalog_user.create_or_update_user(updated_user_request)

        # Verify updates
        updated_user = sdk.catalog_user.get_user(temp_user_id)
        assert updated_user.attributes.firstname == new_firstname
        assert updated_user.attributes.lastname == new_lastname
        assert updated_user.attributes.email == new_email
        assert updated_user.attributes.authentication_id == new_auth_id
        assert len(updated_user.user_groups) == len(new_user_group_ids)
        assert set([i.id for i in updated_user.user_groups]) == set(new_user_group_ids)

    finally:
        # Clean up: Delete temporary user (no cascade issues since it has no permissions)
        try:
            sdk.catalog_user.delete_user(temp_user_id)
        except Exception:
            pass  # User may not exist if creation failed
        # Verify we're back to original user count
        assert len(sdk.catalog_user.list_users()) == initial_user_count


def _restore_demo2_permissions(sdk: GoodDataSdk, test_config: dict) -> None:
    """Restore demo2's data source and workspace permissions after user deletion/recreation.

    This function restores the expected permission state for demo2 user and demoGroup.
    Call this in the finally block of any test that modifies demo2 or demoGroup, or that
    deletes/recreates entities that have permission references to these assignees.

    Expected state after restoration:
    - demo2 user:
        - workspace 'demo': permission=ANALYZE, hierarchy_permission=MANAGE
        - data source 'demo-test-ds': permission=MANAGE
    - demoGroup:
        - workspace 'demo': permission=VIEW, hierarchy_permission=ANALYZE
        - data source 'demo-test-ds': permission=USE

    Note: This function makes HTTP calls. When used in tests with VCR cassettes,
    ensure the cassette includes the restoration calls (in finally blocks).
    """
    from gooddata_sdk.catalog.data_source.declarative_model.data_source import CatalogDeclarativeDataSources

    # Restore data source permissions
    expected_ds_path = _current_dir / "expected" / "declarative_data_sources.json"
    with open(expected_ds_path) as f:
        ds_data = json.load(f)
    credentials_path = _current_dir / "load" / "data_source_credentials" / "data_sources_credentials.yaml"
    data_sources = CatalogDeclarativeDataSources.from_dict(ds_data)
    sdk.catalog_data_source.put_declarative_data_sources(data_sources, credentials_path)

    # Restore workspace permissions
    from gooddata_sdk.catalog.permission.declarative_model.permission import CatalogDeclarativeWorkspacePermissions

    expected_ws_path = _current_dir / "expected" / "declarative_workspace_permissions.json"
    with open(expected_ws_path) as f:
        ws_data = json.load(f)
    ws_permissions = CatalogDeclarativeWorkspacePermissions.from_dict(ws_data, camel_case=True)
    sdk.catalog_permission.put_declarative_permissions(test_config["workspace"], ws_permissions)


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


@pytest.mark.dependency(name="test_get_user_permissions")
@gd_vcr.use_cassette(str(_fixtures_dir / "test_get_user_permissions.yaml"))
def test_get_user_permissions(test_config):
    """Test retrieving user permissions.

    This test expects demo2 user to have specific permissions:
    - Workspace 'demo': permission=ANALYZE, hierarchy_permission=MANAGE
    - Data source 'demo-test-ds': permission=MANAGE

    IMPORTANT: If this test fails due to missing/incorrect permissions, it may indicate
    that a prior test corrupted the state. See module docstring for details on test
    dependencies and how to restore state.

    When regenerating cassettes, ensure fresh state by running:
        _restore_demo2_permissions(sdk, test_config)
    before this test's assertions.
    """
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    user_id = test_config["test_user"]
    workspace_id = test_config["workspace"]
    workspace_name = test_config["workspace_name"]
    data_source_id = test_config["data_source"]

    permissions = sdk.catalog_user.get_user_permissions(user_id)
    assert len(permissions.workspaces) == 1, (
        f"Expected demo2 to have 1 workspace permission, got {len(permissions.workspaces)}. "
        "This may indicate state corruption from a prior test. "
        "Run _restore_demo2_permissions() to fix."
    )
    assert permissions.workspaces[0].id == workspace_id
    assert permissions.workspaces[0].name == workspace_name
    assert permissions.workspaces[0].permissions == ["ANALYZE"]
    assert permissions.workspaces[0].hierarchy_permissions == ["MANAGE"]

    assert len(permissions.data_sources) == 1, (
        f"Expected demo2 to have 1 data source permission, got {len(permissions.data_sources)}. "
        "This may indicate state corruption from a prior test."
    )
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


@pytest.mark.dependency(name="test_get_user_group_permissions")
@gd_vcr.use_cassette(str(_fixtures_dir / "test_get_user_group_permissions.yaml"))
def test_get_user_group_permissions(test_config):
    """Test retrieving user group permissions.

    This test expects demoGroup to have specific permissions:
    - Workspace 'demo': permission=VIEW, hierarchy_permission=ANALYZE
    - Data source 'demo-test-ds': permission=USE

    See test_get_user_permissions docstring for notes on test dependencies.
    """
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    group_id = test_config["test_user_group"]
    workspace_id = test_config["workspace"]
    workspace_name = test_config["workspace_name"]
    data_source_id = test_config["data_source"]

    permissions = sdk.catalog_user.get_user_group_permissions(group_id)
    assert len(permissions.workspaces) == 1, (
        f"Expected demoGroup to have 1 workspace permission, got {len(permissions.workspaces)}. "
        "This may indicate state corruption from a prior test."
    )
    assert permissions.workspaces[0].id == workspace_id
    assert permissions.workspaces[0].name == workspace_name
    assert permissions.workspaces[0].permissions == ["VIEW"]
    assert permissions.workspaces[0].hierarchy_permissions == ["ANALYZE"]

    assert len(permissions.data_sources) == 1, (
        f"Expected demoGroup to have 1 data source permission, got {len(permissions.data_sources)}. "
        "This may indicate state corruption from a prior test."
    )
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
    """Remove all users except admin, demo, and demo2.

    WARNING: This function intentionally preserves demo2 because:
    1. Deleting demo2 cascade-deletes data source permissions referencing it
    2. Deleting demo2 cascade-deletes workspace permissions referencing it
    3. These cascade deletes break subsequent permission tests (test_get_user_permissions, etc.)

    If you need to delete demo2, ensure you call _restore_demo2_permissions() afterward
    to restore the expected permission state.

    Protected users:
    - admin: System administrator
    - demo: Default demo user
    - demo2: Test user with permission references (test_config["test_user"])
    """
    users = sdk.catalog_user.list_users()
    for user in users:
        if user.id not in ["admin", "demo", "demo2"]:
            sdk.catalog_user.delete_user(user.id)


def _clear_user_groups(sdk: GoodDataSdk) -> None:
    """Remove all user groups except adminGroup and demoGroup.

    WARNING: This function intentionally preserves demoGroup because:
    1. Deleting demoGroup cascade-deletes data source permissions referencing it
    2. Deleting demoGroup cascade-deletes workspace permissions referencing it
    3. These cascade deletes break subsequent permission tests (test_get_user_group_permissions, etc.)

    If you need to delete demoGroup, ensure you call _restore_demo2_permissions() afterward
    to restore the expected permission state.

    Protected user groups:
    - adminGroup: Admin group
    - demoGroup: Test user group with permission references (test_config["test_user_group"])
    """
    sdk.catalog_user.put_declarative_user_groups(
        CatalogDeclarativeUserGroups(
            user_groups=[
                CatalogDeclarativeUserGroup(id="adminGroup"),
                CatalogDeclarativeUserGroup(id="demoGroup"),
            ]
        )
    )


def _verify_demo2_permissions_state(sdk: GoodDataSdk, test_config: dict) -> bool:
    """Verify that demo2 and demoGroup have expected permissions.

    This function can be used to check if permission state is correct before running
    permission-dependent tests.

    Returns:
        True if permissions are in expected state, False otherwise.

    Expected state:
    - demo2 user: workspace=ANALYZE, hierarchy=MANAGE, data_source=MANAGE
    - demoGroup: workspace=VIEW, hierarchy=ANALYZE, data_source=USE
    """
    user_id = test_config["test_user"]
    group_id = test_config["test_user_group"]

    try:
        user_perms = sdk.catalog_user.get_user_permissions(user_id)
        group_perms = sdk.catalog_user.get_user_group_permissions(group_id)

        # Check demo2 permissions
        if len(user_perms.workspaces) != 1 or len(user_perms.data_sources) != 1:
            return False
        if user_perms.workspaces[0].permissions != ["ANALYZE"]:
            return False
        if user_perms.workspaces[0].hierarchy_permissions != ["MANAGE"]:
            return False
        if user_perms.data_sources[0].permissions != ["MANAGE"]:
            return False

        # Check demoGroup permissions
        if len(group_perms.workspaces) != 1 or len(group_perms.data_sources) != 1:
            return False
        if group_perms.workspaces[0].permissions != ["VIEW"]:
            return False
        if group_perms.workspaces[0].hierarchy_permissions != ["ANALYZE"]:
            return False
        return group_perms.data_sources[0].permissions == ["USE"]
    except Exception:
        return False
