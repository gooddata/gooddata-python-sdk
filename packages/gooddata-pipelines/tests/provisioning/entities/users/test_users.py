# (C) 2025 GoodData Corporation

from dataclasses import dataclass
from typing import Any, Optional
from unittest import mock

from gooddata_api_client.exceptions import (  # type: ignore[import]
    NotFoundException,
)
from gooddata_sdk.catalog.user.entity_model.user import CatalogUser
from gooddata_sdk.catalog.user.entity_model.user_group import CatalogUserGroup

from gooddata_pipelines.provisioning.entities.users.models.users import (
    UserIncrementalLoad,
)


@dataclass
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


class MockResponse:
    def __init__(
        self, status_code, json_response: dict[str, Any] = {}, text: str = ""
    ):
        self.status_code = status_code
        self.json_response = json_response
        self.text = text

    def json(self):
        return self.json_response


UPSTREAM_USERS = {
    "jozef.mrkva": MockUser(
        "jozef.mrkva", "jozef", "mrkva", "jozef.mrkva@test.com", "auth_id_1", []
    ),
    "kristian.kalerab": MockUser(
        "kristian.kalerab",
        "kristian",
        "kalerab",
        "kristian.kalerab@test.com",
        "auth_id_5",
        [],
    ),
    "richard.cvikla": MockUser(
        "richard.cvikla", "richard", "cvikla", None, "auth_id_6", []
    ),
    "adam.avokado": MockUser("adam.avokado", None, None, None, "auth_id_7", []),
}

UPSTREAM_UG_ID = "ug_1"
EXPECTED_NEW_UG_OBJ = CatalogUserGroup.init("ug_2", "ug_2")
EXPECTED_GET_IDS = {
    "jozef.mrkva",
    "kristian.kalerab",
    "peter.pertzlen",
    "zoltan.zeler",
}
EXPECTED_CREATE_OR_UPDATE_IDS = {
    "peter.pertzlen",
    "zoltan.zeler",
    "kristian.kalerab",
}


def prepare_sdk():
    def mock_get_user(user_id):
        if user_id not in UPSTREAM_USERS:
            raise NotFoundException
        return UPSTREAM_USERS[user_id].to_sdk()

    def mock_get_user_group(ug_id):
        if ug_id != UPSTREAM_UG_ID:
            raise NotFoundException
        return

    sdk = mock.Mock()
    sdk.catalog_user.get_user.side_effect = mock_get_user
    sdk.catalog_user.get_user_group.side_effect = mock_get_user_group
    return sdk


"""
jozef - No change; user exists
bartolomej - no change; user doesnt exist
peter - create (2 ugs); 1 ug exists, 1 doesnt
zoltan - create (1 ug); ug exists
kristian - update
richard - delete (diff fields than in upstream)
adam - delete (same fields as in upstream)
"""
