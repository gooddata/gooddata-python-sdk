# LocalizationIssue

One localization issue in one language.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**locale** | **str** | The problem language. | 
**type** | **str** | The kind of localization issue. The prefix names the area of the problem. METADATA_MISSING_TRANSLATION - the metadata language has no translation under exactly its code. When the metadata language is the default, the display language is checked instead. METADATA_LANGUAGE_MISMATCH - the display language has a translation, but the metadata language is not set to it. METADATA_UNUSED_TRANSLATION - the workspace owns a translation that nobody uses. No workspace in its subtree gets that language. No user has it as their own language. System accounts and the bootstrap user are not counted, as in the usage endpoints. New types may be added. | 
**workspaces** | **int** | Organization issues only. The number of workspaces with this issue. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


