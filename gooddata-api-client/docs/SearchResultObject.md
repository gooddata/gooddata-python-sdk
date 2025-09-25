# SearchResultObject


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** | Timestamp when object was created. | [optional] 
**description** | **str** | Object description. | [optional] 
**id** | **str** | Object ID. | 
**is_hidden** | **bool** | If true, this object is hidden from AI search results by default. | [optional] 
**modified_at** | **datetime** | Timestamp when object was last modified. | [optional] 
**score** | **float** | Result score calculated by a similarity search algorithm (cosine_distance). | [optional] 
**score_descriptor** | **float** | Result score for descriptor containing(now) description and tags. | [optional] 
**score_exact_match** | **int** | Result score for exact match(id/title). 1/1000. Other scores are multiplied by this. | [optional] 
**score_title** | **float** | Result score for object title. | [optional] 
**tags** | **List[str]** |  | [optional] 
**title** | **str** | Object title. | 
**type** | **str** | Object type, e.g. dashboard. | 
**visualization_url** | **str** | If the object is visualization, this field defines the type of visualization. | [optional] 
**workspace_id** | **str** | Workspace ID. | 

## Example

```python
from gooddata_api_client.models.search_result_object import SearchResultObject

# TODO update the JSON string below
json = "{}"
# create an instance of SearchResultObject from a JSON string
search_result_object_instance = SearchResultObject.from_json(json)
# print the JSON string representation of the object
print(SearchResultObject.to_json())

# convert the object into a dict
search_result_object_dict = search_result_object_instance.to_dict()
# create an instance of SearchResultObject from a dict
search_result_object_from_dict = SearchResultObject.from_dict(search_result_object_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


