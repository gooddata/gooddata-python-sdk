# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any

from gooddata_scan_client.model.scan_request import ScanRequest


class CatalogScanModelRequest:
    def __init__(
        self,
        separator: str = "__",
        scan_tables: bool = True,
        scan_views: bool = False,
        table_prefix: str = None,
        view_prefix: str = None,
    ):
        self.separator = separator
        self.scan_tables = scan_tables
        self.scan_views = scan_views
        self.table_prefix = table_prefix
        self.view_prefix = view_prefix
        if not scan_views and not scan_tables:
            raise ValueError("Either scan_tables or scan_views must be True in CatalogScanModelRequest.")

    def to_api(self) -> ScanRequest:
        kwargs: dict[str, Any] = dict()
        if self.table_prefix:
            kwargs["table_prefix"] = self.table_prefix
        if self.view_prefix:
            kwargs["view_prefix"] = self.view_prefix
        return ScanRequest(separator=self.separator, scan_tables=self.scan_tables, scan_views=self.scan_views, **kwargs)
