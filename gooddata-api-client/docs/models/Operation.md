# gooddata_api_client.model.operation.Operation

Represents a Long-Running Operation: a process that takes some time to complete.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Represents a Long-Running Operation: a process that takes some time to complete. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**kind** | str,  | str,  | Type of the long-running operation. * &#x60;provision-database&#x60; — Provisioning of an AI Lake database. * &#x60;deprovision-database&#x60; — Deprovisioning (deletion) of an AI Lake database. * &#x60;run-service-command&#x60; — Running a command in a particular AI Lake service.  | must be one of ["provision-database", "deprovision-database", "run-service-command", ] 
**id** | str,  | str,  | Id of the operation | 
**status** | str,  | str,  |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

