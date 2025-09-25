# JsonApiOrganizationOutMeta


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**permissions** | **List[str]** | List of valid permissions for a logged-in user. | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_organization_out_meta import JsonApiOrganizationOutMeta

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiOrganizationOutMeta from a JSON string
json_api_organization_out_meta_instance = JsonApiOrganizationOutMeta.from_json(json)
# print the JSON string representation of the object
print(JsonApiOrganizationOutMeta.to_json())

# convert the object into a dict
json_api_organization_out_meta_dict = json_api_organization_out_meta_instance.to_dict()
# create an instance of JsonApiOrganizationOutMeta from a dict
json_api_organization_out_meta_from_dict = JsonApiOrganizationOutMeta.from_dict(json_api_organization_out_meta_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


