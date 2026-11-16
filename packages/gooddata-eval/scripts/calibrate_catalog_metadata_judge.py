# (C) 2026 GoodData Corporation
"""Does the real judge grade catalog_metadata criteria on the right side?

tests/test_catalog_metadata_evaluator.py pins the wiring; it cannot pin the verdict, because
the verdict is an LLM's. This does, against tests/fixtures/catalog_metadata_calibration.json:
each case is one item question (the object's real metadata), one criterion and one text, and
the criterion must be satisfied ("pass") or not ("fail") on every run.

The fixture keeps texts that state a wrong fact the question contradicts: a violation judge
that grades correctness instead of presence scores those as absent and lets them pass.

Run it after changing _POSITIVE_STEPS / _VIOLATION_STEPS:

    OPENAI_API_KEY=... make calibrate-catalog-metadata

It is a script rather than a test because CI has no OPENAI_API_KEY. Exits 1 on any mismatch.
"""

import json
import os
import sys
from pathlib import Path

from gooddata_eval.core.evaluators.catalog_metadata import CatalogMetadataEvaluator
from gooddata_eval.core.models import CatalogInput, ChatResult, DatasetItem

RUNS = 3
FIXTURE = Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "catalog_metadata_calibration.json"
_FIELDS = {"include": "must_include", "exclude": "must_not_include"}


def main() -> int:
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY required")
    cases = json.loads(FIXTURE.read_text())
    evaluator = CatalogMetadataEvaluator()
    print(f"judge model: {evaluator._positive_judge.model}, runs: {RUNS}")
    mismatches = 0
    for case in cases:
        item = DatasetItem(
            id=case["label"],
            dataset_name="catalog_metadata_calibration",
            test_kind="catalog_metadata",
            question=case["question"],
            expected_output={_FIELDS[case["kind"]]: [case["criterion"]], "format": {}},
            catalog_input=CatalogInput.model_validate(
                {"object_type": "Metric", "object_id": "calibration", "output": case["output"]}
            ),
        )
        chat = ChatResult(text_response=case["text"], raw_response={"note": None})
        key = f"{case['kind']}_0"
        satisfied = sum(evaluator.evaluate(item, chat).detail.get(key) is True for _ in range(RUNS))
        want = RUNS if case["want"] == "pass" else 0
        ok = satisfied == want
        mismatches += not ok
        print(f"{case['label']:48} want {case['want']:4}  satisfied {satisfied}/{RUNS}  {'OK' if ok else 'MISMATCH'}")
    print(f"\n{'all calibration texts on the right side' if not mismatches else f'{mismatches} mismatch(es)'}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
