# JsonApiOrganizationPatchDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiOrganizationPatch**](JsonApiOrganizationPatch.md) |  | 

## Example

```python
from gooddata_api_client.models.json_api_organization_patch_document import JsonApiOrganizationPatchDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiOrganizationPatchDocument from a JSON string
json_api_organization_patch_document_instance = JsonApiOrganizationPatchDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiOrganizationPatchDocument.to_json())

# convert the object into a dict
json_api_organization_patch_document_dict = json_api_organization_patch_document_instance.to_dict()
# create an instance of JsonApiOrganizationPatchDocument from a dict
json_api_organization_patch_document_from_dict = JsonApiOrganizationPatchDocument.from_dict(json_api_organization_patch_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


