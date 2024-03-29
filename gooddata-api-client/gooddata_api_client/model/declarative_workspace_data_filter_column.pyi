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


class DeclarativeWorkspaceDataFilterColumn(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "dataType",
            "name",
        }
        
        class properties:
            
            
            class dataType(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def INT(cls):
                    return cls("INT")
                
                @schemas.classproperty
                def STRING(cls):
                    return cls("STRING")
                
                @schemas.classproperty
                def DATE(cls):
                    return cls("DATE")
                
                @schemas.classproperty
                def NUMERIC(cls):
                    return cls("NUMERIC")
                
                @schemas.classproperty
                def TIMESTAMP(cls):
                    return cls("TIMESTAMP")
                
                @schemas.classproperty
                def TIMESTAMP_TZ(cls):
                    return cls("TIMESTAMP_TZ")
                
                @schemas.classproperty
                def BOOLEAN(cls):
                    return cls("BOOLEAN")
            name = schemas.StrSchema
            __annotations__ = {
                "dataType": dataType,
                "name": name,
            }
    
    dataType: MetaOapg.properties.dataType
    name: MetaOapg.properties.name
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["dataType"]) -> MetaOapg.properties.dataType: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["dataType", "name", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["dataType"]) -> MetaOapg.properties.dataType: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["dataType", "name", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        dataType: typing.Union[MetaOapg.properties.dataType, str, ],
        name: typing.Union[MetaOapg.properties.name, str, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'DeclarativeWorkspaceDataFilterColumn':
        return super().__new__(
            cls,
            *_args,
            dataType=dataType,
            name=name,
            _configuration=_configuration,
            **kwargs,
        )
