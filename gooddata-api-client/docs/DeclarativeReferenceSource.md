# DeclarativeReferenceSource

A dataset reference source column description.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**column** | **str** | A name of the source column in the table. | 
**target** | [**GrainIdentifier**](GrainIdentifier.md) |  | 
**data_type** | **str** | A type of the source column. | [optional] 
**is_nullable** | **bool** | Flag indicating whether the associated source column allows null values. | [optional] 
**null_value** | **str** | Value used in coalesce during joins instead of null. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


