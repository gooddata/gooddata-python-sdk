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


class DeclarativeUserGroups(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Declarative form of userGroups and its properties.
    """


    class MetaOapg:
        required = {
            "userGroups",
        }
        
        class properties:
            
            
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
            __annotations__ = {
                "userGroups": userGroups,
            }
    
    userGroups: MetaOapg.properties.userGroups
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["userGroups"]) -> MetaOapg.properties.userGroups: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["userGroups", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["userGroups"]) -> MetaOapg.properties.userGroups: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["userGroups", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        userGroups: typing.Union[MetaOapg.properties.userGroups, list, tuple, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'DeclarativeUserGroups':
        return super().__new__(
            cls,
            *_args,
            userGroups=userGroups,
            _configuration=_configuration,
            **kwargs,
        )

from gooddata_api_client.model.declarative_user_group import DeclarativeUserGroup
