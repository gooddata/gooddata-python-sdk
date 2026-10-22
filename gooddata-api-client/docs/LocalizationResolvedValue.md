# LocalizationResolvedValue

The value a workspace gets for one setting, and where it comes from. Never null. `content.value` is null when the workspace gets no language.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | [**LocalizationContent**](LocalizationContent.md) |  | 
**source** | **str** | Where the value comes from, from the strongest source to the weakest: USER - the user set it. WORKSPACE - the workspace sets it. PARENT - the workspace inherits it from a parent workspace. ORGANIZATION - the organization default. ENVIRONMENT - the default set for the whole deployment. DEFAULT - the built-in default. | 
**origin_id** | **str, none_type** | The ancestor workspace that sets the value. Null unless the source is PARENT. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


