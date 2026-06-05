# GetAiLakeOperation200Response


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** |  | 
**result** | **{str: (bool, date, datetime, dict, float, int, list, str, none_type)}** | Operation-specific result payload, can be missing for operations like delete | [optional] 
**id** | **str** | Id of the operation | [optional] 
**kind** | **str** | Type of the long-running operation. * &#x60;provision-database&#x60; — Provisioning of an AI Lake database. * &#x60;deprovision-database&#x60; — Deprovisioning (deletion) of an AI Lake database. * &#x60;run-service-command&#x60; — Running a command in a particular AI Lake service. * &#x60;create-pipe-table&#x60; — Creating a pipe table backed by an S3 data source. * &#x60;delete-pipe-table&#x60; — Deleting a pipe table. * &#x60;analyze-statistics&#x60; — Running ANALYZE TABLE for CBO statistics collection. * &#x60;refresh-partition&#x60; — Refreshing a specific Hive partition (delete + re-load from S3).  | [optional] 
**error** | [**OperationError**](OperationError.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


