# (C) 2026 GoodData Corporation
"""Contract test for the FEAT-002 → gooddata-eval integration seam.

FEAT-002 (synthetic conversations generator) emits a JSONL archive of *captured*
conversations: one conversation per line with `id`, `topic`, `workspace`, and
`turns` (each turn has `user` + `assistant`). It deliberately does NOT produce
expected outputs (scoring is gooddata-eval's job).

This test pins exactly how that output relates to gooddata-eval's two input
formats, so the gap is explicit and the adapter requirements are documented
rather than discovered at integration time. See `docs/coverage-map.md`.
"""
import json

import pytest
from pydantic import ValidationError

from gooddata_eval.core.agentic.conversation import ConversationFixture
from gooddata_eval.core.dataset.local import load_local_dataset
from gooddata_eval.core.models import DatasetItem


def _feat002_conversation() -> dict:
    """A single FEAT-002 archive line (per FEAT-002 spec §Scope)."""
    return {
        "id": "conv-001",
        "topic": "metric-lookup",
        "workspace": "globalmart",
        "turns": [
            {"user": "What was total revenue last quarter?", "assistant": "Total revenue was $1.2M."},
            {"user": "Break it down by region.", "assistant": "Here is revenue by region: ..."},
        ],
    }


def test_feat002_archive_is_jsonl_not_a_dataset_folder():
    """FEAT-002 emits JSONL (one conversation per line); gooddata-eval's
    --dataset loader reads a *folder of .json files* (one DatasetItem per file).
    An adapter must split/transform JSONL → per-item files."""
    line = json.dumps(_feat002_conversation())
    parsed = json.loads(line)
    # FEAT-002 carries conversation-level keys, not the DatasetItem envelope.
    assert set(parsed) == {"id", "topic", "workspace", "turns"}
    assert "test_kind" not in parsed
    assert "expected_output" not in parsed


def test_feat002_conversation_does_not_satisfy_conversation_fixture():
    """The natural target is the multi-turn `agentic_conversation` system, but
    FEAT-002 turns lack the required `turn_id` / `message` / `expected_skill`
    fields, and the fixture needs top-level `expected_skills`. Captured
    `assistant` text is not an `expected_*` annotation."""
    conv = _feat002_conversation()
    with pytest.raises(ValidationError):
        ConversationFixture.model_validate(conv)
    # The turn shape diverges: FEAT-002 has user/assistant, the fixture needs
    # turn_id/message/expected_skill.
    feat002_turn_keys = set(conv["turns"][0])
    required_turn_keys = {"turn_id", "message", "expected_skill"}
    assert feat002_turn_keys.isdisjoint(required_turn_keys)


def _adapt_feat002_to_conversation_fixture(conv: dict, expected_skills_per_turn: list[str]) -> ConversationFixture:
    """Reference adapter: FEAT-002 conversation + externally-supplied per-turn
    expected skills → a valid ConversationFixture.

    This documents the MINIMUM extra information FEAT-002 output needs before it
    can drive the agentic_conversation evaluator: an `expected_skill` per turn
    (the captured `assistant` text alone is insufficient — it is an observation,
    not an expectation)."""
    turns = [
        {
            "turn_id": f"{conv['id']}-t{i}",
            "message": t["user"],
            "expected_skill": skill,
        }
        for i, (t, skill) in enumerate(zip(conv["turns"], expected_skills_per_turn))
    ]
    return ConversationFixture.model_validate(
        {
            "id": conv["id"],
            "dataset_name": conv["topic"],
            "expected_skills": sorted(set(expected_skills_per_turn)),
            "turns": turns,
        }
    )


def test_adapter_produces_valid_conversation_fixture_with_annotations():
    """With per-turn expected_skill annotations supplied, FEAT-002 output adapts
    into a valid ConversationFixture. This is the concrete integration recipe."""
    conv = _feat002_conversation()
    fixture = _adapt_feat002_to_conversation_fixture(conv, ["create_metric", "create_visualization"])
    assert fixture.id == "conv-001"
    assert [t.message for t in fixture.turns] == [t["user"] for t in conv["turns"]]
    assert fixture.expected_skills == ["create_metric", "create_visualization"]


def test_adapted_fixture_loads_as_agentic_conversation_dataset_item(tmp_path):
    """End-to-end seam check: the adapted fixture, wrapped in a DatasetItem file,
    loads via the standard local loader as an `agentic_conversation` item."""
    conv = _feat002_conversation()
    fixture = _adapt_feat002_to_conversation_fixture(conv, ["create_metric", "create_visualization"])
    item_dict = {
        "id": conv["id"],
        "dataset_name": conv["topic"],
        "test_kind": "agentic_conversation",
        "question": conv["turns"][0]["user"],
        "expected_output": {"fixture": fixture.model_dump()},
    }
    (tmp_path / "conv-001.json").write_text(json.dumps(item_dict))
    items = load_local_dataset(tmp_path)
    assert len(items) == 1
    assert isinstance(items[0], DatasetItem)
    assert items[0].test_kind == "agentic_conversation"
    # And the fixture round-trips back out of the loaded item.
    reloaded = ConversationFixture.model_validate(items[0].expected_output["fixture"])
    assert reloaded.id == "conv-001"
