# (C) 2025 GoodData Corporation
"""Gitlint rules for this repository's commit format.

``ConventionalCommit`` extends gitlint's CT1 with an allowed-scope list.
``CommitTrailers`` requires the ``risk:`` trailer and constrains ``jira:``.
"""

import re

from gitlint.options import ListOption, StrOption
from gitlint.rules import CommitMessageTitle, CommitRule, LineRule, RuleViolation

RULE_REGEX = re.compile(r"([^(]+?)(?:\(([^)]+?)\))?!?: .+")

DEFAULT_TYPES = [
    "fix",
    "feat",
    "chore",
    "docs",
    "style",
    "refactor",
    "perf",
    "test",
    "revert",
    "ci",
    "build",
]
DEFAULT_SCOPES = []


class ConventionalCommit(LineRule):
    """This rule enforces the spec at https://www.conventionalcommits.org/."""

    name = "gdc-title-conventional-commits"
    id = "GD1"
    target = CommitMessageTitle

    options_spec = [
        ListOption(
            "types",
            DEFAULT_TYPES,
            "Comma separated list of allowed commit types.",
        ),
        ListOption(
            "scopes",
            DEFAULT_SCOPES,
            "Comma separated list of allowed commit scopes.",
        ),
    ]

    def validate(self, line, _commit):
        violations = []
        match = RULE_REGEX.match(line)

        if not match:
            msg = "Title does not follow ConventionalCommits.org format 'type(optional-scope): description'"
            violations.append(RuleViolation(self.id, msg, line))
        else:
            line_commit_type = match.group(1)
            line_commit_scope = match.group(2)
            if line_commit_type not in self.options["types"].value:
                opt_str = ", ".join(self.options["types"].value)
                violations.append(RuleViolation(self.id, f"Title does not start with one of {opt_str}", line))
            if line_commit_scope and line_commit_scope not in self.options["scopes"].value:
                opt_str = ", ".join(self.options["scopes"].value)
                violations.append(RuleViolation(self.id, f"Scope is defined and is not one of {opt_str}", line))

        return violations


TRAILER_RISK_RE = re.compile(r"^risk: (.+)$")
TRAILER_JIRA_RE = re.compile(r"^jira: (.+)$")
JIRA_TICKET_RE = re.compile(r"^[A-Z][A-Z0-9]+-[0-9]+$")


def _last_paragraph(message: str) -> list[str]:
    """Lines of the message's final non-empty paragraph.

    Git reads trailers from the last paragraph only, so a `risk:` line separated from the
    others by a blank line -- typically one left above a trailing `Co-Authored-By:` -- is
    present in the message but not a trailer.
    """
    paragraphs = [p for p in re.split(r"\n\s*\n", message) if p.strip()]
    if not paragraphs:
        return []
    return [line.strip() for line in paragraphs[-1].splitlines() if line.strip()]


class CommitTrailers(CommitRule):
    """Requires a `risk:` trailer and constrains `jira:` to a ticket or the placeholder."""

    name = "gdc-commit-trailers"
    id = "GD2"

    options_spec = [
        ListOption(
            "risk-values",
            ["nonprod", "low", "high"],
            "Comma separated list of accepted risk levels.",
        ),
        StrOption(
            "ticket-placeholder",
            "trivial",
            "Value of the jira trailer meaning 'no ticket applies'.",
        ),
    ]

    def validate(self, commit):
        violations = []
        message = commit.message.full
        lines = [line.strip() for line in message.splitlines() if line.strip()]
        trailers = _last_paragraph(message)

        risk_lines = [line for line in lines if TRAILER_RISK_RE.match(line)]
        risk_trailers = [line for line in trailers if TRAILER_RISK_RE.match(line)]
        accepted_risks = self.options["risk-values"].value

        if not risk_lines:
            opt_str = "|".join(accepted_risks)
            violations.append(RuleViolation(self.id, f"Missing 'risk: {opt_str}' trailer", None))
        elif len(risk_lines) > 1:
            violations.append(
                RuleViolation(self.id, f"Only one 'risk:' line is allowed (found {len(risk_lines)})", None)
            )
        else:
            value = TRAILER_RISK_RE.match(risk_lines[0]).group(1)
            if value not in accepted_risks:
                opt_str = ", ".join(accepted_risks)
                violations.append(RuleViolation(self.id, f"Risk '{value}' is not one of {opt_str}", risk_lines[0]))
            elif not risk_trailers:
                violations.append(
                    RuleViolation(
                        self.id,
                        "The 'risk:' line is outside the trailer block; keep it in the last "
                        "paragraph, with no blank line before a trailing Co-Authored-By",
                        risk_lines[0],
                    )
                )

        jira_lines = [line for line in lines if TRAILER_JIRA_RE.match(line)]
        placeholder = self.options["ticket-placeholder"].value

        if not jira_lines:
            violations.append(
                RuleViolation(
                    self.id,
                    f"Missing 'jira:' trailer -- a ticket id, or 'jira: {placeholder}' when none applies",
                    None,
                )
            )
        elif len(jira_lines) > 1:
            violations.append(
                RuleViolation(self.id, f"Only one 'jira:' line is allowed (found {len(jira_lines)})", None)
            )
        else:
            value = TRAILER_JIRA_RE.match(jira_lines[0]).group(1)
            if value != placeholder and not JIRA_TICKET_RE.match(value):
                violations.append(
                    RuleViolation(
                        self.id,
                        f"Jira trailer must be a ticket id (e.g. 'jira: STL-123') or 'jira: {placeholder}'",
                        jira_lines[0],
                    )
                )
            elif not [line for line in trailers if TRAILER_JIRA_RE.match(line)]:
                violations.append(
                    RuleViolation(
                        self.id,
                        "The 'jira:' line is outside the trailer block; keep it next to 'risk:'",
                        jira_lines[0],
                    )
                )

        return violations
