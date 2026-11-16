# LocalizationMetadataStatistics

Translations of titles, descriptions, tags and free-form texts of workspace objects. `locales` lists the languages that have stored translations, sorted. A language counts once translations for it are uploaded, even when they are empty.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**locales** | [**[LocalizationStatisticsLocale]**](LocalizationStatisticsLocale.md) |  | 
**workspaces** | [**[LocalizationStatisticsWorkspace]**](LocalizationStatisticsWorkspace.md) | (BETA) Translation counts of the workspace and each parent workspace that the user can see, root first. Present only with &#x60;includeCoverage&#x3D;true&#x60; on the workspace endpoint. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


