# (C) 2025 GoodData Corporation
import pytest
from pytest_mock import MockerFixture

from gooddata_pipelines.ldm_extension.ldm_extension_manager import (
    LdmExtensionManager,
)
from gooddata_pipelines.ldm_extension.models.analytical_object import (
    AnalyticalObject,
    Attributes,
)


@pytest.fixture
def manager(mocker: MockerFixture, mock_logger):
    custom_fields_manager = LdmExtensionManager(host="host", token="token")

    mocker.patch.object(custom_fields_manager, "_validator")
    mocker.patch.object(custom_fields_manager, "_processor")
    mocker.patch.object(custom_fields_manager, "_sdk")
    mocker.patch.object(custom_fields_manager, "_api")

    custom_fields_manager.logger.subscribe(mock_logger)

    return custom_fields_manager


@pytest.fixture
def validated_data(mocker: MockerFixture):
    # Minimal valid structure for validated_data
    return {"workspace_1": {"dataset_1": mocker.MagicMock()}}


def make_analytical_object(
    id, title="Title", type="type", are_relations_valid=True
):
    obj = AnalyticalObject(
        id=id,
        type=type,
        attributes=Attributes(
            title=title, areRelationsValid=are_relations_valid
        ),
    )
    return obj


def test_relations_check_success(
    manager, validated_data, mocker: MockerFixture
):
    """Relation check passes, workspace layout not reverted."""
    # Setup mocks
    mocker.patch.object(
        manager._sdk.catalog_workspace,
        "get_declarative_workspace",
        return_value=mocker.MagicMock(
            json=mocker.MagicMock(return_value="layout_json")
        ),
    )
    mocker.patch.object(
        manager,
        "_get_analytical_objects",
        side_effect=[
            [make_analytical_object("a", "A")],  # current
            [make_analytical_object("a", "A")],  # new
        ],
    )
    mocker.patch.object(
        manager,
        "_get_objects_with_invalid_relations",
        side_effect=[
            set(),  # current_invalid_relations
            set(),  # new_invalid_relations
        ],
    )
    mocker.patch.object(
        manager._processor, "datasets_to_ldm", return_value="ldm"
    )
    mocker.patch.object(
        manager._sdk.catalog_workspace_content, "put_declarative_ldm"
    )
    mocker.patch.object(
        manager, "_new_ldm_does_not_invalidate_relations", return_value=True
    )
    mocker.patch.object(
        manager._sdk.catalog_workspace, "put_declarative_workspace"
    )

    # Should print "Workspace workspace_1 LDM updated." and not revert
    manager._process_with_relations_check(validated_data)
    manager._sdk.catalog_workspace_content.put_declarative_ldm.assert_called_once()
    manager._sdk.catalog_workspace.put_declarative_workspace.assert_not_called()


def test_relations_check_failure_and_revert(
    manager, validated_data, capsys, mocker: MockerFixture
):
    """Relation check fails, workspace layout is reverted."""
    # Setup mocks
    mocker.patch.object(manager._api, "get_workspace_layout")
    obj1 = make_analytical_object("a", "A", "type", False)
    obj2 = make_analytical_object("b", "B", "type", False)
    mocker.patch.object(
        manager,
        "_get_objects_with_invalid_relations",
        side_effect=[
            [obj1],  # current_invalid_relations
            [obj1, obj2],  # new_invalid_relations (one more invalid)
        ],
    )
    mocker.patch.object(
        manager._processor, "datasets_to_ldm", return_value="ldm"
    )
    mocker.patch.object(
        manager._sdk.catalog_workspace_content, "put_declarative_ldm"
    )
    mocker.patch.object(
        manager, "_new_ldm_does_not_invalidate_relations", return_value=False
    )
    mocker.patch.object(
        manager._sdk.catalog_workspace, "put_declarative_workspace"
    )

    manager._process_with_relations_check(validated_data)

    # Should revert and print info about invalid relations
    manager._sdk.catalog_workspace.put_declarative_workspace.assert_called_once()
    out = capsys.readouterr().out
    assert (
        "Difference in invalid relations found in workspace workspace_1." in out
    )
    assert "b (type) B" in out
    assert "Reverting the workspace layout to the original state." in out


def test_relations_check_fewer_invalid_relations(
    manager, validated_data, mocker: MockerFixture
):
    """Fewer invalid relations after LDM update, no revert needed."""
    # Setup mocks
    obj1 = make_analytical_object("a", "A", "type", False)
    mocker.patch.object(
        manager._sdk.catalog_workspace,
        "get_declarative_workspace",
        return_value=mocker.MagicMock(
            json=mocker.MagicMock(return_value="layout_json")
        ),
    )
    mocker.patch.object(
        manager,
        "_get_objects_with_invalid_relations",
        side_effect=[
            [
                obj1,
                make_analytical_object("b", "B", "type", False),
            ],  # current_invalid_relations
            [obj1],  # new_invalid_relations (fewer)
        ],
    )
    mocker.patch.object(
        manager._processor, "datasets_to_ldm", return_value="ldm"
    )
    mocker.patch.object(
        manager._sdk.catalog_workspace_content, "put_declarative_ldm"
    )
    mocker.patch.object(
        manager, "_new_ldm_does_not_invalidate_relations", return_value=True
    )
    mocker.patch.object(
        manager._sdk.catalog_workspace, "put_declarative_workspace"
    )

    manager._process_with_relations_check(validated_data)
    manager._sdk.catalog_workspace.put_declarative_workspace.assert_not_called()


def test_log_diff_invalid_relations(manager, capsys):
    """Log diff invalid relations."""
    manager._log_diff_invalid_relations(
        [
            make_analytical_object("a", "A", "type", False),
            make_analytical_object("c", "C", "type", False),
        ],
        [
            make_analytical_object("b", "B", "type", False),
            make_analytical_object("c", "C", "type", False),
            make_analytical_object("d", "D", "type", False),
        ],
    )

    captured_output = capsys.readouterr().out

    assert "b (type) B" in captured_output
    assert "d (type) D" in captured_output
    assert "c (type) C" not in captured_output
