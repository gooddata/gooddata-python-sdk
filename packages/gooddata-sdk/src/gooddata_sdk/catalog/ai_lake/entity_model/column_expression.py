# (C) 2026 GoodData Corporation
"""SDK model for AI Lake pipe-table ColumnExpression projections."""

from __future__ import annotations

from typing import Literal

import attrs
from gooddata_api_client.model.column_expression import ColumnExpression

ColumnExpressionFunction = Literal["HLL_HASH", "BITMAP_HASH", "BITMAP_HASH64", "TO_BITMAP"]
"""StarRocks transform functions supported in pipe-table column projection overrides."""


@attrs.define(kw_only=True)
class CatalogColumnExpression:
    """Single column projection override for a pipe table.

    Each instance produces ``<function>(<column>) AS <target_column>`` in the
    ``SELECT`` list of the generated ``CREATE PIPE … AS INSERT`` statement.
    Required for AGGREGATE-KEY tables that include native HLL or BITMAP columns
    because StarRocks rejects raw VARBINARY values into those column types.

    Pass a mapping of ``{target_column: CatalogColumnExpression}`` as the
    ``column_expressions`` argument to
    :py:meth:`~gooddata_sdk.catalog.ai_lake.service.CatalogAILakeService.create_pipe_table`.

    Example::

        from gooddata_sdk import CatalogColumnExpression

        exprs = {
            "user_hll": CatalogColumnExpression(column="user_id", function="HLL_HASH"),
            "page_bmp": CatalogColumnExpression(column="page_id", function="TO_BITMAP"),
        }
    """

    column: str
    """Source column produced by parquet schema inference (after ``columnOverrides``)."""

    function: ColumnExpressionFunction
    """StarRocks transform to apply to *column* when projecting it."""

    def as_api_model(self) -> ColumnExpression:
        """Serialize to the auto-generated ``ColumnExpression`` API model."""
        return ColumnExpression(
            column=self.column,
            function=self.function,
            _check_type=False,
        )
