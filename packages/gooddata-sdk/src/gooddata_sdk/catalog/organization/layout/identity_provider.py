# (C) 2024 GoodData Corporation
import builtins

import attr
from gooddata_api_client.model.declarative_identity_provider import DeclarativeIdentityProvider

from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeIdentityProvider(Base):
    id: str
    custom_claim_mapping: dict[str, str] | None = None
    identifiers: list[str] | None = None
    oauth_client_id: str | None = None
    oauth_client_secret: str | None = None
    oauth_issuer_location: str | None = None
    saml_metadata: str | None = None
    idp_type: str | None = None
    oauth_issuer_id: str | None = None
    oauth_subject_id_claim: str | None = None
    oauth_custom_auth_attributes: dict[str, str] | None = None
    oauth_custom_scopes: list[str] | None = None

    @staticmethod
    def client_class() -> builtins.type[DeclarativeIdentityProvider]:
        return DeclarativeIdentityProvider
