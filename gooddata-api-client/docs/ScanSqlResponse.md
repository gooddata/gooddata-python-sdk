# ScanSqlResponse

Result of scanSql. Consists of array of query columns including type. Sql query result data preview can be attached optionally

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | [**[SqlColumn]**](SqlColumn.md) | Array of columns with types. | 
**data_preview** | **[[str]]** | Array of rows where each row is another array of string values. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


