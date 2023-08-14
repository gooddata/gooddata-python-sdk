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


class Total(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Definition of a total. There are two types of totals: grand totals and subtotals. Grand total data will be returned in a separate section of the result structure while subtotals are fully integrated into the main result data. The mechanism for this distinction is automatic and it's described in `TotalDimension`
    """


    class MetaOapg:
        required = {
            "metric",
            "totalDimensions",
            "function",
            "localIdentifier",
        }
        
        class properties:
            
            
            class function(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def SUM(cls):
                    return cls("SUM")
                
                @schemas.classproperty
                def MIN(cls):
                    return cls("MIN")
                
                @schemas.classproperty
                def MAX(cls):
                    return cls("MAX")
                
                @schemas.classproperty
                def AVG(cls):
                    return cls("AVG")
                
                @schemas.classproperty
                def MED(cls):
                    return cls("MED")
            localIdentifier = schemas.StrSchema
            metric = schemas.StrSchema
            
            
            class totalDimensions(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['TotalDimension']:
                        return TotalDimension
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['TotalDimension'], typing.List['TotalDimension']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'totalDimensions':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'TotalDimension':
                    return super().__getitem__(i)
            __annotations__ = {
                "function": function,
                "localIdentifier": localIdentifier,
                "metric": metric,
                "totalDimensions": totalDimensions,
            }
    
    metric: MetaOapg.properties.metric
    totalDimensions: MetaOapg.properties.totalDimensions
    function: MetaOapg.properties.function
    localIdentifier: MetaOapg.properties.localIdentifier
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["function"]) -> MetaOapg.properties.function: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["localIdentifier"]) -> MetaOapg.properties.localIdentifier: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["metric"]) -> MetaOapg.properties.metric: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["totalDimensions"]) -> MetaOapg.properties.totalDimensions: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["function", "localIdentifier", "metric", "totalDimensions", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["function"]) -> MetaOapg.properties.function: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["localIdentifier"]) -> MetaOapg.properties.localIdentifier: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["metric"]) -> MetaOapg.properties.metric: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["totalDimensions"]) -> MetaOapg.properties.totalDimensions: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["function", "localIdentifier", "metric", "totalDimensions", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        metric: typing.Union[MetaOapg.properties.metric, str, ],
        totalDimensions: typing.Union[MetaOapg.properties.totalDimensions, list, tuple, ],
        function: typing.Union[MetaOapg.properties.function, str, ],
        localIdentifier: typing.Union[MetaOapg.properties.localIdentifier, str, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'Total':
        return super().__new__(
            cls,
            *_args,
            metric=metric,
            totalDimensions=totalDimensions,
            function=function,
            localIdentifier=localIdentifier,
            _configuration=_configuration,
            **kwargs,
        )

from gooddata_api_client.model.total_dimension import TotalDimension