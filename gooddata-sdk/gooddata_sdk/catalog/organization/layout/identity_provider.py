# (C) 2024 GoodData Corporation
import builtins
from typing import Optional

import attr
from gooddata_api_client.model.declarative_identity_provider import DeclarativeIdentityProvider

from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeIdentityProvider(Base):
    id: str
    custom_claim_mapping: Optional[dict[str, str]] = None
    identifiers: Optional[list[str]] = None
    oauth_client_id: Optional[str] = None
    oauth_client_secret: Optional[str] = None
    oauth_issuer_location: Optional[str] = None
    saml_metadata: Optional[str] = None

    @staticmethod
    def client_class() -> builtins.type[DeclarativeIdentityProvider]:
        return DeclarativeIdentityProvider
