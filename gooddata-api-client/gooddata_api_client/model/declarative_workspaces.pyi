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


class DeclarativeWorkspaces(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    A declarative form of a all workspace layout.
    """


    class MetaOapg:
        required = {
            "workspaces",
            "workspaceDataFilters",
        }
        
        class properties:
            
            
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
                "workspaceDataFilters": workspaceDataFilters,
                "workspaces": workspaces,
            }
    
    workspaces: MetaOapg.properties.workspaces
    workspaceDataFilters: MetaOapg.properties.workspaceDataFilters
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["workspaceDataFilters"]) -> MetaOapg.properties.workspaceDataFilters: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["workspaces"]) -> MetaOapg.properties.workspaces: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["workspaceDataFilters", "workspaces", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["workspaceDataFilters"]) -> MetaOapg.properties.workspaceDataFilters: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["workspaces"]) -> MetaOapg.properties.workspaces: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["workspaceDataFilters", "workspaces", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        workspaces: typing.Union[MetaOapg.properties.workspaces, list, tuple, ],
        workspaceDataFilters: typing.Union[MetaOapg.properties.workspaceDataFilters, list, tuple, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'DeclarativeWorkspaces':
        return super().__new__(
            cls,
            *_args,
            workspaces=workspaces,
            workspaceDataFilters=workspaceDataFilters,
            _configuration=_configuration,
            **kwargs,
        )

from gooddata_api_client.model.declarative_workspace import DeclarativeWorkspace
from gooddata_api_client.model.declarative_workspace_data_filter import DeclarativeWorkspaceDataFilter
