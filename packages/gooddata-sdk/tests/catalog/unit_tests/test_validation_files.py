# (C) 2026 GoodData Corporation
"""Checks on the layout as it sits on disk.

These exist because loading throws the filesystem away: once objects are in a model, a
filename that disagreed with its object, or two files claiming one id, have already
resolved themselves silently.
"""

from __future__ import annotations

from pathlib import Path

from gooddata_sdk.catalog.validation.files import check_layout_files


def _write(root: Path, folder: str, filename: str, body: str) -> Path:
    directory = root / folder
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / filename
    path.write_text(body)
    return path


def _codes(findings: list) -> list[str]:
    return [f.code for f in findings]


class TestHealthyLayout:
    def test_matching_filenames_and_ids_are_quiet(self, tmp_path):
        _write(tmp_path, "metrics", "revenue.yaml", "id: revenue\ntitle: Revenue\ncontent:\n  maql: SELECT 1\n")
        _write(tmp_path, "visualization_objects", "v1.yaml", "id: v1\ntitle: V1\ncontent: {}\n")
        assert check_layout_files(tmp_path) == []

    def test_a_directory_that_does_not_exist_is_not_an_error(self, tmp_path):
        """Callers point this at a layout that may legitimately hold only some kinds."""
        assert check_layout_files(tmp_path / "missing") == []

    def test_folders_the_sdk_does_not_know_are_left_alone(self, tmp_path):
        _write(tmp_path, "notes", "whatever.yaml", "just: text\n")
        assert check_layout_files(tmp_path) == []


class TestFilenameIdMismatch:
    def test_a_file_whose_name_disagrees_with_its_id_is_reported(self, tmp_path):
        """The layout writes <id>.yaml, so this object round-trips into a different file and
        overwrites whatever legitimately owns that name."""
        _write(tmp_path, "metrics", "old_name.yaml", "id: new_name\ntitle: M\ncontent:\n  maql: SELECT 1\n")
        findings = check_layout_files(tmp_path)
        assert _codes(findings) == ["filename_id_mismatch"]
        assert findings[0].object_id == "new_name"
        assert "old_name.yaml" in findings[0].location

    def test_a_file_without_an_id_is_reported(self, tmp_path):
        _write(tmp_path, "metrics", "m.yaml", "title: no id here\ncontent: {}\n")
        assert _codes(check_layout_files(tmp_path)) == ["missing_id"]

    def test_a_non_string_id_is_reported(self, tmp_path):
        _write(tmp_path, "metrics", "m.yaml", "id: 7\ntitle: M\ncontent: {}\n")
        assert _codes(check_layout_files(tmp_path)) == ["missing_id"]


class TestDuplicateIdsAcrossFiles:
    def test_two_files_claiming_one_id_are_reported(self, tmp_path):
        _write(tmp_path, "metrics", "a.yaml", "id: same\ntitle: A\ncontent: {}\n")
        _write(tmp_path, "metrics", "b.yaml", "id: same\ntitle: B\ncontent: {}\n")
        findings = check_layout_files(tmp_path)
        assert "duplicate_id_in_files" in _codes(findings)

    def test_the_same_id_in_two_collections_is_fine(self, tmp_path):
        _write(tmp_path, "metrics", "shared.yaml", "id: shared\ntitle: M\ncontent: {}\n")
        _write(tmp_path, "visualization_objects", "shared.yaml", "id: shared\ntitle: V\ncontent: {}\n")
        assert check_layout_files(tmp_path) == []


class TestUnreadableFiles:
    def test_a_file_that_is_not_valid_yaml_is_reported_not_raised(self, tmp_path):
        """One unreadable file must not hide the state of the rest of the layout."""
        _write(tmp_path, "metrics", "broken.yaml", "id: x\n  bad: [indent\n")
        _write(tmp_path, "metrics", "fine.yaml", "id: fine\ntitle: F\ncontent: {}\n")
        findings = check_layout_files(tmp_path)
        assert _codes(findings) == ["unreadable_file"]
        assert "broken.yaml" in findings[0].location

    def test_a_file_holding_a_list_rather_than_an_object_is_reported(self, tmp_path):
        _write(tmp_path, "metrics", "m.yaml", "- one\n- two\n")
        findings = check_layout_files(tmp_path)
        assert _codes(findings) == ["unreadable_file"]
        assert "expected a mapping" in findings[0].message
