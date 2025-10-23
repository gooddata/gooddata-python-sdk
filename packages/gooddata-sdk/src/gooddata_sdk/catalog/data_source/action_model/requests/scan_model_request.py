# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any, Optional

import attr
from attr import field
from gooddata_api_client.model.scan_request import ScanRequest

from gooddata_sdk.catalog.base import Base


def one_scan_true(instance: CatalogScanModelRequest, *args: Any) -> None:
    if not instance.scan_views and not instance.scan_tables:
        raise ValueError("Either scan_tables or scan_views must be True in CatalogScanModelRequest.")


@attr.s(auto_attribs=True, kw_only=True)
class CatalogScanModelRequest(Base):
    separator: str = "__"
    scan_tables: bool = field(default=True, validator=one_scan_true)
    scan_views: bool = field(default=False, validator=one_scan_true)
    table_prefix: Optional[str] = None
    view_prefix: Optional[str] = None
    schemata: Optional[list[str]] = None

    @staticmethod
    def client_class() -> type[ScanRequest]:
        return ScanRequest
