# ErrorInfo

Structured error, present when the search could not run (e.g. metadata sync in progress). Absent on success.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reason** | **str** | Stable machine-readable error code. Switch on this for localized client messages. | 
**status_code** | **int** | HTTP-like semantic status (e.g. 503 when the workspace is still syncing). | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


