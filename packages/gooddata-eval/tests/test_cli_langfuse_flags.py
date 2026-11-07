# (C) 2026 GoodData Corporation
"""--langfuse-item-id / --langfuse-item-metadata / --run-metadata-json.

The three flags that let a caller run part of a Langfuse dataset and say what the run was,
plus a regression guard that a run using none of them is dispatched exactly as before.
"""

import json
from unittest.mock import patch

import pytest
from gooddata_eval.cli import main as cli_main
from gooddata_eval.core.config import RunConfig

_BASE = ["run", "--host", "h", "--workspace", "w", "--langfuse-dataset", "mastercard_search_tool"]


def test_item_id_is_repeatable():
    args = cli_main.parse_args([*_BASE, "--langfuse-item-id", "q1-en", "--langfuse-item-id", "q2-en"])
    assert args.langfuse_item_ids == ["q1-en", "q2-en"]


def test_item_metadata_parses_key_value_pairs():
    args = cli_main.parse_args(
        [*_BASE, "--langfuse-item-metadata", "language=es", "--langfuse-item-metadata", "complexity=Basic"]
    )
    assert args.langfuse_item_metadata == [("language", "es"), ("complexity", "Basic")]


@pytest.mark.parametrize("bad", ["language", "=es", "  =es"])
def test_item_metadata_rejects_a_pair_without_a_key(bad):
    with pytest.raises(SystemExit):
        cli_main.parse_args([*_BASE, "--langfuse-item-metadata", bad])


def test_item_metadata_keeps_an_empty_value():
    """`key=` is a real filter -- an item whose metadata holds "" for that key."""
    args = cli_main.parse_args([*_BASE, "--langfuse-item-metadata", "language="])
    assert args.langfuse_item_metadata == [("language", "")]


def test_all_three_flags_default_to_empty():
    args = cli_main.parse_args([*_BASE])
    assert args.langfuse_item_ids == []
    assert args.langfuse_item_metadata == []
    assert args.run_metadata_json is None


def test_run_metadata_json_is_read_from_the_file(tmp_path):
    path = tmp_path / "run.json"
    path.write_text(json.dumps({"agent_id": "a-1", "child_workspace_id": "ws-1"}), encoding="utf-8")
    assert cli_main._load_run_metadata(str(path)) == {"agent_id": "a-1", "child_workspace_id": "ws-1"}


@pytest.mark.parametrize("payload", ["[1, 2]", '"a string"', "42"])
def test_run_metadata_json_rejects_a_non_object(tmp_path, payload):
    """Dataset-run metadata is merged key by key, so a list has nowhere to go."""
    path = tmp_path / "run.json"
    path.write_text(payload, encoding="utf-8")
    with pytest.raises(ValueError, match="expected a JSON object"):
        cli_main._load_run_metadata(str(path))


def test_run_metadata_json_rejects_malformed_json(tmp_path):
    path = tmp_path / "run.json"
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(ValueError, match="not valid JSON"):
        cli_main._load_run_metadata(str(path))


def test_item_filters_reach_load_langfuse_dataset():
    config = RunConfig(
        host="h",
        token="t",
        workspace_id="w",
        langfuse_dataset="mastercard_search_tool",
        kind="search_tool",
        item_ids=("q1-en",),
        item_metadata_filter={"language": "en"},
    )
    with patch("gooddata_eval.core.dataset.langfuse_source.load_langfuse_dataset") as load:
        cli_main._load_dataset(config)
    load.assert_called_once_with(
        "mastercard_search_tool",
        default_test_kind="search_tool",
        item_ids=("q1-en",),
        metadata_filter={"language": "en"},
    )


def test_without_the_flags_the_loader_is_called_as_before():
    """Regression guard: an unfiltered Langfuse run must pass None, not an empty container.

    An empty tuple reaching `item_ids` would select zero items and raise, turning every
    existing unfiltered run into an error.
    """
    config = RunConfig(host="h", token="t", workspace_id="w", langfuse_dataset="ds", kind="search_tool")
    with patch("gooddata_eval.core.dataset.langfuse_source.load_langfuse_dataset") as load:
        cli_main._load_dataset(config)
    load.assert_called_once_with("ds", default_test_kind="search_tool", item_ids=None, metadata_filter=None)


@pytest.mark.parametrize(
    "extra",
    [{"item_ids": ("q1-en",)}, {"item_metadata_filter": {"language": "es"}}],
)
def test_item_filters_with_a_local_dataset_are_refused(tmp_path, capsys, extra):
    """Ignoring them would run the whole local folder and report it as that language."""
    config = RunConfig(host="h", token="t", workspace_id="w", dataset_folder=tmp_path, **extra)
    assert cli_main._run(config) != 0
    assert "require --langfuse-dataset" in capsys.readouterr().err


# run_metadata's journey into the dataset-run metadata is covered behaviourally in
# test_agentic_runner.py, next to the --tag case it merges with.
