# DeclarativeDataset

A dataset defined by its properties.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**grain** | [**[GrainIdentifier]**](GrainIdentifier.md) | An array of grain identifiers. | 
**id** | **str** | The Dataset ID. This ID is further used to refer to this instance of dataset. | 
**references** | [**[DeclarativeReference]**](DeclarativeReference.md) | An array of references. | 
**title** | **str** | A dataset title. | 
**attributes** | [**[DeclarativeAttribute]**](DeclarativeAttribute.md) | An array of attributes. | [optional] 
**data_source_table_id** | [**DataSourceTableIdentifier**](DataSourceTableIdentifier.md) |  | [optional] 
**description** | **str** | A dataset description. | [optional] 
**facts** | [**[DeclarativeFact]**](DeclarativeFact.md) | An array of facts. | [optional] 
**tags** | **[str]** | A list of tags. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


