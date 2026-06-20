# (C) 2026 GoodData Corporation
import pytest
from gooddata_eval.core.dataset.local import load_local_dataset


def test_load_local_dataset_reads_json_files(fixtures_dir):
    from gooddata_eval.core.evaluators import supported_test_kinds

    items = load_local_dataset(fixtures_dir / "sample_dataset")
    # sample_dataset is the canonical fixture: one item per supported test_kind.
    assert len(items) == len(supported_test_kinds())
    ids = {i.id for i in items}
    assert "acme-001" in ids
    assert "metric-001" in ids
    assert {i.test_kind for i in items} == set(supported_test_kinds())


def test_load_local_dataset_missing_folder_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_local_dataset(tmp_path / "does-not-exist")


def test_load_local_dataset_empty_folder_raises(tmp_path):
    with pytest.raises(ValueError, match="no .json"):
        load_local_dataset(tmp_path)
