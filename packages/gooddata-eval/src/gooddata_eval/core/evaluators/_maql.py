# (C) 2026 GoodData Corporation
"""MAQL normalisation shared by every metric comparator."""

import re
from typing import Callable

_IFNULL_RE = re.compile(r"IFNULL\s*\(([^,]+),\s*0\)", re.IGNORECASE)
_SELECT_WRAP_RE = re.compile(r"^\s*\(\s*SELECT\s*\{([^}]+)\}\s*\)\s*$", re.IGNORECASE)
_INNER_SELECT_RE = re.compile(r"\(\s*SELECT\s*\{([^}]+)\}\s*\)", re.IGNORECASE)
# Matches whichever comes first: a {type/id} identifier reference or a quoted string
# literal -- both are case-sensitive data and must survive casefolding untouched.
# Everything else in MAQL (keywords, operators, numbers, punctuation) carries no
# case-sensitive meaning, per the MAQL reference (SELECT/BY/WHERE/FOR PREVIOUS/etc.
# are case-insensitive; only {..} identifiers and quoted literal values are not).
# Feeds normalize_maql, the scoring comparator (_best_maql_match) -- do not widen this
# to handle \X escapes without confirming MAQL literals actually support backslash
# escaping (unconfirmed; see PR #1760 review). A wrong guess here silently changes
# maql_correct for the whole eval dataset, not just a hint. _no_where_clause_hint has its
# own, separately-scoped regex for that reason.
_PROTECTED_RE = re.compile(r"\{[^}]*\}|\"[^\"]*\"|'[^']*'")


_MASK_RE = re.compile(r"\x00(\d+)\x00")


def _mask_quoted_literals(s: str) -> tuple[str, list[str]]:
    """Replace quoted string literals with placeholders, returning the text and the literals.

    A literal's contents are data: the IFNULL/SELECT unwrapping and brace-whitespace
    rewrites below must not reach inside one. Splitting on _PROTECTED_RE rather than on
    quotes alone means a quote character inside a {type/id} reference cannot open a bogus
    literal. Brace regions are deliberately left in place -- normalising the whitespace
    inside {..} is exactly what those rewrites are for.
    """
    literals: list[str] = []

    def _replace(match: re.Match) -> str:
        token = match.group(0)
        if token[0] not in "\"'":
            return token
        literals.append(token)
        return f"\x00{len(literals) - 1}\x00"

    return _PROTECTED_RE.sub(_replace, s), literals


def _unmask_quoted_literals(s: str, literals: list[str]) -> str:
    """Put the literals from _mask_quoted_literals back, verbatim."""
    return _MASK_RE.sub(lambda m: literals[int(m.group(1))], s)


def _strip_outer_parens(s: str) -> str:
    """Strip one balanced layer of outer () if they wrap the entire expression."""
    if not (s.startswith("(") and s.endswith(")")):
        return s
    depth = 0
    for i, ch in enumerate(s):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0 and i < len(s) - 1:
                return s  # Closing paren found before end — not a simple outer wrapper
    return s[1:-1].strip()


def apply_outside_protected(s: str, fn: Callable[[str], str]) -> str:
    """Run ``fn`` on the text between ``{..}`` / ``".."`` / ``'..'`` regions only,
    preserving case-sensitive {type/id} identifiers and quoted string literal values."""
    parts: list[str] = []
    last = 0
    for m in _PROTECTED_RE.finditer(s):
        parts.append(fn(s[last : m.start()]))
        parts.append(m.group(0))
        last = m.end()
    parts.append(fn(s[last:]))
    return "".join(parts)


def _tighten_punctuation(seg: str) -> str:
    """Drop whitespace next to parens, commas and operators -- it carries no meaning in MAQL."""
    seg = re.sub(r"\s*\(\s*", "(", seg)
    seg = re.sub(r"\s*\)", ")", seg)
    seg = re.sub(r"\s*,\s*", ",", seg)
    seg = re.sub(r"\s*([-+*/=<>])\s*", r"\1", seg)
    return seg


def normalize_maql(maql: str) -> str:
    """Semantic normalisation: strip whitespace, unwrap IFNULL/SELECT wrappers, casefold
    keywords, tighten punctuation."""
    if not maql:
        return ""
    m, literals = _mask_quoted_literals(maql.strip())
    m = _IFNULL_RE.sub(lambda mo: _strip_outer_parens(mo.group(1).strip()), m)
    m = _SELECT_WRAP_RE.sub(r"{\1}", m)
    m = _INNER_SELECT_RE.sub(r"{\1}", m)
    m = re.sub(r"\{\s+", "{", m)
    m = re.sub(r"\s+\}", "}", m)
    m = re.sub(r"\s+", " ", m)
    normalized = apply_outside_protected(m.strip(), str.lower)
    normalized = apply_outside_protected(normalized, _tighten_punctuation)
    return _unmask_quoted_literals(normalized, literals)
