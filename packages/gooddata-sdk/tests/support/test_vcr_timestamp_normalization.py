# (C) 2026 GoodData Corporation
from __future__ import annotations

import pytest
from tests_support.vcrpy_utils import _CANONICAL_TIMESTAMP, _normalize_hashes_in_text

_TS = "2026-11-27 10:15"


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        # stdlib JSON
        (f'{{"createdAt": "{_TS}"}}', f'{{"createdAt": "{_CANONICAL_TIMESTAMP}"}}'),
        (f'{{"modifiedAt": "{_TS}"}}', f'{{"modifiedAt": "{_CANONICAL_TIMESTAMP}"}}'),
        # orjson
        (f'{{"createdAt":"{_TS}"}}', f'{{"createdAt":"{_CANONICAL_TIMESTAMP}"}}'),
        (f'{{"modifiedAt":"{_TS}"}}', f'{{"modifiedAt":"{_CANONICAL_TIMESTAMP}"}}'),
        # YAML, top-level, nested and as the first key of a list item
        (f"modifiedAt: {_TS}\n", f"modifiedAt: {_CANONICAL_TIMESTAMP}\n"),
        (f"data:\n  createdAt: {_TS}\n", f"data:\n  createdAt: {_CANONICAL_TIMESTAMP}\n"),
        (f"items:\n  - modifiedAt: {_TS}\n", f"items:\n  - modifiedAt: {_CANONICAL_TIMESTAMP}\n"),
    ],
)
def test_timestamp_fields_are_normalized(text: str, expected: str) -> None:
    assert _normalize_hashes_in_text(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        # The key text inside a string value, in JSON and in YAML
        f'{{"description": "modifiedAt: {_TS}"}}',
        f"description: modifiedAt: {_TS}\n",
        f"description: 'see modifiedAt: {_TS}'\n",
        # A longer key that merely ends with a timestamp key
        f'{{"lastModifiedAt": "{_TS}"}}',
        f'{{"xcreatedAt": "{_TS}"}}',
        f"xcreatedAt: {_TS}\n",
    ],
)
def test_timestamp_text_outside_a_field_is_kept(text: str) -> None:
    assert _normalize_hashes_in_text(text) == text
