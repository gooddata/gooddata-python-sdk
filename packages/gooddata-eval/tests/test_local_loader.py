# (C) 2026 GoodData Corporation
import pytest
from gooddata_eval.core.dataset.local import load_local_dataset


def test_load_local_dataset_reads_json_files(fixtures_dir):
    items = load_local_dataset(fixtures_dir / "sample_dataset")
    assert len(items) == 2
    ids = {i.id for i in items}
    assert "acme-001" in ids
    assert "metric-001" in ids


def test_load_local_dataset_missing_folder_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_local_dataset(tmp_path / "does-not-exist")


def test_load_local_dataset_empty_folder_raises(tmp_path):
    with pytest.raises(ValueError, match="no .json"):
        load_local_dataset(tmp_path)
