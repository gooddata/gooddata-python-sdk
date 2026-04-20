# (C) 2024 GoodData Corporation
from __future__ import annotations

from typing import Any, Literal

import attrs
from gooddata_api_client.model.set_certification_request import SetCertificationRequest

from gooddata_sdk.catalog.base import Base

CertificationStatus = Literal["CERTIFIED"]


@attrs.define(kw_only=True)
class CatalogSetCertificationRequest(Base):
    """Request to set or clear the certification status of an analytics object.

    Pass ``status=None`` to remove the certification from the object.
    Pass ``status="CERTIFIED"`` (the default) to certify it.
    """

    id: str
    type: str
    message: str | None = None
    status: str | None = "CERTIFIED"

    @staticmethod
    def client_class() -> type[SetCertificationRequest]:
        return SetCertificationRequest

    def as_api_model(self) -> SetCertificationRequest:
        kwargs: dict[str, Any] = {}
        if self.message is not None:
            kwargs["message"] = self.message
        # status=None means "clear certification" — always forward it so the
        # caller can explicitly remove a previously set status.
        kwargs["status"] = self.status
        return SetCertificationRequest(
            id=self.id,
            type=self.type,
            _check_type=False,
            **kwargs,
        )
