# (C) 2026 GoodData Corporation
"""Does the real judge put each calibration text on the right side of every default criterion?

tests/test_takeaway_evaluator.py pins the wiring and the criterion wording; it cannot pin
the verdict, because the verdict is an LLM's. This does, against the texts in
tests/fixtures/takeaway_calibration.json:

- a "pass" text must satisfy every default judge criterion on every run;
- a "fail" text must violate each criterion it names on every run.

Run it after changing any DEFAULT_MUST_INCLUDE / DEFAULT_MUST_NOT_INCLUDE wording:

    OPENAI_API_KEY=... make calibrate-takeaway

It is a script rather than a test because CI has no OPENAI_API_KEY. Exits 1 on any mismatch.
"""

import json
import os
import sys
from pathlib import Path

from gooddata_eval.core.evaluators.takeaway import (
    DEFAULT_MUST_INCLUDE,
    DEFAULT_MUST_NOT_INCLUDE,
    DocumentTakeawayEvaluator,
)
from gooddata_eval.core.models import ChatResult, DatasetItem, TakeawayInput

RUNS = 3
FIXTURE = Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "takeaway_calibration.json"

CRITERIA = {f"default_include_{k}": k for k in DEFAULT_MUST_INCLUDE} | {
    f"default_exclude_{k}": k for k in DEFAULT_MUST_NOT_INCLUDE
}


def main() -> int:
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY required")
    fixture = json.loads(FIXTURE.read_text())
    evaluator = DocumentTakeawayEvaluator()
    print(f"judge model: {evaluator._positive_judge.model}, runs: {RUNS}")
    mismatches = 0
    for case in fixture["texts"]:
        item = DatasetItem(
            id=case["label"],
            dataset_name="takeaway_calibration",
            test_kind="document_takeaway",
            question=fixture["question"],
            expected_output={},
            takeaway_input=TakeawayInput(visualizations=["calibration"]),
        )
        chat = ChatResult(text_response=case["text"], raw_response={"takeaway": case["text"], "noData": False})
        satisfied = dict.fromkeys(CRITERIA.values(), 0)
        for _ in range(RUNS):
            detail = evaluator.evaluate(item, chat).detail
            for key, name in CRITERIA.items():
                satisfied[name] += detail.get(key) is True
        want_pass = case["want"] == "pass"
        must = dict.fromkeys(satisfied, RUNS) if want_pass else dict.fromkeys(case["criteria"], 0)
        print(f"\n{case['label']} (want {case['want']})")
        for name, count in satisfied.items():
            flag = ""
            if name in must:
                ok = count == must[name]
                mismatches += not ok
                flag = "OK" if ok else "MISMATCH"
            print(f"  {name:20} satisfied {count}/{RUNS}  {flag}")
    print(f"\n{'all calibration texts on the right side' if not mismatches else f'{mismatches} mismatch(es)'}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
