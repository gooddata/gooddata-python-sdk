# SearchResultObject


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Object ID. | 
**title** | **str** | Object title. | 
**type** | **str** | Object type, e.g. dashboard. | 
**workspace_id** | **str** | Workspace ID. | 
**created_at** | **datetime** | Timestamp when object was created. | [optional] 
**description** | **str** | Object description. | [optional] 
**modified_at** | **datetime** | Timestamp when object was last modified. | [optional] 
**score** | **float** | Result score calculated by a similarity search algorithm (cosine_distance). | [optional] 
**score_descriptor** | **float** | Result score for descriptor containing(now) description and tags. | [optional] 
**score_exact_match** | **int** | Result score for exact match(id/title). 1/1000. Other scores are multiplied by this. | [optional] 
**score_title** | **float** | Result score for object title. | [optional] 
**tags** | **[str]** |  | [optional] 
**visualization_url** | **str** | If the object is visualization, this field defines the type of visualization. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


