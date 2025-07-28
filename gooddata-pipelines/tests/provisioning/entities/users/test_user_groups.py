# (C) 2025 GoodData Corporation

from dataclasses import dataclass
from unittest import mock

import pytest
from gooddata_sdk.catalog.user.entity_model.user_group import CatalogUserGroup

from gooddata_pipelines.provisioning.entities.users.models.user_groups import (
    UserGroupIncrementalLoad,
)

TEST_CSV_PATH = "tests/data/user_group_mgmt/input.csv"


@dataclass
class MockUserGroup:
    id: str
    name: str
    parent_ids: list[str]

    def to_sdk(self):
        return CatalogUserGroup.init(
            user_group_id=self.id,
            user_group_name=self.name,
            user_group_parent_ids=self.parent_ids,
        )


def test_from_csv_row_standard():
    input = [
        {
            "user_group_id": "ug_1",
            "user_group_name": "Admins",
            "parent_user_groups": "ug_2|ug_3",
            "is_active": "True",
        }
    ]
    result = UserGroupIncrementalLoad.from_list_of_dicts(input, "|")
    expected = [
        UserGroupIncrementalLoad(
            user_group_id="ug_1",
            user_group_name="Admins",
            parent_user_groups=["ug_2", "ug_3"],
            is_active=True,
        )
    ]
    assert result == expected, "Standard row should be parsed correctly"


def test_from_csv_row_no_parent_groups():
    input = [
        {
            "user_group_id": "ug_2",
            "user_group_name": "Developers",
            "parent_user_groups": "",
            "is_active": "True",
        }
    ]
    result = UserGroupIncrementalLoad.from_list_of_dicts(input, "|")
    expected = [
        UserGroupIncrementalLoad(
            user_group_id="ug_2",
            user_group_name="Developers",
            parent_user_groups=[],
            is_active=True,
        )
    ]
    assert result == expected, (
        "Row without parent user groups should be parsed correctly"
    )


def test_from_csv_row_fallback_name():
    input = [
        {
            "user_group_id": "ug_3",
            "user_group_name": "",
            "parent_user_groups": "",
            "is_active": "False",
        }
    ]
    result = UserGroupIncrementalLoad.from_list_of_dicts(input, "|")
    expected = [
        UserGroupIncrementalLoad(
            user_group_id="ug_3",
            user_group_name="ug_3",
            parent_user_groups=[],
            is_active=False,
        )
    ]
    assert result == expected, (
        "Row with empty name should fallback to user group ID"
    )


def test_from_csv_row_invalid_is_active():
    input = [
        {
            "user_group_id": "ug_4",
            "user_group_name": "Testers",
            "parent_user_groups": "ug_1",
            "is_active": "not_a_boolean",
        }
    ]
    with pytest.raises(ValueError):
        UserGroupIncrementalLoad.from_list_of_dicts(input, "|")


def prepare_sdk():
    def mock_list_user_groups():
        return [
            MockUserGroup("ug_1", "Admins", []).to_sdk(),
            MockUserGroup("ug_4", "TemporaryAccess", ["ug_2"]).to_sdk(),
        ]

    sdk = mock.Mock()
    sdk.catalog_user.list_user_groups = mock_list_user_groups
    return sdk
