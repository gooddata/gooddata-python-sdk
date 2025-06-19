# DeclarativeFact

A dataset fact.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Fact ID. | 
**source_column** | **str** | A name of the source column in the table. | 
**title** | **str** | Fact title. | 
**description** | **str** | Fact description. | [optional] 
**source_column_data_type** | **str** | A type of the source column | [optional] 
**source_fact_reference** | [**DeclarativeSourceFactReference**](DeclarativeSourceFactReference.md) |  | [optional] 
**tags** | **[str]** | A list of tags. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


