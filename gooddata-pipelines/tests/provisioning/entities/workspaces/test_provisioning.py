# (C) 2025 GoodData Corporation

from gooddata_pipelines import WorkspaceProvisioner
from gooddata_pipelines.provisioning.provisioning import Provisioning


def test_create_groups_base_case(
    workspace_provisioner: WorkspaceProvisioner,
) -> None:
    provisioner: Provisioning = workspace_provisioner
    test_source_ids = {"source_id_1", "source_id_2", "source_id_3"}
    test_panther_ids = {"source_id_2", "source_id_3", "source_id_4"}

    id_groups = provisioner._create_groups(test_source_ids, test_panther_ids)

    assert id_groups.ids_in_both_systems == {"source_id_2", "source_id_3"}
    assert id_groups.ids_to_delete == {"source_id_4"}
    assert id_groups.ids_to_create == {"source_id_1"}


def test_create_groups_empty_sets(
    workspace_provisioner: WorkspaceProvisioner,
) -> None:
    provisioner: Provisioning = workspace_provisioner
    test_source_ids: set[str] = set()
    test_panther_ids: set[str] = set()

    id_groups = provisioner._create_groups(test_source_ids, test_panther_ids)

    assert id_groups.ids_in_both_systems == set()
    assert id_groups.ids_to_delete == set()
    assert id_groups.ids_to_create == set()


def test_create_groups_no_overlap(
    workspace_provisioner: WorkspaceProvisioner,
) -> None:
    provisioner: Provisioning = workspace_provisioner
    test_source_ids = {"source_id_1", "source_id_2"}
    test_panther_ids = {"source_id_3", "source_id_4"}

    id_groups = provisioner._create_groups(test_source_ids, test_panther_ids)

    assert id_groups.ids_in_both_systems == set()
    assert id_groups.ids_to_delete == {"source_id_3", "source_id_4"}
    assert id_groups.ids_to_create == {"source_id_1", "source_id_2"}


def test_create_groups_full_overlap(
    workspace_provisioner: WorkspaceProvisioner,
) -> None:
    provisioner: Provisioning = workspace_provisioner
    test_source_ids = {"source_id_1", "source_id_2"}
    test_panther_ids = {"source_id_1", "source_id_2"}

    id_groups = provisioner._create_groups(test_source_ids, test_panther_ids)

    assert id_groups.ids_in_both_systems == {"source_id_1", "source_id_2"}
    assert id_groups.ids_to_delete == set()
    assert id_groups.ids_to_create == set()
