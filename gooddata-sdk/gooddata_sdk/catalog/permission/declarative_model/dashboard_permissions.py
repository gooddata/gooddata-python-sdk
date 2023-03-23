# (C) 2023 GoodData Corporation
from typing import List, Optional, Type

import attr

from gooddata_api_client.model.dashboard_permissions import DashboardPermissions
from gooddata_api_client.model.granted_permission import GrantedPermission
from gooddata_api_client.model.user_group_permission import UserGroupPermission
from gooddata_api_client.model.user_permission import UserPermission
from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class CatalogGrantedPermission(Base):
    level: str
    source: str

    @staticmethod
    def client_class() -> Type[GrantedPermission]:
        return GrantedPermission


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserPermission(Base):
    id: str
    name: Optional[str] = None
    email: Optional[str] = None
    permissions: Optional[List[CatalogGrantedPermission]] = None

    @staticmethod
    def client_class() -> Type[UserPermission]:
        return UserPermission


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserGroupPermission(Base):
    id: str
    name: Optional[str] = None
    permissions: Optional[List[CatalogGrantedPermission]] = None

    @staticmethod
    def client_class() -> Type[UserGroupPermission]:
        return UserGroupPermission


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDashboardPermissions(Base):
    user_groups: List[CatalogUserGroupPermission]
    users: List[CatalogUserPermission]

    @staticmethod
    def client_class() -> Type[DashboardPermissions]:
        return DashboardPermissions
