# JsonApiWorkspaceInAttributesDataSource

The data source used for the particular workspace instead of the one defined in the LDM inherited from its parent workspace. Such data source cannot be defined for a single or a top-parent workspace.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The ID of the used data source. | 
**schema_path** | **[str]** | The full schema path as array of its path parts. Will be rendered as subPath1.subPath2... | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


