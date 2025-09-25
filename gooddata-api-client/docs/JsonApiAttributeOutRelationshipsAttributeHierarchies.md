# JsonApiAttributeOutRelationshipsAttributeHierarchies


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[JsonApiAttributeHierarchyLinkage]**](JsonApiAttributeHierarchyLinkage.md) | References to other resource objects in a to-many (\\\&quot;relationship\\\&quot;). Relationships can be specified by including a member in a resource&#39;s links object. | 

## Example

```python
from gooddata_api_client.models.json_api_attribute_out_relationships_attribute_hierarchies import JsonApiAttributeOutRelationshipsAttributeHierarchies

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAttributeOutRelationshipsAttributeHierarchies from a JSON string
json_api_attribute_out_relationships_attribute_hierarchies_instance = JsonApiAttributeOutRelationshipsAttributeHierarchies.from_json(json)
# print the JSON string representation of the object
print(JsonApiAttributeOutRelationshipsAttributeHierarchies.to_json())

# convert the object into a dict
json_api_attribute_out_relationships_attribute_hierarchies_dict = json_api_attribute_out_relationships_attribute_hierarchies_instance.to_dict()
# create an instance of JsonApiAttributeOutRelationshipsAttributeHierarchies from a dict
json_api_attribute_out_relationships_attribute_hierarchies_from_dict = JsonApiAttributeOutRelationshipsAttributeHierarchies.from_dict(json_api_attribute_out_relationships_attribute_hierarchies_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


