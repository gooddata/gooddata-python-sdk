# (C) 2025 GoodData Corporation
from typing import Optional

from attrs import define


@define
class CatalogRunningSection:
    left: Optional[str] = None
    right: Optional[str] = None
