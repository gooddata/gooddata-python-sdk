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


class InlineFilterDefinition(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Filter in form of direct MAQL query.
    """


    class MetaOapg:
        required = {
            "inline",
        }
        
        class properties:
            
            
            class inline(
                schemas.DictSchema
            ):
            
            
                class MetaOapg:
                    required = {
                        "filter",
                    }
                    
                    class properties:
                        applyOnResult = schemas.BoolSchema
                        filter = schemas.StrSchema
                        __annotations__ = {
                            "applyOnResult": applyOnResult,
                            "filter": filter,
                        }
                
                filter: MetaOapg.properties.filter
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["applyOnResult"]) -> MetaOapg.properties.applyOnResult: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["filter"]) -> MetaOapg.properties.filter: ...
                
                @typing.overload
                def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                
                def __getitem__(self, name: typing.Union[typing_extensions.Literal["applyOnResult", "filter", ], str]):
                    # dict_instance[name] accessor
                    return super().__getitem__(name)
                
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["applyOnResult"]) -> typing.Union[MetaOapg.properties.applyOnResult, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["filter"]) -> MetaOapg.properties.filter: ...
                
                @typing.overload
                def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                
                def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["applyOnResult", "filter", ], str]):
                    return super().get_item_oapg(name)
                
            
                def __new__(
                    cls,
                    *_args: typing.Union[dict, frozendict.frozendict, ],
                    filter: typing.Union[MetaOapg.properties.filter, str, ],
                    applyOnResult: typing.Union[MetaOapg.properties.applyOnResult, bool, schemas.Unset] = schemas.unset,
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'inline':
                    return super().__new__(
                        cls,
                        *_args,
                        filter=filter,
                        applyOnResult=applyOnResult,
                        _configuration=_configuration,
                        **kwargs,
                    )
            __annotations__ = {
                "inline": inline,
            }
    
    inline: MetaOapg.properties.inline
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["inline"]) -> MetaOapg.properties.inline: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["inline", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["inline"]) -> MetaOapg.properties.inline: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["inline", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        inline: typing.Union[MetaOapg.properties.inline, dict, frozendict.frozendict, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'InlineFilterDefinition':
        return super().__new__(
            cls,
            *_args,
            inline=inline,
            _configuration=_configuration,
            **kwargs,
        )