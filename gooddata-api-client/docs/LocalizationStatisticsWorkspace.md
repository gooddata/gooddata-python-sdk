# LocalizationStatisticsWorkspace

Metadata texts of one workspace. A row counts only the texts that the workspace owns. A parent's row counts only the texts that the workspaces below it inherit. A child workspace sums its row and the rows of its parents.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Workspace ID. | 
**locales** | [**[LocalizationStatisticsTranslatedLocale]**](LocalizationStatisticsTranslatedLocale.md) | Every language of &#x60;metadata.locales&#x60;, sorted, with 0 where nothing is translated. | 
**total** | **int** | Titles, descriptions, tags and free-form texts the workspace owns. Blank texts are not counted. | 
**name** | **str, none_type** | Workspace name. Null for a parent that the user has no permission on. The name stays when the user can see the workspace right below it. | [optional] 
**parent_id** | **str, none_type** | Parent workspace ID, null for a root workspace. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


