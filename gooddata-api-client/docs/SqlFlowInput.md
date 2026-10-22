# SqlFlowInput

Runs a SELECT statement on a data source and reads its rows as a table. Its columns are named and typed as the statement returns them. Data filters of the workspace and of the user do not apply. A GDSTORAGE, FlexConnect or platform-managed data source cannot run it.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_source_id** | **str** | Identifier of the data source that runs the statement. | 
**sql** | **str** | One SELECT statement in the SQL dialect of the data source. | 
**type** | **str** | Type of the input. | defaults to "sql"
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


