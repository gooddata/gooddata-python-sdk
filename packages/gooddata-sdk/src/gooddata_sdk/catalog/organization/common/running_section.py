# (C) 2025 GoodData Corporation

from attrs import define


@define
class CatalogRunningSection:
    left: str | None = None
    right: str | None = None
