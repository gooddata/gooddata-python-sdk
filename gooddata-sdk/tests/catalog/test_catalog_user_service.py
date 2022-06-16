# (C) 2022 GoodData Corporation
from __future__ import annotations

import json
from pathlib import Path

import vcr

import gooddata_metadata_client.apis as metadata_apis
from gooddata_sdk import GoodDataApiClient, GoodDataSdk
from gooddata_sdk.catalog.user.declarative_model.user_group import (
    CatalogDeclarativeUserGroup,
    CatalogDeclarativeUserGroups,
)
from gooddata_sdk.utils import create_directory
from tests import VCR_MATCH_ON

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures" / "users"

gd_vcr = vcr.VCR(filter_headers=["authorization", "user-agent"], serializer="json", match_on=VCR_MATCH_ON)


# ENTITY USERS


@gd_vcr.use_cassette(str(_fixtures_dir / "list_users.json"))
def test_list_users(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    users = sdk.catalog_user.list_users()
    assert len(users) == 3
    assert set(user.id for user in users) == {"demo2", "admin", "demo"}


@gd_vcr.use_cassette(str(_fixtures_dir / "get_user.json"))
def test_get_user(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    user = sdk.catalog_user.get_user(test_config["test_user"])
    assert user.id == test_config["test_user"]
    assert user.get_user_groups == [test_config["test_user_group"]]


@gd_vcr.use_cassette(str(_fixtures_dir / "create_delete_user.json"))
def test_create_delete_user(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    user_id = test_config["test_new_user"]
    authentication_id = f"{user_id}_auth_id"
    user_groups = [test_config["test_user_group"]]

    try:
        assert len(sdk.catalog_user.list_users()) == 3
        sdk.catalog_user.create_or_update_user(
            user_id=user_id, authentication_id=authentication_id, user_groups=user_groups
        )
        user = sdk.catalog_user.get_user(user_id)
        assert len(sdk.catalog_user.list_users()) == 4
        assert user.id == user_id
        assert user.get_user_groups == user_groups
        assert user.attributes.authentication_id == authentication_id
    finally:
        sdk.catalog_user.delete_user(user_id)
        assert len(sdk.catalog_user.list_users()) == 3


@gd_vcr.use_cassette(str(_fixtures_dir / "update_user.json"))
def test_update_user(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    user_id = test_config["test_user"]
    user = sdk.catalog_user.get_user(user_id)
    new_auth_id = f"{user_id}_123"
    new_user_groups = ["demoGroup", "visitorsGroup"]
    try:
        sdk.catalog_user.create_or_update_user(user_id, new_auth_id, new_user_groups)
        updated_user = sdk.catalog_user.get_user(user_id)
        assert updated_user.attributes.authentication_id == new_auth_id
        assert len(updated_user.get_user_groups) == len(new_user_groups)
        assert set(updated_user.get_user_groups) == set(new_user_groups)

    finally:
        sdk.catalog_user.delete_user(user_id)
        sdk.catalog_user.create_or_update_user(user.id, user.attributes.authentication_id, user.get_user_groups)
        assert len(sdk.catalog_user.list_users()) == 3


# ENTITY USER GROUPS


@gd_vcr.use_cassette(str(_fixtures_dir / "list_user_groups.json"))
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


@gd_vcr.use_cassette(str(_fixtures_dir / "get_user_group.json"))
def test_get_user_group(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    user_group = sdk.catalog_user.get_user_group(test_config["test_user_group"])
    assert user_group.id == test_config["test_user_group"]


@gd_vcr.use_cassette(str(_fixtures_dir / "create_delete_user_group.json"))
def test_create_delete_user_group(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    user_group_id = test_config["test_new_user_group"]
    user_group_parents_id = [test_config["test_user_group"]]

    try:
        assert len(sdk.catalog_user.list_user_groups()) == 4
        sdk.catalog_user.create_or_update_user_group(
            user_group_id=user_group_id, user_group_parents_id=user_group_parents_id
        )
        user_group = sdk.catalog_user.get_user_group(user_group_id)
        assert len(sdk.catalog_user.list_user_groups()) == 5
        assert user_group.id == user_group_id
        assert [p.id for p in user_group.relationships.parents.data] == user_group_parents_id
    finally:
        sdk.catalog_user.delete_user_group(user_group_id)
        assert len(sdk.catalog_user.list_user_groups()) == 4


@gd_vcr.use_cassette(str(_fixtures_dir / "update_user_group.json"))
def test_update_user_group(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    user_group_id = test_config["test_user_group"]
    user_group = sdk.catalog_user.get_user_group(user_group_id)
    user_group_parent_ids = []

    try:
        sdk.catalog_user.create_or_update_user_group(user_group_id, user_group_parent_ids)
        updated_user_group = sdk.catalog_user.get_user_group(user_group_id)
        assert user_group.id == updated_user_group.id
        assert len(updated_user_group.get_parents) == len(user_group_parent_ids)
        assert set(updated_user_group.get_parents) == set(user_group_parent_ids)
    finally:
        sdk.catalog_user.delete_user(user_group_id)
        sdk.catalog_user.create_or_update_user_group(user_group_id, user_group.get_parents)
        assert len(sdk.catalog_user.list_user_groups()) == 4


# DECLARATIVE USERS


@gd_vcr.use_cassette(str(_fixtures_dir / "get_declarative_users.json"))
def test_get_declarative_users(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    client = GoodDataApiClient(host=test_config["host"], token=test_config["token"])
    layout_api = metadata_apis.LayoutApi(client.metadata_client)

    users = sdk.catalog_user.get_declarative_users()

    assert len(users.users) == 3
    assert [user.id for user in users.users] == ["admin", "demo", "demo2"]
    assert users.to_dict(camel_case=True) == layout_api.get_users_layout().to_dict(camel_case=True)


@gd_vcr.use_cassette(str(_fixtures_dir / "store_declarative_users.json"))
def test_store_declarative_users(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "store"
    create_directory(path)

    users_e = sdk.catalog_user.get_declarative_users()
    sdk.catalog_user.store_declarative_users(path)
    users_o = sdk.catalog_user.load_declarative_users(path)

    assert users_e == users_o
    assert users_e.to_dict(camel_case=True) == users_o.to_dict(camel_case=True)


@gd_vcr.use_cassette(str(_fixtures_dir / "put_declarative_users.json"))
def test_put_declarative_users(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    users_e = sdk.catalog_user.get_declarative_users()

    try:
        _clear_users(sdk)

        sdk.catalog_user.put_declarative_users(users_e)
        users_o = sdk.catalog_user.get_declarative_users()
        assert users_e == users_o
        assert users_e.to_dict(camel_case=True) == users_o.to_dict(camel_case=True)
    finally:
        sdk.catalog_user.put_declarative_users(users_e)


@gd_vcr.use_cassette(str(_fixtures_dir / "load_and_put_declarative_users.json"))
def test_load_and_put_declarative_users(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "load"
    users_e = sdk.catalog_user.get_declarative_users()

    try:
        _clear_users(sdk)

        sdk.catalog_user.load_and_put_declarative_users(path)
        users_o = sdk.catalog_user.get_declarative_users()
        assert set(user.id for user in users_e.users) == set(user.id for user in users_o.users)
        assert [user.user_groups for user in users_e.users] == [user.user_groups for user in users_o.users]
    finally:
        sdk.catalog_user.put_declarative_users(users_e)


# DECLARATIVE USER GROUPS


@gd_vcr.use_cassette(str(_fixtures_dir / "get_declarative_user_groups.json"))
def test_get_declarative_user_groups(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    client = GoodDataApiClient(host=test_config["host"], token=test_config["token"])
    layout_api = metadata_apis.LayoutApi(client.metadata_client)

    user_groups = sdk.catalog_user.get_declarative_user_groups()

    assert len(user_groups.user_groups) == 4
    assert set(user_group.id for user_group in user_groups.user_groups) == {
        "adminGroup",
        "demoGroup",
        "adminQA1Group",
        "visitorsGroup",
    }
    assert user_groups.to_dict(camel_case=True) == layout_api.get_user_groups_layout().to_dict(camel_case=True)


@gd_vcr.use_cassette(str(_fixtures_dir / "store_declarative_user_groups.json"))
def test_store_declarative_user_groups(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "store"
    create_directory(path)

    user_groups_e = sdk.catalog_user.get_declarative_user_groups()
    sdk.catalog_user.store_declarative_user_groups(path)
    user_groups_o = sdk.catalog_user.load_declarative_user_groups(path)

    assert user_groups_e == user_groups_o
    assert user_groups_e.to_dict(camel_case=True) == user_groups_o.to_dict(camel_case=True)


@gd_vcr.use_cassette(str(_fixtures_dir / "put_declarative_user_groups.json"))
def test_put_declarative_user_groups(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    user_groups_path = _current_dir / "expected" / "declarative_user_groups.json"
    user_groups_e = sdk.catalog_user.get_declarative_user_groups()
    users_e = sdk.catalog_user.get_declarative_users()

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


@gd_vcr.use_cassette(str(_fixtures_dir / "load_and_put_declarative_user_groups.json"))
def test_load_and_put_declarative_user_groups(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "load"
    expected_json_path = _current_dir / "expected" / "declarative_user_groups.json"
    users_e = sdk.catalog_user.get_declarative_users()
    user_groups_e = sdk.catalog_user.get_declarative_user_groups()

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


# Help functions


def _clear_users(sdk: GoodDataSdk) -> None:
    users = sdk.catalog_user.list_users()
    for user in users:
        if user.id not in ["admin", "demo"]:
            sdk.catalog_user.delete_user(user.id)


def _clear_user_groups(sdk: GoodDataSdk) -> None:
    sdk.catalog_user.put_declarative_user_groups(
        CatalogDeclarativeUserGroups(user_groups=[CatalogDeclarativeUserGroup(id="adminGroup")])
    )
