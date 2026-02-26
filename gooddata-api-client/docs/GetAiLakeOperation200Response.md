# GetAiLakeOperation200Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** |  | 
**result** | **{str: (bool, date, datetime, dict, float, int, list, str, none_type)}** | Operation-specific result payload, can be missing for operations like delete | [optional] 
**id** | **str** | Id of the operation | [optional] 
**kind** | **str** | Type of the long-running operation. * &#x60;provision-database&#x60; — Provisioning of an AI Lake database. * &#x60;deprovision-database&#x60; — Deprovisioning (deletion) of an AI Lake database. * &#x60;run-service-command&#x60; — Running a command in a particular AI Lake service.  | [optional] 
**error** | [**OperationError**](OperationError.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


