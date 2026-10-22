# LocalizationUsageValue

One language. `workspaces` counts the workspaces that get it in any of the settings, once each. `users` counts the users who get it in any of the settings, once each. In the entry with a null value, `users` counts the users who get no language in any setting.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**by_setting** | [**LocalizationSettingUsages**](LocalizationSettingUsages.md) |  | 
**content** | [**LocalizationContent**](LocalizationContent.md) |  | 
**users** | [**LocalizationCount**](LocalizationCount.md) |  | 
**workspaces** | [**LocalizationCount**](LocalizationCount.md) |  | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


