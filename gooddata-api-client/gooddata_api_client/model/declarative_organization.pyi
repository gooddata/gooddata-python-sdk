# coding: utf-8

"""
    OpenAPI definition

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v0
    Contact: support@gooddata.com
    Generated by: https://openapi-generator.tech
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from gooddata_api_client import schemas  # noqa: F401


class DeclarativeOrganization(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Complete definition of an organization in a declarative form.
    """


    class MetaOapg:
        required = {
            "organization",
        }
        
        class properties:
        
            @staticmethod
            def organization() -> typing.Type['DeclarativeOrganizationInfo']:
                return DeclarativeOrganizationInfo
            
            
            class dataSources(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['DeclarativeDataSource']:
                        return DeclarativeDataSource
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['DeclarativeDataSource'], typing.List['DeclarativeDataSource']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'dataSources':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'DeclarativeDataSource':
                    return super().__getitem__(i)
            
            
            class userGroups(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['DeclarativeUserGroup']:
                        return DeclarativeUserGroup
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['DeclarativeUserGroup'], typing.List['DeclarativeUserGroup']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'userGroups':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'DeclarativeUserGroup':
                    return super().__getitem__(i)
            
            
            class users(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['DeclarativeUser']:
                        return DeclarativeUser
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['DeclarativeUser'], typing.List['DeclarativeUser']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'users':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'DeclarativeUser':
                    return super().__getitem__(i)
            
            
            class workspaceDataFilters(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['DeclarativeWorkspaceDataFilter']:
                        return DeclarativeWorkspaceDataFilter
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['DeclarativeWorkspaceDataFilter'], typing.List['DeclarativeWorkspaceDataFilter']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'workspaceDataFilters':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'DeclarativeWorkspaceDataFilter':
                    return super().__getitem__(i)
            
            
            class workspaces(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['DeclarativeWorkspace']:
                        return DeclarativeWorkspace
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['DeclarativeWorkspace'], typing.List['DeclarativeWorkspace']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'workspaces':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'DeclarativeWorkspace':
                    return super().__getitem__(i)
            __annotations__ = {
                "organization": organization,
                "dataSources": dataSources,
                "userGroups": userGroups,
                "users": users,
                "workspaceDataFilters": workspaceDataFilters,
                "workspaces": workspaces,
            }
    
    organization: 'DeclarativeOrganizationInfo'
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["organization"]) -> 'DeclarativeOrganizationInfo': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["dataSources"]) -> MetaOapg.properties.dataSources: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["userGroups"]) -> MetaOapg.properties.userGroups: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["users"]) -> MetaOapg.properties.users: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["workspaceDataFilters"]) -> MetaOapg.properties.workspaceDataFilters: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["workspaces"]) -> MetaOapg.properties.workspaces: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["organization", "dataSources", "userGroups", "users", "workspaceDataFilters", "workspaces", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["organization"]) -> 'DeclarativeOrganizationInfo': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["dataSources"]) -> typing.Union[MetaOapg.properties.dataSources, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["userGroups"]) -> typing.Union[MetaOapg.properties.userGroups, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["users"]) -> typing.Union[MetaOapg.properties.users, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["workspaceDataFilters"]) -> typing.Union[MetaOapg.properties.workspaceDataFilters, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["workspaces"]) -> typing.Union[MetaOapg.properties.workspaces, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["organization", "dataSources", "userGroups", "users", "workspaceDataFilters", "workspaces", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        organization: 'DeclarativeOrganizationInfo',
        dataSources: typing.Union[MetaOapg.properties.dataSources, list, tuple, schemas.Unset] = schemas.unset,
        userGroups: typing.Union[MetaOapg.properties.userGroups, list, tuple, schemas.Unset] = schemas.unset,
        users: typing.Union[MetaOapg.properties.users, list, tuple, schemas.Unset] = schemas.unset,
        workspaceDataFilters: typing.Union[MetaOapg.properties.workspaceDataFilters, list, tuple, schemas.Unset] = schemas.unset,
        workspaces: typing.Union[MetaOapg.properties.workspaces, list, tuple, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'DeclarativeOrganization':
        return super().__new__(
            cls,
            *_args,
            organization=organization,
            dataSources=dataSources,
            userGroups=userGroups,
            users=users,
            workspaceDataFilters=workspaceDataFilters,
            workspaces=workspaces,
            _configuration=_configuration,
            **kwargs,
        )

from gooddata_api_client.model.declarative_data_source import DeclarativeDataSource
from gooddata_api_client.model.declarative_organization_info import DeclarativeOrganizationInfo
from gooddata_api_client.model.declarative_user import DeclarativeUser
from gooddata_api_client.model.declarative_user_group import DeclarativeUserGroup
from gooddata_api_client.model.declarative_workspace import DeclarativeWorkspace
from gooddata_api_client.model.declarative_workspace_data_filter import DeclarativeWorkspaceDataFilter
