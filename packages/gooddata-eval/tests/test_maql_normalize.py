# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
"""Tests for the shared MAQL normaliser (core/evaluators/_maql.py)."""

import pytest
from gooddata_eval.core.evaluators._maql import normalize_maql

# Pairs that are the SAME MAQL and must compare equal.
EQUIVALENT_PAIRS = [
    pytest.param(
        "SELECT {metric/sales_order_revenue} - "
        "(SELECT {metric/sales_order_revenue} FOR PREVIOUS ({label/transaction_date.month}))",
        "SELECT {metric/sales_order_revenue} - "
        "(SELECT {metric/sales_order_revenue} FOR PREVIOUS({label/transaction_date.month}))",
        id="qa29226-b6fe30e7-space-before-paren",
    ),
    pytest.param("FOR PREVIOUS ({label/x})", "FOR PREVIOUS({label/x})", id="space-before-paren"),
    pytest.param("THIS(QUARTER, -1)", "THIS(QUARTER,-1)", id="space-after-comma"),
    pytest.param("{metric/a} / {metric/b}", "{metric/a}/{metric/b}", id="spaces-around-operator"),
    pytest.param('{label/y} = "2025"', '{label/y}="2025"', id="spaces-around-equals"),
]


@pytest.mark.parametrize(("left", "right"), EQUIVALENT_PAIRS)
def test_whitespace_around_punctuation_is_not_semantic(left, right):
    assert normalize_maql(left) == normalize_maql(right)


def test_punctuation_inside_a_quoted_literal_survives():
    maql = 'SELECT {metric/x} WHERE {label/account} = "Acme (Inc), Ltd"'
    assert '"Acme (Inc), Ltd"' in normalize_maql(maql)


def test_whitespace_inside_a_quoted_literal_is_not_collapsed():
    assert normalize_maql('WHERE {label/x} = "A  B"') != normalize_maql('WHERE {label/x} = "A B"')


def test_whitespace_outside_literals_is_still_collapsed():
    assert normalize_maql("SELECT   {metric/a}\n\n  BY  {label/b}") == normalize_maql("SELECT {metric/a} BY {label/b}")


def test_distinct_quoted_literals_still_differ():
    assert normalize_maql('WHERE {label/x} = "A (1)"') != normalize_maql('WHERE {label/x} = "A(1)"')


def test_ifnull_tolerates_whitespace_before_its_paren():
    assert normalize_maql("IFNULL ({metric/a}, 0)") == normalize_maql("IFNULL({metric/a}, 0)")


def test_wrapper_syntax_inside_a_quoted_literal_is_not_unwrapped():
    maql = 'WHERE {label/x} = "IFNULL({metric/y}, 0)"'
    assert '"IFNULL({metric/y}, 0)"' in normalize_maql(maql)


def test_braces_inside_a_quoted_literal_keep_their_whitespace():
    maql = 'WHERE {label/x} = "a { b }"'
    assert '"a { b }"' in normalize_maql(maql)
    assert normalize_maql(maql) != normalize_maql('WHERE {label/x} = "a {b}"')


def test_strips_whitespace():
    assert normalize_maql("  SELECT  { metric/foo }  ") == "select {metric/foo}"


def test_removes_select_wrapper():
    assert normalize_maql("(SELECT {metric/abc})") == "{metric/abc}"


def test_is_case_insensitive_for_keywords():
    """Regression test for a live-reproduced bug: 'FOR PREVIOUS(...)' vs
    'FOR Previous(...)' scored as a mismatch even though MAQL keywords are
    case-insensitive -- a semantically identical agent answer failed the eval
    purely on keyword casing."""
    actual = "SELECT {metric/active_card_count_-_txn_-_cutcgco} FOR PREVIOUS({label/process_date.year})"
    expected = "SELECT {metric/active_card_count_-_txn_-_cutcgco}\n  FOR Previous({label/process_date.year})"
    assert normalize_maql(actual) == normalize_maql(expected)


def test_preserves_identifier_case():
    # {type/id} references are real, case-sensitive ids -- must never be casefolded.
    assert "Mixed_Case_Id" in normalize_maql("SELECT {metric/Mixed_Case_Id}")


def test_preserves_quoted_literal_case():
    """The bug this guards against: naively lowercasing everything outside {..}
    would also lowercase quoted WHERE-clause literal values, which are real,
    case-sensitive data -- not keywords. Two literals differing only in case
    must NOT be treated as equal; that would be a false positive."""
    assert normalize_maql('WHERE {label/status} = "Active"') != normalize_maql('WHERE {label/status} = "active"')


def test_does_not_consume_escape_sequences():
    """PR #1760 review (Henry): _PROTECTED_RE feeds this comparator, so it must NOT treat
    \\X as an escape sequence unless MAQL literals are confirmed to support backslash
    escaping (unconfirmed). A `\\"` inside a literal must still end that literal at the
    next real quote -- not swallow everything up to the following quoted value, which
    would leave a real keyword like AND uncasefolded and a later literal's case wrongly
    casefolded."""
    maql = 'SELECT {metric/x} WHERE {label/path} = "C:\\" AND {label/y} = "Active"'
    normalized = normalize_maql(maql)
    assert "and {label/y}" in normalized  # AND is a keyword outside the literal -- casefolded
    assert '"Active"' in normalized  # the second literal's case is untouched -- not "active"


def test_empty_input():
    assert normalize_maql("") == ""
