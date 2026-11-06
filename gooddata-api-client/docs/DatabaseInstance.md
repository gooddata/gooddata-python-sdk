# DatabaseInstance

A single AI Lake Database instance

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_sources** | [**[DataSourceInfo]**](DataSourceInfo.md) | All data source associations for this database instance. | 
**id** | **str** | Id of the AI Lake Database instance | 
**name** | **str** | Name of the AI Lake Database instance | 
**storage_ids** | **[str]** | Set of names of the storage instances this database instance accesses. Kept for backward compatibility; use &#x60;storages&#x60; for the storage ids. | 
**storages** | [**[ObjectStorageRef]**](ObjectStorageRef.md) | Storage instances this database instance accesses. | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


