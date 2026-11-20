# (C) 2026 GoodData Corporation
"""Does the real judge grade agentic_knowledge criteria on the right side?

tests/test_knowledge_evaluator.py pins the wiring, not the verdict. This pins the verdict,
against tests/fixtures/knowledge_calibration.json: each case is one question, one criterion
and one real answer, and the criterion must be satisfied ("pass") or not ("fail") on every run.

Run it after changing the judge steps in core/evaluators/knowledge.py:

    OPENAI_API_KEY=... make calibrate-knowledge

A script, not a test: CI has no OPENAI_API_KEY. Exits 1 on any mismatch.
"""

import json
import os
import sys
from pathlib import Path

from gooddata_eval.core.evaluators.knowledge import AgenticKnowledgeEvaluator
from gooddata_eval.core.models import ChatResult, DatasetItem

RUNS = 3
FIXTURE = Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "knowledge_calibration.json"
_FIELDS = {"include": "must_include", "exclude": "must_not_include"}


def main() -> int:
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY required")
    cases = json.loads(FIXTURE.read_text(encoding="utf-8"))
    evaluator = AgenticKnowledgeEvaluator()
    print(f"judge model: {evaluator._positive_judge.model}, runs: {RUNS}")
    mismatches = 0
    for case in cases:
        item = DatasetItem(
            id=case["label"],
            dataset_name="knowledge_calibration",
            test_kind="agentic_knowledge",
            question=case["question"],
            # No tool calls here: only the judge is calibrated.
            expected_output={_FIELDS[case["kind"]]: [case["criterion"]], "expect_search": False},
        )
        chat = ChatResult(text_response=case["text"])
        key = f"{case['kind']}_0"
        verdicts = [evaluator.evaluate(item, [chat]).detail.get(key) for _ in range(RUNS)]
        ungraded = sum(not isinstance(v, bool) for v in verdicts)
        satisfied = sum(v is True for v in verdicts)
        want = RUNS if case["want"] == "pass" else 0
        # An ungraded run proves nothing, on either side.
        ok = satisfied == want and not ungraded
        mismatches += not ok
        print(
            f"{case['label'][:44]:44} {case['kind']:7} want {case['want']:4}  satisfied {satisfied}/{RUNS}"
            f"{f'  ungraded {ungraded}' if ungraded else ''}  {'OK' if ok else 'MISMATCH'}"
        )
    print(f"\n{'all calibration answers on the right side' if not mismatches else f'{mismatches} mismatch(es)'}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
