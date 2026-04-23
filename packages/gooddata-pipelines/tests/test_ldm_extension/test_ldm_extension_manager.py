# (C) 2025 GoodData Corporation
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.dataset.dataset import (
    CatalogDeclarativeDataset,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.ldm import (
    CatalogDeclarativeLdm,
    CatalogDeclarativeModel,
)

from gooddata_pipelines.ldm_extension.input_processor import (
    LdmExtensionDataProcessor,
)
from gooddata_pipelines.ldm_extension.input_validator import (
    LdmExtensionDataValidator,
)
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

    manager._process_with_relations_check(validated_data)
    manager._sdk.catalog_workspace_content.put_declarative_ldm.assert_called_once()
    manager._sdk.catalog_workspace.put_declarative_workspace.assert_not_called()


def test_relations_check_failure_and_revert(
    manager, validated_data, capsys, mocker: MockerFixture
):
    """Relation check fails, workspace layout is reverted."""
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


def _bare_manager(sdk_mock: MagicMock) -> LdmExtensionManager:
    """Build a manager with a real ``LdmExtensionDataProcessor`` and a mocked SDK.

    Used by tests that assert the real merge/payload logic end-to-end. Tests that
    only need to check dispatch or logging use the ``manager`` fixture above,
    which mocks the processor as well.
    """
    bare = object.__new__(LdmExtensionManager)
    bare._processor = LdmExtensionDataProcessor()
    bare._validator = LdmExtensionDataValidator()
    bare._sdk = sdk_mock
    bare.logger = MagicMock()
    return bare


def test_ldm_payload_without_merge_returns_fragment_only(mock_custom_dataset):
    sdk_mock = MagicMock()
    bare = _bare_manager(sdk_mock)

    payload = bare._ldm_payload_for_workspace(
        "workspace1",
        {"ds1": mock_custom_dataset},
        merge_into_existing_ldm=False,
        remove_managed_datasets_missing_from_input=False,
        management_tag=None,
    )

    sdk_mock.catalog_workspace_content.get_declarative_ldm.assert_not_called()
    assert payload.ldm is not None
    assert [d.id for d in payload.ldm.datasets] == ["ds1"]


def test_ldm_payload_merges_with_existing_ldm(mock_custom_dataset):
    inherited = CatalogDeclarativeDataset(
        id="parent_only",
        title="Parent",
        grain=[],
        references=[],
    )
    existing = CatalogDeclarativeModel(
        ldm=CatalogDeclarativeLdm(datasets=[inherited], date_instances=[])
    )
    sdk_mock = MagicMock()
    sdk_mock.catalog_workspace_content.get_declarative_ldm.return_value = (
        existing
    )
    bare = _bare_manager(sdk_mock)

    payload = bare._ldm_payload_for_workspace(
        "workspace1",
        {"ds1": mock_custom_dataset},
        merge_into_existing_ldm=True,
        remove_managed_datasets_missing_from_input=False,
        management_tag=None,
    )

    sdk_mock.catalog_workspace_content.get_declarative_ldm.assert_called_once_with(
        "workspace1"
    )
    assert payload.ldm is not None
    assert {d.id for d in payload.ldm.datasets} == {"parent_only", "ds1"}


def test_ldm_payload_merge_forwards_cleanup_flags(mock_custom_dataset):
    managed_old = CatalogDeclarativeDataset(
        id="managed_old",
        title="Old",
        grain=[],
        references=[],
        tags=["bca_tooling_managed"],
    )
    existing = CatalogDeclarativeModel(
        ldm=CatalogDeclarativeLdm(datasets=[managed_old], date_instances=[])
    )
    sdk_mock = MagicMock()
    sdk_mock.catalog_workspace_content.get_declarative_ldm.return_value = (
        existing
    )
    bare = _bare_manager(sdk_mock)

    payload = bare._ldm_payload_for_workspace(
        "workspace1",
        {"ds1": mock_custom_dataset},
        merge_into_existing_ldm=True,
        remove_managed_datasets_missing_from_input=True,
        management_tag="bca_tooling_managed",
    )

    assert payload.ldm is not None
    assert [d.id for d in payload.ldm.datasets] == ["ds1"]


def test_process_without_relations_check_forwards_merge_kwargs(
    mock_custom_dataset,
):
    existing = CatalogDeclarativeModel(
        ldm=CatalogDeclarativeLdm(datasets=[], date_instances=[])
    )
    sdk_mock = MagicMock()
    sdk_mock.catalog_workspace_content.get_declarative_ldm.return_value = (
        existing
    )
    bare = _bare_manager(sdk_mock)

    bare._process_without_relations_check(
        {"workspace1": {"ds1": mock_custom_dataset}},
        merge_into_existing_ldm=True,
        remove_managed_datasets_missing_from_input=False,
        management_tag=None,
    )

    sdk_mock.catalog_workspace_content.get_declarative_ldm.assert_called_once_with(
        "workspace1"
    )
    put_call = sdk_mock.catalog_workspace_content.put_declarative_ldm
    put_call.assert_called_once()
    kwargs = put_call.call_args.kwargs
    assert kwargs["workspace_id"] == "workspace1"
    assert [d.id for d in kwargs["ldm"].ldm.datasets] == ["ds1"]


def test_process_with_relations_check_happy_path(mock_custom_dataset):
    sdk_mock = MagicMock()
    bare = _bare_manager(sdk_mock)
    bare._get_objects_with_invalid_relations = MagicMock(return_value=[])

    bare._process_with_relations_check(
        {"workspace1": {"ds1": mock_custom_dataset}},
        merge_into_existing_ldm=False,
        remove_managed_datasets_missing_from_input=False,
        management_tag=None,
    )

    sdk_mock.catalog_workspace.get_declarative_workspace.assert_called_once_with(
        "workspace1"
    )
    put_call = sdk_mock.catalog_workspace_content.put_declarative_ldm
    put_call.assert_called_once()
    assert put_call.call_args.kwargs["workspace_id"] == "workspace1"
    sdk_mock.catalog_workspace.put_declarative_workspace.assert_not_called()


def test_process_dispatches_with_relations_check_by_default():
    sdk_mock = MagicMock()
    bare = _bare_manager(sdk_mock)
    bare._validator = MagicMock()
    bare._validator.validate.return_value = {"workspace1": {}}
    bare._process_with_relations_check = MagicMock()
    bare._process_without_relations_check = MagicMock()

    bare.process(
        custom_datasets=[],
        custom_fields=[],
        merge_into_existing_ldm=True,
        remove_managed_datasets_missing_from_input=True,
        management_tag="bca_tooling_managed",
    )

    bare._process_with_relations_check.assert_called_once_with(
        {"workspace1": {}},
        merge_into_existing_ldm=True,
        remove_managed_datasets_missing_from_input=True,
        management_tag="bca_tooling_managed",
    )
    bare._process_without_relations_check.assert_not_called()


def test_process_skips_relations_check_when_flag_is_false():
    sdk_mock = MagicMock()
    bare = _bare_manager(sdk_mock)
    bare._validator = MagicMock()
    bare._validator.validate.return_value = {"workspace1": {}}
    bare._process_with_relations_check = MagicMock()
    bare._process_without_relations_check = MagicMock()

    bare.process(
        custom_datasets=[],
        custom_fields=[],
        check_relations=False,
    )

    bare._process_without_relations_check.assert_called_once_with(
        {"workspace1": {}},
        merge_into_existing_ldm=False,
        remove_managed_datasets_missing_from_input=False,
        management_tag=None,
    )
    bare._process_with_relations_check.assert_not_called()
