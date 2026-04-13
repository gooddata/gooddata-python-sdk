# (C) 2026 GoodData Corporation
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class TypesMapper(Enum):
    """
    Controls how Arrow column types are mapped to pandas dtypes during conversion.

    DEFAULT       — no remapping; produces float64 and object strings, identical to
                    the JSON execution path. Safe default, fully backward compatible.
    ARROW_STRINGS — strings use Arrow-backed StringDtype (lower memory, faster);
                    all numeric types unchanged. Recommended next step for services.
    CUSTOM        — use the custom_mapping dict passed alongside. Raises ValueError
                    if custom_mapping is not provided.
    """

    DEFAULT = "default"
    ARROW_STRINGS = "arrow_strings"
    CUSTOM = "custom"


@dataclass
class ArrowConfig:
    """
    Arrow IPC conversion configuration for DataFrameFactory.

    Controls *how* Arrow data is converted to a pandas DataFrame. Whether to
    use the Arrow path at all is set via the ``use_arrow`` parameter on
    ``DataFrameFactory`` itself.

    Set once on the factory; applies to every Arrow-path call (for_exec_def,
    for_exec_def_arrow, for_arrow_table, for_exec_result_id).

    Attributes:
        self_destruct: When True, Arrow buffers are freed during conversion,
            reducing peak native memory at the cost of not being able to reuse
            the table after the call. Defaults to False.
        types_mapper: Controls how Arrow types are mapped to pandas dtypes.
            TypesMapper.DEFAULT (default) — no mapping; float64 and object strings,
                identical to the JSON execution path.
            TypesMapper.ARROW_STRINGS — strings use Arrow-backed StringDtype;
                all numeric types unchanged.
            TypesMapper.CUSTOM — uses custom_mapping; raises ValueError if
                custom_mapping is not provided.
        custom_mapping: Arrow type → pandas dtype mapping dict. Only used when
            types_mapper=TypesMapper.CUSTOM, ignored otherwise.
    """

    self_destruct: bool = False
    types_mapper: TypesMapper = TypesMapper.DEFAULT
    custom_mapping: dict | None = field(default=None)
