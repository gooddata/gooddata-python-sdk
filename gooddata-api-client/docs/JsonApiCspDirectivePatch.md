# JsonApiCspDirectivePatch

JSON:API representation of patching cspDirective entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiCspDirectivePatchAttributes**](JsonApiCspDirectivePatchAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_csp_directive_patch import JsonApiCspDirectivePatch

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiCspDirectivePatch from a JSON string
json_api_csp_directive_patch_instance = JsonApiCspDirectivePatch.from_json(json)
# print the JSON string representation of the object
print(JsonApiCspDirectivePatch.to_json())

# convert the object into a dict
json_api_csp_directive_patch_dict = json_api_csp_directive_patch_instance.to_dict()
# create an instance of JsonApiCspDirectivePatch from a dict
json_api_csp_directive_patch_from_dict = JsonApiCspDirectivePatch.from_dict(json_api_csp_directive_patch_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


