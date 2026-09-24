# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
import json

import pytest
from gooddata_eval.core.agentic._obfuscation_check import (
    AI_ON_DATA_REDACTION,
    SINK_CONVERSATION_DB,
    SINK_LANGFUSE_TRACE,
    SINKS,
    derive_anchor,
    evaluate_case,
    find_canary,
)
from gooddata_eval.core.agentic.obfuscation import without_canaries

_QUESTION = "Can you check the recent orders for the account registered to marie.canary7f3a@example.invalid?"
_EMAIL = {
    "nonce": "canary7f3a",
    "value": "marie.canary7f3a@example.invalid",
    "class": "EMAIL",
    "absent_from": [SINK_LANGFUSE_TRACE, SINK_CONVERSATION_DB],
    "mask_marker_present": "[EMAIL]",
}
_ENFORCED = {"canaries": [_EMAIL], "status": "enforced"}
_ANCHOR = "Can you check the recent orders for the"
_MASKED = "Can you check the recent orders for the account registered to [EMAIL]?"


def _db(text: str) -> dict:
    return {"conversation": {"title": None}, "items": [{"role": "user", "content": {"type": "text", "text": text}}]}


def _trace(text: str) -> list:
    # Langfuse keeps span input as a JSON document serialised into a string.
    return [{"id": "t1", "input": json.dumps({"parts": [{"text": text}]}), "observations": []}]


def _sinks(db_text: str, trace_text: str) -> dict:
    return {SINK_CONVERSATION_DB: _db(db_text), SINK_LANGFUSE_TRACE: _trace(trace_text)}


def test_anchor_is_the_longest_plain_word_run_outside_the_canary():
    assert derive_anchor(_QUESTION, [_EMAIL]) == _ANCHOR


def test_anchor_does_not_keep_the_part_of_a_canary_left_around_its_nonce():
    escaped = {
        "nonce": "canary2d8e",
        "value": "john\\.canary2d8e@northwind\\-demo\\.invalid",
        "unescaped_value": "john.canary2d8e@northwind-demo.invalid",
    }
    question = "Pouvez-vous verifier la commande passee par john\\.canary2d8e@northwind\\-demo\\.invalid la semaine"
    assert derive_anchor(question, [escaped]) == "vous verifier la commande passee par"


def test_anchor_is_none_when_nothing_but_the_canary_is_left():
    assert derive_anchor("marie.canary7f3a@example.invalid", [_EMAIL]) is None


def test_masked_in_both_sinks_passes():
    verdict = evaluate_case(_ENFORCED, _sinks(_MASKED, _MASKED), [_ANCHOR])
    assert verdict.passed, verdict.failures


def test_canary_inside_json_serialised_trace_input_is_a_leak():
    verdict = evaluate_case(_ENFORCED, _sinks(_MASKED, _QUESTION), [_ANCHOR])
    assert [f for f in verdict.failures if f.startswith("LEAK")] == [
        f"LEAK EMAIL 'canary7f3a' in {SINK_LANGFUSE_TRACE}: $[0].input<json>.parts[0].text ('canary7f3a')"
    ]


def test_a_sink_without_the_anchor_is_blind_not_clean():
    verdict = evaluate_case(_ENFORCED, _sinks(_MASKED, "unrelated title-generation trace"), [_ANCHOR])
    assert not verdict.passed
    assert any("blind" in f and SINK_LANGFUSE_TRACE in f for f in verdict.failures)


def test_a_sink_that_was_not_collected_fails():
    verdict = evaluate_case(_ENFORCED, {SINK_CONVERSATION_DB: _db(_MASKED), SINK_LANGFUSE_TRACE: None}, [_ANCHOR])
    assert any("not collected" in f for f in verdict.failures)


def test_ai_on_data_redaction_is_reported_instead_of_passing():
    verdict = evaluate_case(_ENFORCED, _sinks(_MASKED, AI_ON_DATA_REDACTION), [_ANCHOR])
    assert any("enableGenAiTraceRedaction" in f for f in verdict.failures)


def test_missing_mask_marker_fails_even_without_a_leak():
    verdict = evaluate_case(_ENFORCED, _sinks(_MASKED, "Can you check the recent orders for the account?"), [_ANCHOR])
    assert any("mask marker '[EMAIL]' missing from langfuse_trace" in f for f in verdict.failures)


def test_card_written_with_spaces_matches_the_compact_nonce():
    card = {"nonce": "4916338506082832", "value": "4916338506082832", "class": "CREDIT_CARD"}
    assert find_canary(card, SINK_CONVERSATION_DB, {"text": "card 4916 3385-0608 2832"})


def test_known_limitation_that_stops_reproducing_asks_for_a_deliberate_flip():
    person = {"nonce": "Canary8d47", "value": "Marina Canary8d47", "class": "PERSON", "present_in": list(SINKS)}
    expected = {
        "canaries": [person],
        "status": "known_limitation",
        "known_limitation": {"flip_when": "the PERSON classifier ships"},
    }
    anchor = "was diagnosed in march"
    masked = f"Patient [PERSON] {anchor}"
    verdict = evaluate_case(expected, _sinks(masked, masked), [anchor])
    assert len(verdict.failures) == 2
    assert all("the PERSON classifier ships" in f for f in verdict.failures)


_DECIMAL = {
    "nonce": "5621697898080164",
    "value": "0.5621697898080164",
    "class": "NOT_SENSITIVE",
    "present_in": list(SINKS),
}
_DECIMAL_ANCHOR = "Is that higher than the average monthly"


def test_an_enforced_value_that_must_stay_is_reported_as_over_masked_when_masked():
    masked = f"Our margin came out as 0.[CREDIT_CARD]. {_DECIMAL_ANCHOR} margin?"
    verdict = evaluate_case({"canaries": [_DECIMAL], "status": "enforced"}, _sinks(masked, masked), [_DECIMAL_ANCHOR])
    assert sorted(verdict.failures) == [
        f"OVER-MASKED NOT_SENSITIVE '5621697898080164' in {sink}: expected unchanged but it was masked (false positive)"
        for sink in sorted(SINKS)
    ]


def test_an_enforced_value_that_must_stay_passes_when_left_alone():
    kept = f"Our margin came out as 0.5621697898080164. {_DECIMAL_ANCHOR} margin?"
    verdict = evaluate_case({"canaries": [_DECIMAL], "status": "enforced"}, _sinks(kept, kept), [_DECIMAL_ANCHOR])
    assert verdict.passed


def test_a_canary_used_as_a_json_key_is_a_leak():
    pasted = '{"marie.canary7f3a@example.invalid": true, "note": "Can you check the recent orders for the account"}'
    verdict = evaluate_case(_ENFORCED, _sinks(pasted, _MASKED), [_ANCHOR])
    assert any(
        f.startswith(f"LEAK EMAIL 'canary7f3a' in {SINK_CONVERSATION_DB}") and "<key>" in f for f in verdict.failures
    )


def test_rejected_turn_may_export_no_trace():
    expected = {"canaries": [{**_EMAIL, "mask_marker_present": None}], "status": "enforced"}
    sinks = {SINK_CONVERSATION_DB: {"conversation": {}, "items": []}, SINK_LANGFUSE_TRACE: None}
    verdict = evaluate_case(expected, sinks, [], turn_rejected=True)
    assert verdict.passed, verdict.failures
    assert verdict.notes


def test_rejected_turn_still_convicts_a_trace_that_shows_the_canary():
    expected = {"canaries": [{**_EMAIL, "mask_marker_present": None}], "status": "enforced"}
    sinks = {SINK_CONVERSATION_DB: {"conversation": {}, "items": []}, SINK_LANGFUSE_TRACE: _trace(_QUESTION)}
    verdict = evaluate_case(expected, sinks, [], turn_rejected=True)
    assert any(f.startswith("LEAK") for f in verdict.failures)


def test_record_only_path_is_reported_but_not_gated():
    canary = {**_EMAIL, "record_only_paths": [r"\.alertProposal\."]}
    db = _db(_MASKED)
    db["items"].append({"role": "assistant", "content": {"parts": [{"alertProposal": {"to": _EMAIL["value"]}}]}})
    verdict = evaluate_case({"canaries": [canary]}, {**_sinks(_MASKED, _MASKED), SINK_CONVERSATION_DB: db}, [_ANCHOR])
    assert verdict.passed, verdict.failures
    assert any(n.startswith("RECORDED EMAIL") and "alertProposal" in n for n in verdict.notes)


def test_a_canary_outside_the_record_only_path_still_fails():
    canary = {**_EMAIL, "record_only_paths": [r"\.alertProposal\."]}
    verdict = evaluate_case({"canaries": [canary]}, _sinks(_QUESTION, _MASKED), [_ANCHOR])
    assert any(f.startswith("LEAK") for f in verdict.failures)


def test_unknown_sink_name_is_a_fixture_error():
    expected = {"canaries": [{**_EMAIL, "absent_from": ["langfuse"]}]}
    with pytest.raises(ValueError, match="unknown sink"):
        evaluate_case(expected, _sinks(_MASKED, _MASKED), [_ANCHOR])


def test_langfuse_comment_carries_no_canary_spelling():
    card = {"nonce": "4916338506082832", "value": "4916 3385 0608 2832", "class": "CREDIT_CARD"}
    text = "LEAK CREDIT_CARD '4916338506082832' in conversation_db: $.items[0] ('4916 3385 0608 2832')"
    cleaned = without_canaries(text, [card])
    assert "4916" not in cleaned
    assert "<CREDIT_CARD>" in cleaned


def test_a_numeric_secret_inside_decoded_json_is_found():
    password = {"nonce": "90210731", "value": "90210731", "class": "PASSWORD"}
    stored = {"items": [{"content": {"text": '{"api_key": "[API_KEY]", "password": 90210731}'}}]}
    assert find_canary(password, SINK_CONVERSATION_DB, stored)


def test_booleans_are_not_leaves():
    flag = {"nonce": "True", "value": "True", "class": "TOKEN"}
    assert not find_canary(flag, SINK_CONVERSATION_DB, {"passed": True})
