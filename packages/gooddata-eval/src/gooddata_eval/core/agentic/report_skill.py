# (C) 2026 GoodData Corporation. All rights reserved.
"""Deprecated: use ``gooddata_eval.core.agentic.document_skill``."""

import warnings

from gooddata_eval.core.agentic.document_skill import (
    AgenticDocumentSummary as AgenticReportSummary,
)
from gooddata_eval.core.agentic.document_skill import (
    DocumentEvaluation as ReportEvaluation,
)
from gooddata_eval.core.agentic.document_skill import (
    DocumentRunResult as ReportRunResult,
)
from gooddata_eval.core.agentic.document_skill import (
    DocumentSkillAssertionError as ReportSkillAssertionError,
)
from gooddata_eval.core.agentic.document_skill import (
    build_simulated_reply,
)
from gooddata_eval.core.agentic.document_skill import (
    evaluate_agentic_document_skill as evaluate_agentic_report_skill,
)
from gooddata_eval.core.agentic.document_skill import (
    evaluate_document_response as evaluate_report_response,
)
from gooddata_eval.core.agentic.document_skill import (
    render_document_text as render_report_text,
)
from gooddata_eval.core.agentic.document_skill import (
    run_agentic_document_skill as run_agentic_report_skill,
)

warnings.warn(
    "gooddata_eval.core.agentic.report_skill is deprecated; import from gooddata_eval.core.agentic.document_skill",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = [
    "AgenticReportSummary",
    "ReportEvaluation",
    "ReportRunResult",
    "ReportSkillAssertionError",
    "build_simulated_reply",
    "evaluate_agentic_report_skill",
    "evaluate_report_response",
    "render_report_text",
    "run_agentic_report_skill",
]
