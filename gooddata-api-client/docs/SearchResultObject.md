# SearchResultObject


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **str** | Timestamp when object was created. | 
**description** | **str** | Object description. | 
**id** | **str** | Object ID. | 
**modified_at** | **str** | Timestamp when object was last modified. | 
**score** | **float** | Result score calculated by a similarity search algorithm (cosine_distance). | 
**score_descriptor** | **float** | Result score for descriptor containing(now) description and tags. | 
**score_exact_match** | **int** | Result score for exact match(id/title). 1/1000. Other scores are multiplied by this. | 
**score_title** | **float** | Result score for object title. | 
**tags** | **[str]** |  | 
**title** | **str** | Object title. | 
**type** | **str** | Object type, e.g. dashboard. | 
**visualization_url** | **str** | If the object is visualization, this field defines the type of visualization. | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


