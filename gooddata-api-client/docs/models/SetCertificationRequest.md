# gooddata_api_client.model.set_certification_request.SetCertificationRequest

Request to set or clear the certification of a workspace entity.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Request to set or clear the certification of a workspace entity. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**id** | str,  | str,  | ID of the entity. | 
**type** | str,  | str,  | Type of the entity. | must be one of ["metric", "visualizationObject", "analyticalDashboard", ] 
**message** | None, str,  | NoneClass, str,  | Optional message associated with the certification. | [optional] 
**status** | None, str,  | NoneClass, str,  | Certification status of the entity. | [optional] must be one of ["CERTIFIED", ] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

