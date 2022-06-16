# DeclarativeTable

A database table.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | [**[DeclarativeColumn]**](DeclarativeColumn.md) | An array of physical columns | 
**id** | **str** | Table id. | 
**path** | **[str]** | Path to table. | 
**type** | **str** | Table type: TABLE or VIEW. | 
**name_prefix** | **str** | Table or view name prefix used in scan. Will be stripped when generating LDM. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


