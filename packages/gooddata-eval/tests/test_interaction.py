# (C) 2026 GoodData Corporation
import pytest
from gooddata_eval.cli.agentic_runner import AGENTIC_TEST_KINDS
from gooddata_eval.core.evaluators import supported_test_kinds
from gooddata_eval.core.interaction import (
    MULTI_TURN,
    MULTI_TURN_KINDS,
    SINGLE_SHOT,
    SINGLE_TURN_AGENTIC_KINDS,
    interaction_mode,
)


def test_every_agentic_kind_is_classified_on_purpose():
    """A new agentic kind defaults to single-shot in `interaction_mode`, which would silently
    fold a multi-turn conversation into the per-trace section. Failing here makes whoever adds
    the kind say which it is."""
    assert SINGLE_TURN_AGENTIC_KINDS | MULTI_TURN_KINDS == AGENTIC_TEST_KINDS
    assert not SINGLE_TURN_AGENTIC_KINDS & MULTI_TURN_KINDS


@pytest.mark.parametrize("kind", sorted(supported_test_kinds()))
def test_the_non_agentic_kinds_are_single_shot(kind):
    # They send one chat message (or one summary request) per run.
    assert interaction_mode(kind) == SINGLE_SHOT


@pytest.mark.parametrize("kind", sorted(SINGLE_TURN_AGENTIC_KINDS))
def test_single_turn_agentic_kinds_are_single_shot(kind):
    assert interaction_mode(kind) == SINGLE_SHOT


@pytest.mark.parametrize("kind", sorted(MULTI_TURN_KINDS))
def test_conversation_driving_kinds_are_multi_turn(kind):
    assert interaction_mode(kind) == MULTI_TURN
