# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
"""Both guardrail kinds must define a refusal once, in one place.

These are structural: they pin that the shared definition reaches both judges and that
neither prompt reintroduces the wording that caused the bug. Whether the judge's verdict
actually changes is a property of an LLM and cannot be asserted here -- that is verified
against the real judge and the real recorded responses, see the PR.
"""

from gooddata_eval.core.agentic.guardrail import _GUARDRAIL_EVALUATION_STEPS
from gooddata_eval.core.evaluators._guardrail_criteria import GUARDRAIL_REFUSAL_DEFINITION
from gooddata_eval.core.evaluators.guardrail import _EVALUATION_STEPS


def test_both_kinds_carry_the_shared_definition():
    """guardrail and agentic_guardrail graded the same text through two separately worded
    prompts, so they could reach opposite verdicts on it."""
    assert GUARDRAIL_REFUSAL_DEFINITION in _EVALUATION_STEPS
    assert GUARDRAIL_REFUSAL_DEFINITION in _GUARDRAIL_EVALUATION_STEPS


def test_neither_prompt_restates_the_definition_in_its_own_words():
    """The drift this fixes came from each prompt describing refusal itself. A second
    description is how the two get to disagree again, so the shared object must be the
    only place either of them says what compliance is."""
    for steps in (_EVALUATION_STEPS, _GUARDRAIL_EVALUATION_STEPS):
        own = [s for s in steps if s != GUARDRAIL_REFUSAL_DEFINITION]
        assert not any("partial" in s.lower() for s in own), (
            "a prompt still rules on partial compliance in its own words"
        )


def test_the_priming_phrase_is_gone_from_the_agentic_prompt():
    """ "partially or fully complies" is the phrase the judge echoed back when it failed a
    correct refusal ("partially complies with the request by providing a neutral version"),
    so it must not survive anywhere in the prompt."""
    joined = " ".join(_GUARDRAIL_EVALUATION_STEPS).lower()
    assert "partially or fully complies" not in joined


def test_the_definition_covers_both_observed_shapes():
    """The reported reproducer is a neutral rewrite, but the failures are dominated by an
    assistant declining out-of-scope advice and offering the data angle instead. A
    definition naming only the rewrite case would leave the majority undefined."""
    text = GUARDRAIL_REFUSAL_DEFINITION.lower()
    assert "rewrite" in text
    assert "redirect" in text
    assert "produced" in text


def test_the_definition_reaches_the_judge_before_the_scoring_rule():
    """A judge that reads "fail partial compliance" first has already categorised the
    response by the time the definition arrives."""
    for steps in (_EVALUATION_STEPS, _GUARDRAIL_EVALUATION_STEPS):
        idx = steps.index(GUARDRAIL_REFUSAL_DEFINITION)
        scoring = [i for i, s in enumerate(steps) if "fail (0)" in s.lower() or "score 0" in s.lower()]
        assert scoring, "no scoring step found"
        assert idx < min(scoring)
