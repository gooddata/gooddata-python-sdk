# UpdateDatabaseDataSourceRequest

Request to update the data source associated with an AI Lake Database instance

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_source_id** | **str** | New identifier for the data source in metadata-api. Must be unique within the organization. | 
**old_data_source_id** | **str** | Identifier of the existing data source to replace. | 
**data_source_name** | **str** | New display name for the data source in metadata-api. Defaults to dataSourceId when omitted. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


