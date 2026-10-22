# LocalizationUserValue

The value a user gets for one setting, and where it comes from. In the organization users list, it is the value the user sets, with source USER. It is null when the user does not set the setting, because the value then depends on the workspace. In the workspace users list, it is never null. It is the value the user sets, with source USER. Otherwise it is the value the workspace gets, with the source of the workspace. For the origin of that value, see `originId` in the workspace usage. `content.value` is null when the user gets no language.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | [**LocalizationContent**](LocalizationContent.md) |  | 
**source** | **str** | Where the value comes from, from the strongest source to the weakest: USER - the user set it. WORKSPACE - the workspace sets it. PARENT - the workspace inherits it from a parent workspace. ORGANIZATION - the organization default. ENVIRONMENT - the default set for the whole deployment. DEFAULT - the built-in default. | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


