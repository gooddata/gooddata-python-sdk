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


class DashboardPermissions(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "userGroups",
            "users",
        }
        
        class properties:
            
            
            class userGroups(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['UserGroupPermission']:
                        return UserGroupPermission
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['UserGroupPermission'], typing.List['UserGroupPermission']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'userGroups':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'UserGroupPermission':
                    return super().__getitem__(i)
            
            
            class users(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['UserPermission']:
                        return UserPermission
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['UserPermission'], typing.List['UserPermission']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'users':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'UserPermission':
                    return super().__getitem__(i)
            __annotations__ = {
                "userGroups": userGroups,
                "users": users,
            }
    
    userGroups: MetaOapg.properties.userGroups
    users: MetaOapg.properties.users
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["userGroups"]) -> MetaOapg.properties.userGroups: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["users"]) -> MetaOapg.properties.users: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["userGroups", "users", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["userGroups"]) -> MetaOapg.properties.userGroups: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["users"]) -> MetaOapg.properties.users: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["userGroups", "users", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        userGroups: typing.Union[MetaOapg.properties.userGroups, list, tuple, ],
        users: typing.Union[MetaOapg.properties.users, list, tuple, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'DashboardPermissions':
        return super().__new__(
            cls,
            *_args,
            userGroups=userGroups,
            users=users,
            _configuration=_configuration,
            **kwargs,
        )

from gooddata_api_client.model.user_group_permission import UserGroupPermission
from gooddata_api_client.model.user_permission import UserPermission
