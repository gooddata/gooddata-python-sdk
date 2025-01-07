# (C) 2025 GoodData Corporation
"""
An extension of the CT1 rule from gitlint to enforce the conventional commit format.
This version also allows specifying allowed scope values.
"""

import re

from gitlint.options import ListOption
from gitlint.rules import CommitMessageTitle, LineRule, RuleViolation

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
