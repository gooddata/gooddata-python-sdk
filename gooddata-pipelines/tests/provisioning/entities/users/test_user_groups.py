# (C) 2025 GoodData Corporation


import pytest

from gooddata_pipelines.provisioning.entities.users.models.user_groups import (
    UserGroupIncrementalLoad,
)


def test_missing_key_no_parent_groups() -> None:
    result = UserGroupIncrementalLoad(
        user_group_id="ug_2", user_group_name="Developers", is_active=True
    )
    expected = UserGroupIncrementalLoad(
        user_group_id="ug_2",
        user_group_name="Developers",
        parent_user_groups=[],
        is_active=True,
    )

    assert result == expected, (
        "Row without parent user groups should be parsed correctly"
    )


@pytest.mark.parametrize("invalid_name", [None, ""])
def test_fallback_name(invalid_name) -> None:
    result = UserGroupIncrementalLoad(
        user_group_id="ug_3",
        user_group_name=invalid_name,
        parent_user_groups=[],
        is_active=False,
    )
    expected = UserGroupIncrementalLoad(
        user_group_id="ug_3",
        user_group_name="ug_3",
        parent_user_groups=[],
        is_active=False,
    )

    assert result == expected, (
        "Row with empty name should fallback to user group ID"
    )


@pytest.mark.parametrize("empty_parent_groups", [None, "", []])
def test_no_parent_user_groups(empty_parent_groups) -> None:
    result = UserGroupIncrementalLoad(
        user_group_id="ug_3",
        user_group_name="ug_3",
        parent_user_groups=empty_parent_groups,
        is_active=False,
    )
    expected = UserGroupIncrementalLoad(
        user_group_id="ug_3",
        user_group_name="ug_3",
        parent_user_groups=[],
        is_active=False,
    )

    assert result == expected, (
        "Row with empty parent user groups should be parsed correctly"
    )


def test_row_invalid_is_active() -> None:
    with pytest.raises(ValueError):
        UserGroupIncrementalLoad(
            user_group_id="ug_4",
            user_group_name="Testers",
            parent_user_groups=[],
            is_active="not_a_boolean",  # type: ignore
        )
