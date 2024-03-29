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


class DeclarativeCustomApplicationSetting(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Custom application setting and its value.
    """


    class MetaOapg:
        required = {
            "id",
            "applicationName",
            "content",
        }
        
        class properties:
            
            
            class applicationName(
                schemas.StrSchema
            ):
                pass
            content = schemas.DictSchema
            
            
            class id(
                schemas.StrSchema
            ):
                pass
            __annotations__ = {
                "applicationName": applicationName,
                "content": content,
                "id": id,
            }
    
    id: MetaOapg.properties.id
    applicationName: MetaOapg.properties.applicationName
    content: MetaOapg.properties.content
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["applicationName"]) -> MetaOapg.properties.applicationName: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["content"]) -> MetaOapg.properties.content: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["applicationName", "content", "id", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["applicationName"]) -> MetaOapg.properties.applicationName: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["content"]) -> MetaOapg.properties.content: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["applicationName", "content", "id", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        id: typing.Union[MetaOapg.properties.id, str, ],
        applicationName: typing.Union[MetaOapg.properties.applicationName, str, ],
        content: typing.Union[MetaOapg.properties.content, dict, frozendict.frozendict, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'DeclarativeCustomApplicationSetting':
        return super().__new__(
            cls,
            *_args,
            id=id,
            applicationName=applicationName,
            content=content,
            _configuration=_configuration,
            **kwargs,
        )
