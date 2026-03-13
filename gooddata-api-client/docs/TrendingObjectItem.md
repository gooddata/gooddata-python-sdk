# TrendingObjectItem

Trending analytics catalog objects

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Object ID. | 
**tags** | **[str]** |  | 
**title** | **str** | Object title. | 
**type** | **str** | Object type, e.g. dashboard, visualization, metric. | 
**usage_count** | **int** | Number of times this object has been used/referenced. | 
**workspace_id** | **str** | Workspace ID the object belongs to. | 
**created_at** | **datetime** | Timestamp when object was created. | [optional] 
**created_by** | **str** | ID of the user who created the object. | [optional] 
**dataset_id** | **str** | ID of the associated dataset, if applicable. | [optional] 
**dataset_title** | **str** | Title of the associated dataset, if applicable. | [optional] 
**dataset_type** | **str** | Type of the associated dataset, if applicable. | [optional] 
**description** | **str** | Object description. | [optional] 
**is_hidden** | **bool** | If true, this object is hidden from AI search results by default. | [optional] 
**is_hidden_from_kda** | **bool** | If true, this object is hidden from KDA. | [optional] 
**metric_type** | **str** | Type of the metric (e.g. MAQL), if applicable. | [optional] 
**modified_at** | **datetime** | Timestamp when object was last modified. | [optional] 
**modified_by** | **str** | ID of the user who last modified the object. | [optional] 
**visualization_url** | **str** | URL of the visualization, if applicable. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


