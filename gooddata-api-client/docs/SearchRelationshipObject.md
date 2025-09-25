# SearchRelationshipObject


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**source_object_id** | **str** | Source object ID. | 
**source_object_title** | **str** | Source object title. | 
**source_object_type** | **str** | Source object type, e.g. dashboard. | 
**source_workspace_id** | **str** | Source workspace ID. If relationship is dashboard-&gt;visualization, this is the workspace where the dashboard is located. | 
**target_object_id** | **str** | Target object ID. | 
**target_object_title** | **str** | Target object title. | 
**target_object_type** | **str** | Target object type, e.g. visualization. | 
**target_workspace_id** | **str** | Target workspace ID. If relationship is dashboard-&gt;visualization, this is the workspace where the visualization is located. | 

## Example

```python
from gooddata_api_client.models.search_relationship_object import SearchRelationshipObject

# TODO update the JSON string below
json = "{}"
# create an instance of SearchRelationshipObject from a JSON string
search_relationship_object_instance = SearchRelationshipObject.from_json(json)
# print the JSON string representation of the object
print(SearchRelationshipObject.to_json())

# convert the object into a dict
search_relationship_object_dict = search_relationship_object_instance.to_dict()
# create an instance of SearchRelationshipObject from a dict
search_relationship_object_from_dict = SearchRelationshipObject.from_dict(search_relationship_object_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


