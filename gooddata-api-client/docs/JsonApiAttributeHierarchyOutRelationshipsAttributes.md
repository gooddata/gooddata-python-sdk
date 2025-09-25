# JsonApiAttributeHierarchyOutRelationshipsAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[JsonApiAttributeLinkage]**](JsonApiAttributeLinkage.md) | References to other resource objects in a to-many (\\\&quot;relationship\\\&quot;). Relationships can be specified by including a member in a resource&#39;s links object. | 

## Example

```python
from gooddata_api_client.models.json_api_attribute_hierarchy_out_relationships_attributes import JsonApiAttributeHierarchyOutRelationshipsAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAttributeHierarchyOutRelationshipsAttributes from a JSON string
json_api_attribute_hierarchy_out_relationships_attributes_instance = JsonApiAttributeHierarchyOutRelationshipsAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiAttributeHierarchyOutRelationshipsAttributes.to_json())

# convert the object into a dict
json_api_attribute_hierarchy_out_relationships_attributes_dict = json_api_attribute_hierarchy_out_relationships_attributes_instance.to_dict()
# create an instance of JsonApiAttributeHierarchyOutRelationshipsAttributes from a dict
json_api_attribute_hierarchy_out_relationships_attributes_from_dict = JsonApiAttributeHierarchyOutRelationshipsAttributes.from_dict(json_api_attribute_hierarchy_out_relationships_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


