# LocalizationStatisticsWorkspace

Metadata texts of one workspace. A row counts only the texts that the workspace owns. A child workspace sums its row and the rows of its parents.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Workspace ID. | 
**locales** | [**[LocalizationStatisticsTranslatedLocale]**](LocalizationStatisticsTranslatedLocale.md) | Every language of &#x60;metadata.locales&#x60;, sorted, with 0 where nothing is translated. | 
**name** | **str** | Workspace name. | 
**total** | **int** | Titles, descriptions, tags and free-form texts the workspace owns. Blank texts are not counted. | 
**parent_id** | **str, none_type** | Parent workspace ID, null for a root workspace. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


