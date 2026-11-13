# (C) 2026 GoodData Corporation
"""gooddata-eval: evaluate the GoodData AI agent against your own datasets."""

from gooddata_eval._version import __version__
from gooddata_eval.core.outcome import (
    ErrorSource,
    EvalHarnessError,
    Outcome,
    OutcomeStatus,
    outcome_from_loop_exit,
)

__all__ = [
    "ErrorSource",
    "EvalHarnessError",
    "Outcome",
    "OutcomeStatus",
    "__version__",
    "outcome_from_loop_exit",
]
