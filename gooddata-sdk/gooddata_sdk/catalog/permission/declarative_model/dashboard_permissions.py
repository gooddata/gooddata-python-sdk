# (C) 2023 GoodData Corporation
import builtins
from typing import Optional

import attr
from gooddata_api_client.model.dashboard_permissions import DashboardPermissions
from gooddata_api_client.model.granted_permission import GrantedPermission
from gooddata_api_client.model.rule_permission import RulePermission
from gooddata_api_client.model.user_group_permission import UserGroupPermission
from gooddata_api_client.model.user_permission import UserPermission

from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class CatalogGrantedPermission(Base):
    level: str
    source: str

    @staticmethod
    def client_class() -> type[GrantedPermission]:
        return GrantedPermission


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserPermission(Base):
    id: str
    name: Optional[str] = None
    email: Optional[str] = None
    permissions: Optional[list[CatalogGrantedPermission]] = None

    @staticmethod
    def client_class() -> type[UserPermission]:
        return UserPermission


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserGroupPermission(Base):
    id: str
    name: Optional[str] = None
    permissions: Optional[list[CatalogGrantedPermission]] = None

    @staticmethod
    def client_class() -> type[UserGroupPermission]:
        return UserGroupPermission


@attr.s(auto_attribs=True, kw_only=True)
class CatalogRulePermission(Base):
    type: str
    permissions: Optional[list[str]] = None

    @staticmethod
    def client_class() -> builtins.type[RulePermission]:  # noqa: UP006
        return RulePermission


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDashboardPermissions(Base):
    rules: list[CatalogRulePermission]
    user_groups: list[CatalogUserGroupPermission]
    users: list[CatalogUserPermission]

    @staticmethod
    def client_class() -> type[DashboardPermissions]:
        return DashboardPermissions
