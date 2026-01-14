# DeclarativeColumn

A table column.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_type** | **str** | Column type | 
**name** | **str** | Column name | 
**description** | **str** | Column description/comment from database | [optional] 
**is_nullable** | **bool** | Column is nullable | [optional] 
**is_primary_key** | **bool** | Is column part of primary key? | [optional] 
**referenced_table_column** | **str** | Referenced table (Foreign key) | [optional] 
**referenced_table_id** | **str** | Referenced table (Foreign key) | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


