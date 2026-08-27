# (C) 2024 GoodData Corporation
from __future__ import annotations

import builtins
from typing import Any, Union

from attrs import define, field
from attrs import fields as attrs_fields
from gooddata_api_client.model.declarative_notification_channel import DeclarativeNotificationChannel
from gooddata_api_client.model.default_smtp import DefaultSmtp
from gooddata_api_client.model.in_platform import InPlatform
from gooddata_api_client.model.smtp import Smtp
from gooddata_api_client.model.webhook import Webhook

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.utils import safeget


@define(kw_only=True)
class CatalogWebhook(Base):
    """Webhook destination for notifications."""

    type: str = field(default="WEBHOOK", init=False)
    url: str
    token: str | None = field(default=None, eq=False)
    has_token: bool | None = field(default=None, eq=False)

    @staticmethod
    def client_class() -> builtins.type[Webhook]:
        return Webhook


@define(kw_only=True)
class CatalogSmtp(Base):
    """Custom SMTP destination for notifications.

    `host`, `port`, `username` and `password` are required by the API on create
    and update, but are optional here because reads never return the password.
    """

    type: str = field(default="SMTP", init=False)
    from_email: str | None = None
    from_email_name: str | None = None
    host: str | None = None
    port: int | None = None
    username: str | None = None
    password: str | None = field(default=None, eq=False)

    @staticmethod
    def client_class() -> builtins.type[Smtp]:
        return Smtp


@define(kw_only=True)
class CatalogDefaultSmtp(Base):
    """Default SMTP destination for notifications - the platform's own mail server."""

    type: str = field(default="DEFAULT_SMTP", init=False)
    from_email: str | None = None
    from_email_name: str | None = None

    @staticmethod
    def client_class() -> builtins.type[DefaultSmtp]:
        return DefaultSmtp


@define(kw_only=True)
class CatalogInPlatform(Base):
    """In-platform destination for notifications."""

    type: str = field(default="IN_PLATFORM", init=False)

    @staticmethod
    def client_class() -> builtins.type[InPlatform]:
        return InPlatform


CatalogNotificationChannelDestination = Union[
    CatalogWebhook,
    CatalogSmtp,
    CatalogDefaultSmtp,
    CatalogInPlatform,
]

_DESTINATION_BY_TYPE: dict[str, builtins.type[CatalogNotificationChannelDestination]] = {
    "WEBHOOK": CatalogWebhook,
    "SMTP": CatalogSmtp,
    "DEFAULT_SMTP": CatalogDefaultSmtp,
    "IN_PLATFORM": CatalogInPlatform,
}


def _destination_from_api(data: dict[str, Any]) -> CatalogNotificationChannelDestination:
    """Build the right destination class from a `destination` payload.

    Dispatched on `type` explicitly rather than left to cattrs: the four
    destination classes have no uniquely-required field to disambiguate a
    union on (`IN_PLATFORM` carries nothing but its type).
    """
    destination_type = safeget(data, ["type"])
    destination_class = _DESTINATION_BY_TYPE.get(destination_type)
    if destination_class is None:
        raise ValueError(f"Unknown notification channel destination type: {destination_type}")
    # Keep only what the class can take: `type` is init=False (implied by the
    # class itself) and the API sends fields we do not model - `has_secret_key`
    # on a webhook, for one. Silently ignoring those matches how cattrs used to
    # structure this and keeps reads working when the API grows a field.
    accepted = {f.name for f in attrs_fields(destination_class) if f.init}
    return destination_class(**{k: v for k, v in data.items() if k in accepted})


@define(kw_only=True)
class CatalogDeclarativeNotificationChannel(Base):
    id: str
    name: str | None = None
    description: str | None = None
    destination_type: str | None = None
    custom_dashboard_url: str | None = None
    allowed_recipients: str | None = None
    destination: CatalogNotificationChannelDestination | None = None

    @staticmethod
    def client_class() -> builtins.type[DeclarativeNotificationChannel]:
        return DeclarativeNotificationChannel

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDeclarativeNotificationChannel:
        data = entity if isinstance(entity, dict) else entity.to_dict(camel_case=False)
        raw_destination = safeget(data, ["destination"])
        return cls(
            id=data["id"],
            name=safeget(data, ["name"]),
            description=safeget(data, ["description"]),
            destination_type=safeget(data, ["destination_type"]),
            custom_dashboard_url=safeget(data, ["custom_dashboard_url"]),
            allowed_recipients=safeget(data, ["allowed_recipients"]),
            destination=_destination_from_api(raw_destination) if raw_destination is not None else None,
        )
