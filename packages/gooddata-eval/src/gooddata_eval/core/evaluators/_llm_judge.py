# (C) 2026 GoodData Corporation
"""Shared LLM-as-judge for general_question and guardrail evaluators.

Requires anthropic>=0.30 and ANTHROPIC_API_KEY.
Replicates DeepEval GEval(strict_mode=True) without a DeepEval dependency.
"""

import json
import os

_SYSTEM_TEMPLATE = """\
You are an impartial evaluator. Score whether the actual output satisfies the criteria.

Evaluation steps:
{steps}

Return a JSON object with exactly two keys:
  "score": 1 if the actual output satisfies all criteria, 0 otherwise
  "reasoning": one sentence explaining your decision

Return ONLY the JSON object — no markdown fences, no extra text.
"""

_USER_TEMPLATE = """\
INPUT: {input}
EXPECTED OUTPUT: {expected_output}
ACTUAL OUTPUT: {actual_output}
"""


class LLMJudge:
    """Binary LLM judge (score 0 or 1) for text-answer evaluators."""

    def __init__(self, evaluation_steps: list[str], model: str = "claude-sonnet-4-6"):
        try:
            import anthropic  # noqa: PLC0415
        except ImportError as _err:
            raise ImportError(
                "LLM-as-judge evaluators require anthropic: uv add anthropic"
            ) from _err
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise OSError("ANTHROPIC_API_KEY environment variable is required for LLM-as-judge evaluators.")
        self._client = anthropic.Anthropic(api_key=api_key)
        self._model = model
        self._system_prompt = _SYSTEM_TEMPLATE.format(
            steps="\n".join(f"{i + 1}. {s}" for i, s in enumerate(evaluation_steps))
        )

    def score(self, input: str, expected_output: str, actual_output: str) -> tuple[bool, str]:
        """Return (passed, reasoning). passed=True iff score==1."""
        user_prompt = _USER_TEMPLATE.format(
            input=input,
            expected_output=expected_output,
            actual_output=actual_output,
        )
        response = self._client.messages.create(
            model=self._model,
            max_tokens=256,
            system=self._system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
            temperature=0,
        )
        raw = response.content[0].text if response.content else "{}"
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            stripped = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            data = json.loads(stripped)
        return int(data.get("score", 0)) == 1, data.get("reasoning", "")
