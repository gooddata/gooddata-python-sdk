# (C) 2026 GoodData Corporation
"""Unit test: ``Base`` writes keyword-named attributes under the generated client's names.

The generated client names an attribute whose API name is a Python keyword with a
leading underscore (``from`` becomes ``_from``), while an attrs class names it with a
trailing one (``from_``). Only attrs field names are renamed; keys of a ``dict`` value
are user data and pass through as they are.
"""

from __future__ import annotations

from typing import Any

from attrs import define, field
from gooddata_sdk.catalog.base import Base


@define(kw_only=True)
class _Range(Base):
    from_: str
    to: str


@define(kw_only=True)
class _Holder(Base):
    from_: int
    range: _Range
    ranges: list[_Range] = field(factory=list)
    content: dict[str, Any] = field(factory=dict)
    note: str | None = None


def test_top_level_keyword_attribute_is_written_as_client_name() -> None:
    holder = _Holder(from_=-1, range=_Range(from_="2026-01-01", to="2026-01-31"))

    snake = holder.to_dict(camel_case=False)

    assert snake["_from"] == -1
    assert "from_" not in snake


def test_nested_keyword_attribute_is_written_as_client_name() -> None:
    holder = _Holder(
        from_=-1,
        range=_Range(from_="2026-01-01", to="2026-01-31"),
        ranges=[_Range(from_="2026-02-01", to="2026-02-28")],
    )

    snake = holder.to_dict(camel_case=False)

    assert snake["range"] == {"_from": "2026-01-01", "to": "2026-01-31"}
    assert snake["ranges"] == [{"_from": "2026-02-01", "to": "2026-02-28"}]


def test_dict_value_keys_are_not_renamed() -> None:
    content = {"class_": 1, "from_": {"in_": [{"is_": True}]}}
    holder = _Holder(from_=0, range=_Range(from_="a", to="b"), content=content)

    snake = holder.to_dict(camel_case=False)

    assert snake["content"] == content


def test_none_attributes_are_left_out() -> None:
    holder = _Holder(from_=0, range=_Range(from_="a", to="b"))

    snake = holder.to_dict(camel_case=False)

    assert "note" not in snake
