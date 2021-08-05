# ErrorMessage

Contains information about the error.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**timestamp** | **str** | Error timestamp in ISO 8601. | 
**status** | **int** | HTTP error response status code. | 
**error** | **str** | HTTP error message like: Bad Request, Not Found, etc. | 
**message** | **str** | Error message returned by the server application. | 
**path** | **str** | Path of the failed request. | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


