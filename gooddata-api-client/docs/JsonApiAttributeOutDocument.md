# JsonApiAttributeOutDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiAttributeOut**](JsonApiAttributeOut.md) |  | 
**included** | [**List[JsonApiAttributeOutIncludes]**](JsonApiAttributeOutIncludes.md) | Included resources | [optional] 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_attribute_out_document import JsonApiAttributeOutDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAttributeOutDocument from a JSON string
json_api_attribute_out_document_instance = JsonApiAttributeOutDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiAttributeOutDocument.to_json())

# convert the object into a dict
json_api_attribute_out_document_dict = json_api_attribute_out_document_instance.to_dict()
# create an instance of JsonApiAttributeOutDocument from a dict
json_api_attribute_out_document_from_dict = JsonApiAttributeOutDocument.from_dict(json_api_attribute_out_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


