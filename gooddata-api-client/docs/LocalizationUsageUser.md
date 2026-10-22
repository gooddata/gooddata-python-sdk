# LocalizationUsageUser


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**by_setting** | [**LocalizationUserValues**](LocalizationUserValues.md) |  | 
**id** | **str** |  | 
**source** | **str** | Where the value comes from, from the strongest source to the weakest: USER - the user set it. WORKSPACE - the workspace sets it. PARENT - the workspace inherits it from a parent workspace. ORGANIZATION - the organization default. ENVIRONMENT - the default set for the whole deployment. DEFAULT - the built-in default. | 
**email** | **str, none_type** |  | [optional] 
**name** | **str, none_type** | First and last name. Null when the user has neither. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


