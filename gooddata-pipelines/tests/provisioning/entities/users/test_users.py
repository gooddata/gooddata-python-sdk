# (C) 2025 GoodData Corporation
from typing import Literal, Optional

import attrs
import orjson
import pytest
from gooddata_api_client.exceptions import NotFoundException  # type: ignore
from gooddata_sdk.catalog.user.entity_model.user import (
    CatalogUser,
    CatalogUserAttributes,
    CatalogUserGroupsData,
    CatalogUserRelationships,
)
from gooddata_sdk.catalog.user.entity_model.user_group import (
    CatalogUserGroup,
)
from pytest_mock import MockerFixture
from requests import Response

from gooddata_pipelines.provisioning.entities.users.models.users import (
    UserFullLoad,
    UserIncrementalLoad,
)
from gooddata_pipelines.provisioning.entities.users.users import (
    UserProvisioner,
)
from tests.conftest import TEST_DATA_DIR

TEST_DATA_SUBDIR = f"{TEST_DATA_DIR}/provisioning/entities/users"


@attrs.define
class MockUser:
    id: str
    firstname: Optional[str]
    lastname: Optional[str]
    email: Optional[str]
    authenticationId: Optional[str]
    user_groups: list[str]

    def to_sdk(self):
        return CatalogUser.init(
            user_id=self.id,
            firstname=self.firstname,
            lastname=self.lastname,
            email=self.email,
            authentication_id=self.authenticationId,
            user_group_ids=self.user_groups,
        )

    def to_json(self):
        attrs = {}
        if self.authenticationId:
            attrs["authenticationId"] = self.authenticationId
        if self.firstname:
            attrs["firstname"] = self.firstname
        if self.lastname:
            attrs["lastname"] = self.lastname
        if self.email:
            attrs["email"] = self.email

        data = {
            "id": self.id,
            "type": "user",
            "attributes": attrs,
        }

        if not self.user_groups:
            return data

        relsdata = [
            {"id": group, "type": "userGroup"} for group in self.user_groups
        ]
        if relsdata:
            data["relationships"] = {"userGroups": {"data": relsdata}}
        return data


def test_user_obj_from_sdk():
    user_input = MockUser(
        "some.user", "some", "user", "some@email.com", "auth", ["ug"]
    )
    excepted = UserIncrementalLoad(
        user_id="some.user",
        firstname="some",
        lastname="user",
        email="some@email.com",
        auth_id="auth",
        user_groups=["ug"],
        is_active=True,
    )
    user = UserIncrementalLoad.from_sdk_obj(user_input.to_sdk())
    assert excepted == user


def test_user_obj_from_sdk_no_ugs():
    user_input = MockUser(
        "some.user", "some", "user", "some@email.com", "auth", []
    )
    excepted = UserIncrementalLoad(
        user_id="some.user",
        firstname="some",
        lastname="user",
        email="some@email.com",
        auth_id="auth",
        user_groups=[],
        is_active=True,
    )
    user = UserIncrementalLoad.from_sdk_obj(user_input.to_sdk())
    assert excepted == user


def test_user_obj_to_sdk():
    user_input = MockUser(
        "some.user", "some", "user", "some@email.com", "auth", ["ug"]
    )
    user = UserIncrementalLoad(
        user_id="some.user",
        firstname="some",
        lastname="user",
        email="some@email.com",
        auth_id="auth",
        user_groups=["ug"],
        is_active=True,
    )
    excepted = user_input.to_sdk()
    assert excepted == user.to_sdk_obj()


def test_user_obj_to_sdk_no_ugs():
    user_input = MockUser(
        "some.user", "some", "user", "some@email.com", "auth", []
    )
    user = UserIncrementalLoad(
        user_id="some.user",
        firstname="some",
        lastname="user",
        email="some@email.com",
        auth_id="auth",
        user_groups=[],
        is_active=True,
    )
    excepted = user_input.to_sdk()
    assert excepted == user.to_sdk_obj()


@pytest.fixture
def user_provisioner(mocker: MockerFixture) -> UserProvisioner:
    """Mock instance of UserProvisioner."""
    provisioner_instance = UserProvisioner.create(
        host="https://localhost:3000", token="token"
    )

    # Patch the API
    mocker.patch.object(provisioner_instance, "_api", return_value=None)

    return provisioner_instance


def parse_user_data(user_data: list[dict]) -> list[CatalogUser]:
    """Parse json user metadata to CatalogUser objects."""
    users: list[CatalogUser] = []
    for user in user_data:
        users.append(
            CatalogUser(
                id=user["user_id"],
                attributes=CatalogUserAttributes(
                    firstname=user["firstname"],
                    lastname=user["lastname"],
                    email=user["email"],
                    authentication_id=user["authentication_id"],
                ),
                relationships=CatalogUserRelationships(
                    user_groups=CatalogUserGroupsData(
                        data=[
                            CatalogUserGroup(id=group)
                            for group in user["user_groups"]
                        ]
                    )
                ),
            )
        )
    return sorted(users, key=lambda x: x.id)


@pytest.mark.parametrize(
    ("input_path", "expected_path", "load_method"),
    [
        (
            "users_input_full_load.json",
            "users_expected_full_load.json",
            "full_load",
        ),
        (
            "users_input_incremental_load.json",
            "users_expected_incremental_load.json",
            "incremental_load",
        ),
        (
            "users_input_full_load_modifies_protected_user.json",
            "users_expected_full_load.json",
            "full_load",
        ),
        (
            "users_input_incremental_load_modifies_protected_user.json",
            "users_expected_incremental_load.json",
            "incremental_load",
        ),
        (
            "users_input_incremental_load_deletes_protected_user.json",
            "users_expected_incremental_load.json",
            "incremental_load",
        ),
    ],
)
def test_user_provisioning(
    input_path: str,
    expected_path: str,
    load_method: Literal["full_load", "incremental_load"],
    user_provisioner: UserProvisioner,
    mocker: MockerFixture,
):
    """Test complete user provisioning workflow by checking that the script will
    attempt to create, update or delete expected users for given input."""

    # Load input data
    with open(f"{TEST_DATA_SUBDIR}/{input_path}", "r") as f:
        input_data = orjson.loads(f.read())

    # Load expected data
    with open(f"{TEST_DATA_SUBDIR}/{expected_path}", "r") as f:
        raw_expected_data = orjson.loads(f.read())

    # Load and patch "existing users"
    with open(f"{TEST_DATA_SUBDIR}/existing_upstream_users.json", "r") as f:
        raw_upstream_users = orjson.loads(f.read())

    upstream_users = parse_user_data(raw_upstream_users)

    mocker.patch.object(
        user_provisioner._api,
        "list_users",
        return_value=upstream_users,
    )

    def mock_get_profile(*args, **kwargs) -> Response:
        """Mock the get_profile method by creating a response object with sample
        response from the API reference.
        """
        with open(
            f"{TEST_DATA_SUBDIR}/profile_response_content.json", "r"
        ) as f:
            profile_response = f.read()
        response = Response()
        response.status_code = 200
        response._content = profile_response.encode("utf-8")
        response.headers["Content-Type"] = "application/json"
        return response

    mocker.patch.object(
        user_provisioner._api,
        "get_profile",
        side_effect=mock_get_profile,
    )

    upstream_user_cache = {user.id: user for user in upstream_users}

    def patch_get_user(user_id: str):
        if user_id in upstream_user_cache:
            return upstream_user_cache[user_id]
        raise NotFoundException(f"User {user_id} not found")

    mocker.patch.object(
        user_provisioner._api._sdk.catalog_user,
        "get_user",
        side_effect=patch_get_user,
    )

    # Parse expected data
    expected_deleted_users = sorted(raw_expected_data["deleted_users"])
    raw_expected_modified_users = raw_expected_data["modified_users"]

    expected_modified_users = parse_user_data(raw_expected_modified_users)

    # Patch the API methods to store which users were modified or deleted
    created_or_updated_users: list[CatalogUser] = []
    deleted_users: list[str] = []

    def patch_create_or_update_user(user: CatalogUser, *args, **kwargs):
        created_or_updated_users.append(user)

    def patch_delete_user(user_id: str, *args, **kwargs):
        deleted_users.append(user_id)

    mocker.patch.object(
        user_provisioner._api,
        "create_or_update_user",
        side_effect=patch_create_or_update_user,
    )
    mocker.patch.object(
        user_provisioner._api,
        "delete_user",
        side_effect=patch_delete_user,
    )

    # Run the provisioning
    if load_method == "incremental_load":
        incremental_load_data = [
            UserIncrementalLoad(**row) for row in input_data
        ]
        user_provisioner.incremental_load(incremental_load_data)
    else:
        full_load_data = [UserFullLoad(**row) for row in input_data]
        user_provisioner.full_load(full_load_data)

    # Compare list lengths
    assert len(created_or_updated_users) == len(expected_modified_users)
    assert len(deleted_users) == len(expected_deleted_users)

    # Sort the actual data
    created_or_updated_users = sorted(
        created_or_updated_users, key=lambda x: x.id
    )
    deleted_users = sorted(deleted_users)

    # Compare the actual data
    assert deleted_users == expected_deleted_users
    assert created_or_updated_users == expected_modified_users
