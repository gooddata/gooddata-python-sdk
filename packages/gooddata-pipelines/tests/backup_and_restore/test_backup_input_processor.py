# (C) 2025 GoodData Corporation

import os
import tempfile

import pytest

from gooddata_pipelines.backup_and_restore.backup_input_processor import (
    BackupInputProcessor,
)
from gooddata_pipelines.backup_and_restore.models.input_type import InputType
from gooddata_pipelines.backup_and_restore.models.workspace_response import (
    Hierarchy,
    Links,
    Meta,
    Page,
    Workspace,
    WorkspaceResponse,
)


@pytest.fixture
def backup_input_processor(mock_gooddata_api, mock_logger):
    processor = BackupInputProcessor(mock_gooddata_api, page_size=2)
    processor.hierarchy_endpoint = (
        "/fake/hierarchy?filter=parent.id=={parent_id}"
    )
    processor.all_workspaces_endpoint = "/fake/all"
    processor.logger.subscribe(mock_logger)
    return processor


def test_process_data_extracts_children_and_subparents(backup_input_processor):
    ws1 = Workspace(id="ws1", meta=Meta(hierarchy=Hierarchy(children_count=2)))
    ws2 = Workspace(id="ws2", meta=Meta(hierarchy=Hierarchy(children_count=0)))
    ws3 = Workspace(id="ws3", meta=None)

    result = backup_input_processor.process_data([ws1, ws2, ws3])
    assert result.workspace_ids == ["ws1", "ws2", "ws3"]
    assert result.sub_parents == ["ws1"]


def test_log_paging_progress_logs_info(backup_input_processor, capsys):
    response = WorkspaceResponse(
        data=[],
        meta=Meta(
            page=Page(size=5, total_elements=25, number=1, total_pages=5),
            hierarchy=None,
        ),
        links=Links(self="self", next="next"),
    )

    backup_input_processor.log_paging_progress(response)
    captured = capsys.readouterr()
    assert "Fetched page: 2 of 5" in captured.out


def test_log_paging_progress_no_page(backup_input_processor, capsys):
    response = WorkspaceResponse(
        data=[],
        meta=Meta(page=None, hierarchy=None),
        links=Links(self="self", next="next"),
    )

    backup_input_processor.log_paging_progress(response)
    captured = capsys.readouterr()
    assert captured.out == ""


def test_paginate_calls_fetch_page_and_process_data(
    backup_input_processor, monkeypatch
):
    ws1 = Workspace(id="ws1", meta=Meta(hierarchy=Hierarchy(children_count=1)))
    ws2 = Workspace(id="ws2", meta=Meta(hierarchy=Hierarchy(children_count=0)))
    links1 = Links(self="self", next="next_url")
    links2 = Links(self="self", next=None)
    resp1 = WorkspaceResponse(
        data=[ws1], meta=Meta(hierarchy=None, page=None), links=links1
    )
    resp2 = WorkspaceResponse(
        data=[ws2], meta=Meta(hierarchy=None, page=None), links=links2
    )

    fetch_page_calls = []

    def fetch_page_side_effect(url):
        fetch_page_calls.append(url)
        return resp1 if len(fetch_page_calls) == 1 else resp2

    backup_input_processor.fetch_page = fetch_page_side_effect

    process_data_calls = []

    def process_data_side_effect(data):
        process_data_calls.append(data)
        if len(process_data_calls) == 1:
            return BackupInputProcessor._ProcessDataOutput(["ws1"], ["ws1"])
        else:
            return BackupInputProcessor._ProcessDataOutput(["ws2"], [])

    monkeypatch.setattr(
        BackupInputProcessor,
        "process_data",
        staticmethod(process_data_side_effect),
    )
    monkeypatch.setattr(
        BackupInputProcessor,
        "log_paging_progress",
        staticmethod(lambda resp: None),
    )

    result = backup_input_processor._paginate("first_url")
    assert len(result) == 2
    assert result[0].workspace_ids == ["ws1"]
    assert result[1].workspace_ids == ["ws2"]
    assert len(fetch_page_calls) == 2
    assert len(process_data_calls) == 2


def test_get_hierarchy_recurses(backup_input_processor):
    def fake_paginate(url):
        if "p1" in url:
            return [BackupInputProcessor._ProcessDataOutput(["c1"], ["c1"])]
        if "c1" in url:
            return [BackupInputProcessor._ProcessDataOutput(["c2"], [])]
        return []

    backup_input_processor._paginate = fake_paginate
    result = backup_input_processor.get_hierarchy("p1")
    assert set(result) == {"c1", "c2"}


def test_get_workspaces_to_backup_empty_org(
    backup_input_processor, monkeypatch, capsys
):
    """Test that the function returns an empty list if the organization contains no workspaces."""
    monkeypatch.setattr(
        backup_input_processor,
        "_paginate",
        lambda _: [],
    )
    backup_input_processor.get_ids_to_backup(
        InputType.ORGANIZATION,
        "some-csv-file.csv",
    )
    captured = capsys.readouterr()
    assert "No workspaces found in the organization." in captured.out


def test_read_csv_input_empty_file(backup_input_processor) -> None:
    """Test with an empty CSV file."""
    with tempfile.NamedTemporaryFile() as temp_csv:
        path_to_csv = temp_csv.name
        with pytest.raises(
            ValueError, match="No content found in the CSV file."
        ):
            backup_input_processor.csv_reader.read_backup_csv(path_to_csv)


def test_read_csv_input_only_header(backup_input_processor) -> None:
    """Test with a CSV file that contains only the header."""
    with tempfile.NamedTemporaryFile() as temp_csv:
        temp_csv.write(b"header1\n")
        temp_csv.flush()
        temp_csv.seek(0)
        path_to_csv = temp_csv.name
        with pytest.raises(
            ValueError, match="No workspaces found in the CSV file."
        ):
            backup_input_processor.csv_reader.read_backup_csv(path_to_csv)


def test_read_csv_input_valid(backup_input_processor) -> None:
    """Test with a valid CSV file."""
    with tempfile.NamedTemporaryFile(delete=False) as temp_csv:
        temp_csv.write(b"header1\n")
        temp_csv.write(b"workspace1\n")
        temp_csv.write(b"workspace2\n")
        temp_csv.flush()
        temp_csv.seek(0)
        path_to_csv = temp_csv.name
        result = backup_input_processor.csv_reader.read_backup_csv(path_to_csv)
        assert result == ["workspace1", "workspace2"]
    os.remove(path_to_csv)


def test_read_csv_input_too_many_columns(backup_input_processor) -> None:
    """Test with a CSV file that contains too many columns."""
    with tempfile.NamedTemporaryFile(delete=False) as temp_csv:
        temp_csv.write(b"header1,header2\n")
        temp_csv.write(b"workspace1,extra_column\n")
        temp_csv.flush()
        temp_csv.seek(0)
        path_to_csv = temp_csv.name
        with pytest.raises(
            ValueError,
            match="Input file contains more than one column. Please check the input and try again.",
        ):
            backup_input_processor.csv_reader.read_backup_csv(path_to_csv)
    os.remove(path_to_csv)
