# JsonApiDataSourcePatch

JSON:API representation of patching dataSource entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiDataSourcePatchAttributes**](JsonApiDataSourcePatchAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_data_source_patch import JsonApiDataSourcePatch

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiDataSourcePatch from a JSON string
json_api_data_source_patch_instance = JsonApiDataSourcePatch.from_json(json)
# print the JSON string representation of the object
print(JsonApiDataSourcePatch.to_json())

# convert the object into a dict
json_api_data_source_patch_dict = json_api_data_source_patch_instance.to_dict()
# create an instance of JsonApiDataSourcePatch from a dict
json_api_data_source_patch_from_dict = JsonApiDataSourcePatch.from_dict(json_api_data_source_patch_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


