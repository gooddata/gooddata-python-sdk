# JsonApiAttributeHierarchyOutDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiAttributeHierarchyOut**](JsonApiAttributeHierarchyOut.md) |  | 
**included** | [**List[JsonApiAttributeHierarchyOutIncludes]**](JsonApiAttributeHierarchyOutIncludes.md) | Included resources | [optional] 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_attribute_hierarchy_out_document import JsonApiAttributeHierarchyOutDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAttributeHierarchyOutDocument from a JSON string
json_api_attribute_hierarchy_out_document_instance = JsonApiAttributeHierarchyOutDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiAttributeHierarchyOutDocument.to_json())

# convert the object into a dict
json_api_attribute_hierarchy_out_document_dict = json_api_attribute_hierarchy_out_document_instance.to_dict()
# create an instance of JsonApiAttributeHierarchyOutDocument from a dict
json_api_attribute_hierarchy_out_document_from_dict = JsonApiAttributeHierarchyOutDocument.from_dict(json_api_attribute_hierarchy_out_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


