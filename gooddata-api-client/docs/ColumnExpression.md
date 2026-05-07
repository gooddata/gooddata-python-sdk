# ColumnExpression

Single column projection override: applies `function(column)` to a source column.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**column** | **str** | Source column produced by parquet schema inference (after columnOverrides). | 
**function** | **str** | StarRocks transform applied to a source column when projecting it through the generated CREATE PIPE ... AS INSERT statement. | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


