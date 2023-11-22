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


class JsonApiWorkspaceDataFilterPatch(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    JSON:API representation of patching workspaceDataFilter entity.
    """


    class MetaOapg:
        required = {
            "id",
            "type",
        }
        
        class properties:
            
            
            class id(
                schemas.StrSchema
            ):
                pass
            
            
            class type(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def WORKSPACE_DATA_FILTER(cls):
                    return cls("workspaceDataFilter")
            
            
            class attributes(
                schemas.DictSchema
            ):
            
            
                class MetaOapg:
                    
                    class properties:
                        
                        
                        class columnName(
                            schemas.StrSchema
                        ):
                            pass
                        
                        
                        class description(
                            schemas.StrSchema
                        ):
                            pass
                        
                        
                        class title(
                            schemas.StrSchema
                        ):
                            pass
                        __annotations__ = {
                            "columnName": columnName,
                            "description": description,
                            "title": title,
                        }
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["columnName"]) -> MetaOapg.properties.columnName: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["description"]) -> MetaOapg.properties.description: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["title"]) -> MetaOapg.properties.title: ...
                
                @typing.overload
                def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                
                def __getitem__(self, name: typing.Union[typing_extensions.Literal["columnName", "description", "title", ], str]):
                    # dict_instance[name] accessor
                    return super().__getitem__(name)
                
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["columnName"]) -> typing.Union[MetaOapg.properties.columnName, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["description"]) -> typing.Union[MetaOapg.properties.description, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["title"]) -> typing.Union[MetaOapg.properties.title, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                
                def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["columnName", "description", "title", ], str]):
                    return super().get_item_oapg(name)
                
            
                def __new__(
                    cls,
                    *_args: typing.Union[dict, frozendict.frozendict, ],
                    columnName: typing.Union[MetaOapg.properties.columnName, str, schemas.Unset] = schemas.unset,
                    description: typing.Union[MetaOapg.properties.description, str, schemas.Unset] = schemas.unset,
                    title: typing.Union[MetaOapg.properties.title, str, schemas.Unset] = schemas.unset,
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'attributes':
                    return super().__new__(
                        cls,
                        *_args,
                        columnName=columnName,
                        description=description,
                        title=title,
                        _configuration=_configuration,
                        **kwargs,
                    )
            
            
            class relationships(
                schemas.DictSchema
            ):
            
            
                class MetaOapg:
                    
                    class properties:
                        
                        
                        class filterSettings(
                            schemas.DictSchema
                        ):
                        
                        
                            class MetaOapg:
                                required = {
                                    "data",
                                }
                                
                                class properties:
                                
                                    @staticmethod
                                    def data() -> typing.Type['JsonApiWorkspaceDataFilterSettingToManyLinkage']:
                                        return JsonApiWorkspaceDataFilterSettingToManyLinkage
                                    __annotations__ = {
                                        "data": data,
                                    }
                            
                            data: 'JsonApiWorkspaceDataFilterSettingToManyLinkage'
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["data"]) -> 'JsonApiWorkspaceDataFilterSettingToManyLinkage': ...
                            
                            @typing.overload
                            def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                            
                            def __getitem__(self, name: typing.Union[typing_extensions.Literal["data", ], str]):
                                # dict_instance[name] accessor
                                return super().__getitem__(name)
                            
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["data"]) -> 'JsonApiWorkspaceDataFilterSettingToManyLinkage': ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                            
                            def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["data", ], str]):
                                return super().get_item_oapg(name)
                            
                        
                            def __new__(
                                cls,
                                *_args: typing.Union[dict, frozendict.frozendict, ],
                                data: 'JsonApiWorkspaceDataFilterSettingToManyLinkage',
                                _configuration: typing.Optional[schemas.Configuration] = None,
                                **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                            ) -> 'filterSettings':
                                return super().__new__(
                                    cls,
                                    *_args,
                                    data=data,
                                    _configuration=_configuration,
                                    **kwargs,
                                )
                        __annotations__ = {
                            "filterSettings": filterSettings,
                        }
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["filterSettings"]) -> MetaOapg.properties.filterSettings: ...
                
                @typing.overload
                def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                
                def __getitem__(self, name: typing.Union[typing_extensions.Literal["filterSettings", ], str]):
                    # dict_instance[name] accessor
                    return super().__getitem__(name)
                
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["filterSettings"]) -> typing.Union[MetaOapg.properties.filterSettings, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                
                def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["filterSettings", ], str]):
                    return super().get_item_oapg(name)
                
            
                def __new__(
                    cls,
                    *_args: typing.Union[dict, frozendict.frozendict, ],
                    filterSettings: typing.Union[MetaOapg.properties.filterSettings, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'relationships':
                    return super().__new__(
                        cls,
                        *_args,
                        filterSettings=filterSettings,
                        _configuration=_configuration,
                        **kwargs,
                    )
            __annotations__ = {
                "id": id,
                "type": type,
                "attributes": attributes,
                "relationships": relationships,
            }
    
    id: MetaOapg.properties.id
    type: MetaOapg.properties.type
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["type"]) -> MetaOapg.properties.type: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["attributes"]) -> MetaOapg.properties.attributes: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["relationships"]) -> MetaOapg.properties.relationships: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["id", "type", "attributes", "relationships", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["type"]) -> MetaOapg.properties.type: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["attributes"]) -> typing.Union[MetaOapg.properties.attributes, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["relationships"]) -> typing.Union[MetaOapg.properties.relationships, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["id", "type", "attributes", "relationships", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        id: typing.Union[MetaOapg.properties.id, str, ],
        type: typing.Union[MetaOapg.properties.type, str, ],
        attributes: typing.Union[MetaOapg.properties.attributes, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        relationships: typing.Union[MetaOapg.properties.relationships, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'JsonApiWorkspaceDataFilterPatch':
        return super().__new__(
            cls,
            *_args,
            id=id,
            type=type,
            attributes=attributes,
            relationships=relationships,
            _configuration=_configuration,
            **kwargs,
        )

from gooddata_api_client.model.json_api_workspace_data_filter_setting_to_many_linkage import JsonApiWorkspaceDataFilterSettingToManyLinkage
