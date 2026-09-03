# (C) 2026 GoodData Corporation
"""Validated run configuration produced by the CLI and consumed by the runner."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, cast, get_args

# Values that mean "off" when read from the environment. Needed because every non-empty
# string is truthy in Python, so a bare bool() on an env var reads FOO=0 -- the obvious way
# to write "off" -- as ON.
_ENV_FALSE = frozenset({"", "0", "false", "no", "off"})


def env_flag(name: str) -> bool:
    """True only when the variable is set to something that does not mean "off"."""
    return os.environ.get(name, "").strip().lower() not in _ENV_FALSE


# The judge model, overridable for comparison experiments. The default is deliberate on
# two counts: gpt-4o honours temperature=0, so a given response always gets the same
# verdict; and it is NOT the family under test, so the judge is not grading its own
# output. Changing it trades one or both of those away -- see LLMJudge.score.
JUDGE_MODEL_ENV_VAR = "GD_EVAL_JUDGE_MODEL"
DEFAULT_JUDGE_MODEL = "gpt-4o"


def judge_model() -> str:
    """The LLM-as-judge model, from the environment or the default."""
    return os.environ.get(JUDGE_MODEL_ENV_VAR, "").strip() or DEFAULT_JUDGE_MODEL


ReasoningEffort = Literal["LOW", "MEDIUM", "HIGH"]
"""Effort values the AI chat endpoint accepts, uppercase as the server enum requires."""


def normalize_reasoning_effort(value: str | None) -> ReasoningEffort | None:
    """Canonical effort, or None when unset.

    The `Literal` above only constrains static callers, so normalize once at the
    boundary: without it a lowercase value reaches the endpoint and is rejected as
    an out-of-enum request, while an empty string is sent yet skipped by the
    truthiness checks in the Langfuse writers — leaving a run whose recorded
    identity disagrees with what it actually requested.
    """
    if value is None:
        return None
    candidate = value.strip().upper()
    if not candidate:
        return None
    if candidate not in get_args(ReasoningEffort):
        raise ValueError(f"Invalid reasoning effort {value!r}; expected one of {', '.join(get_args(ReasoningEffort))}.")
    return cast("ReasoningEffort", candidate)


@dataclass
class RunConfig:
    host: str
    token: str
    workspace_id: str
    dataset_folder: Path | None = None
    langfuse_dataset: str | None = None
    models: list[str] = field(default_factory=list)
    runs: int = 2
    concurrency: int = 1
    json_path: Path | None = None
    log_to_langfuse: bool = False
    quiet: bool = False
    kind: str = "visualization"
    preserve_failed: bool = False
    reasoning_effort: ReasoningEffort | None = None
    agent_id: str | None = None
