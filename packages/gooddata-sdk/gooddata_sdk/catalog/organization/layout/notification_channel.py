# (C) 2024 GoodData Corporation
import builtins
from typing import Optional

from attrs import define, field
from gooddata_api_client.model.declarative_notification_channel import DeclarativeNotificationChannel
from gooddata_api_client.model.webhook import Webhook

from gooddata_sdk.catalog.base import Base

# TODO: there is an issue with generated client which causes these two classes to fail
# type in gooddata_api_client/model/declarative_notification_channel_destination.py contains only WEBHOOK as valid value
# @define(auto_attribs=True, kw_only=True)
# class CatalogDefaultSmtp(Base):
#     from_email: Optional[str] = None
#     from_email_name: Optional[str] = None
#
#     @staticmethod
#     def client_class() -> Type[DefaultSmtp]:
#         return DefaultSmtp
#
#
# @define(auto_attribs=True, kw_only=True)
# class CatalogSmtp(Base):
#     from_email: Optional[str] = None
#     from_email_name: Optional[str] = None
#     host: Optional[str] = None
#     password: Optional[str] = None
#     port: Optional[int] = None
#     username: Optional[str] = None
#
#     @staticmethod
#     def client_class() -> Type[Smtp]:
#         return Smtp


@define(auto_attribs=True, kw_only=True)
class CatalogWebhook(Base):
    type: str = field(default="WEBHOOK", init=False)
    url: str
    token: Optional[str] = field(default=None, eq=False)
    has_token: Optional[bool] = field(default=None, eq=False)

    @staticmethod
    def client_class() -> builtins.type[Webhook]:
        return Webhook


@define(auto_attribs=True, kw_only=True)
class CatalogDeclarativeNotificationChannel(Base):
    id: str
    name: Optional[str] = None
    description: Optional[str] = None
    destination_type: Optional[str] = None
    custom_dashboard_url: Optional[str] = None
    allowed_recipients: Optional[str] = None
    # destination: Optional[Union[CatalogDefaultSmtp, CatalogSmtp, CatalogWebhook]] = None
    destination: Optional[CatalogWebhook] = None

    @staticmethod
    def client_class() -> builtins.type[DeclarativeNotificationChannel]:
        return DeclarativeNotificationChannel
