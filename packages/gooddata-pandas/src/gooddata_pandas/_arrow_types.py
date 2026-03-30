# (C) 2026 GoodData Corporation
from __future__ import annotations

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
