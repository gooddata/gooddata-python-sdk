# DeclarativeDataset

A dataset defined by its properties.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The Dataset ID. This ID is further used to refer to this instance of dataset. | 
**title** | **str** | A dataset title. | 
**grain** | [**[GrainIdentifier]**](GrainIdentifier.md) | An array of grain identifiers. | 
**attributes** | [**[DeclarativeAttribute]**](DeclarativeAttribute.md) | An array of attributes. | 
**facts** | [**[DeclarativeFact]**](DeclarativeFact.md) | An array of facts. | 
**references** | [**[DeclarativeReference]**](DeclarativeReference.md) | An array of references. | 
**description** | **str** | A dataset description. | [optional] 
**data_source_table_id** | [**DataSourceTableIdentifier**](DataSourceTableIdentifier.md) |  | [optional] 
**tags** | **[str]** | A list of tags. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


