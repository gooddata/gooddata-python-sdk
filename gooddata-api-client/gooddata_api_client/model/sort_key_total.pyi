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


class SortKeyTotal(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Sorting rule for sorting by total value. DataColumnLocators are only required if there is ambiguity. Locator for measureGroup is taken from the metric of the total.
    """


    class MetaOapg:
        required = {
            "total",
        }
        
        class properties:
            
            
            class total(
                schemas.DictSchema
            ):
            
            
                class MetaOapg:
                    required = {
                        "totalIdentifier",
                    }
                    
                    class properties:
                    
                        @staticmethod
                        def dataColumnLocators() -> typing.Type['DataColumnLocators']:
                            return DataColumnLocators
                        
                        
                        class direction(
                            schemas.EnumBase,
                            schemas.StrSchema
                        ):
                            
                            @schemas.classproperty
                            def ASC(cls):
                                return cls("ASC")
                            
                            @schemas.classproperty
                            def DESC(cls):
                                return cls("DESC")
                        totalIdentifier = schemas.StrSchema
                        __annotations__ = {
                            "dataColumnLocators": dataColumnLocators,
                            "direction": direction,
                            "totalIdentifier": totalIdentifier,
                        }
                
                totalIdentifier: MetaOapg.properties.totalIdentifier
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["dataColumnLocators"]) -> 'DataColumnLocators': ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["direction"]) -> MetaOapg.properties.direction: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["totalIdentifier"]) -> MetaOapg.properties.totalIdentifier: ...
                
                @typing.overload
                def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                
                def __getitem__(self, name: typing.Union[typing_extensions.Literal["dataColumnLocators", "direction", "totalIdentifier", ], str]):
                    # dict_instance[name] accessor
                    return super().__getitem__(name)
                
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["dataColumnLocators"]) -> typing.Union['DataColumnLocators', schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["direction"]) -> typing.Union[MetaOapg.properties.direction, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["totalIdentifier"]) -> MetaOapg.properties.totalIdentifier: ...
                
                @typing.overload
                def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                
                def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["dataColumnLocators", "direction", "totalIdentifier", ], str]):
                    return super().get_item_oapg(name)
                
            
                def __new__(
                    cls,
                    *_args: typing.Union[dict, frozendict.frozendict, ],
                    totalIdentifier: typing.Union[MetaOapg.properties.totalIdentifier, str, ],
                    dataColumnLocators: typing.Union['DataColumnLocators', schemas.Unset] = schemas.unset,
                    direction: typing.Union[MetaOapg.properties.direction, str, schemas.Unset] = schemas.unset,
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'total':
                    return super().__new__(
                        cls,
                        *_args,
                        totalIdentifier=totalIdentifier,
                        dataColumnLocators=dataColumnLocators,
                        direction=direction,
                        _configuration=_configuration,
                        **kwargs,
                    )
            __annotations__ = {
                "total": total,
            }
    
    total: MetaOapg.properties.total
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["total"]) -> MetaOapg.properties.total: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["total", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["total"]) -> MetaOapg.properties.total: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["total", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        total: typing.Union[MetaOapg.properties.total, dict, frozendict.frozendict, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'SortKeyTotal':
        return super().__new__(
            cls,
            *_args,
            total=total,
            _configuration=_configuration,
            **kwargs,
        )

from gooddata_api_client.model.data_column_locators import DataColumnLocators
