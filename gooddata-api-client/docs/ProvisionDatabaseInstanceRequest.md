# ProvisionDatabaseInstanceRequest

Request to provision a new AILake Database instance

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the database instance | 
**storage_ids** | **[str]** | Set of ids of the storage instances this database instance should access. | 
**data_source_id** | **str** | Identifier for the data source created in metadata-api. Defaults to the database name. | [optional] 
**data_source_name** | **str** | Display name for the data source created in metadata-api. Defaults to the database name. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


