# JsonApiLabelOutDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiLabelOut**](JsonApiLabelOut.md) |  | 
**included** | [**List[JsonApiAttributeOutWithLinks]**](JsonApiAttributeOutWithLinks.md) | Included resources | [optional] 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_label_out_document import JsonApiLabelOutDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiLabelOutDocument from a JSON string
json_api_label_out_document_instance = JsonApiLabelOutDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiLabelOutDocument.to_json())

# convert the object into a dict
json_api_label_out_document_dict = json_api_label_out_document_instance.to_dict()
# create an instance of JsonApiLabelOutDocument from a dict
json_api_label_out_document_from_dict = JsonApiLabelOutDocument.from_dict(json_api_label_out_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


