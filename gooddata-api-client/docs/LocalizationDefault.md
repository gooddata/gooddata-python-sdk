# LocalizationDefault

The value a workspace gets for one setting when it and its parents set nothing, and where it comes from. Null when that value has no language.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | [**LocalizationContent**](LocalizationContent.md) |  | 
**source** | **str** | Where the value comes from, from the strongest source to the weakest: USER - the user set it. WORKSPACE - the workspace sets it. PARENT - the workspace inherits it from a parent workspace. ORGANIZATION - the organization default. ENVIRONMENT - the default set for the whole deployment. DEFAULT - the built-in default. | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


