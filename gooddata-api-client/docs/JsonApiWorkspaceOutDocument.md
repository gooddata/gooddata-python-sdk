# JsonApiWorkspaceOutDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiWorkspaceOut**](JsonApiWorkspaceOut.md) |  | 
**included** | [**List[JsonApiWorkspaceOutWithLinks]**](JsonApiWorkspaceOutWithLinks.md) | Included resources | [optional] 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_workspace_out_document import JsonApiWorkspaceOutDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiWorkspaceOutDocument from a JSON string
json_api_workspace_out_document_instance = JsonApiWorkspaceOutDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiWorkspaceOutDocument.to_json())

# convert the object into a dict
json_api_workspace_out_document_dict = json_api_workspace_out_document_instance.to_dict()
# create an instance of JsonApiWorkspaceOutDocument from a dict
json_api_workspace_out_document_from_dict = JsonApiWorkspaceOutDocument.from_dict(json_api_workspace_out_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


