# (C) 2024 GoodData Corporation
from __future__ import annotations

from typing import Any

import attrs


@attrs.define(kw_only=True)
class ExecutionResultLimitBreak:
    """Describes a limit that was broken, resulting in partial data being returned.

    When the server truncates execution results because a configured threshold was
    exceeded, it returns one or more ``ExecutionResultLimitBreak`` objects inside
    ``ExecutionResult.metadata["limitBreaks"]``.  Use :meth:`from_dict` to convert
    each raw dict entry into a typed instance.

    Example::

        result = execution.read_result(limit=10000)
        raw_breaks = result.metadata.get("limitBreaks") or []
        limit_breaks = [ExecutionResultLimitBreak.from_dict(lb) for lb in raw_breaks]
        if limit_breaks:
            print("Result is partial!")
            for lb in limit_breaks:
                print(f"  {lb.limit_type}: value={lb.value}, limit={lb.limit}")
    """

    limit: int
    """The configured threshold value."""

    limit_type: str
    """Type of the limit that was broken, e.g. ``"rowCount"``."""

    value: int | None = None
    """The actual value that triggered the limit; ``None`` when it cannot be determined exactly."""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ExecutionResultLimitBreak:
        """Create an :class:`ExecutionResultLimitBreak` from a raw API response dict.

        Args:
            data: A single item from the ``limitBreaks`` list in the execution result
                metadata, as returned by the GoodData API.

        Returns:
            A typed :class:`ExecutionResultLimitBreak` instance.
        """
        return cls(
            limit=data["limit"],
            limit_type=data["limitType"],
            value=data.get("value"),
        )
