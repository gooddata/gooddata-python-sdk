# JsonApiUserDataFilterPatchAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**are_relations_valid** | **bool** |  | [optional] 
**description** | **str** |  | [optional] 
**maql** | **str** |  | [optional] 
**tags** | **List[str]** |  | [optional] 
**title** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_user_data_filter_patch_attributes import JsonApiUserDataFilterPatchAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiUserDataFilterPatchAttributes from a JSON string
json_api_user_data_filter_patch_attributes_instance = JsonApiUserDataFilterPatchAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiUserDataFilterPatchAttributes.to_json())

# convert the object into a dict
json_api_user_data_filter_patch_attributes_dict = json_api_user_data_filter_patch_attributes_instance.to_dict()
# create an instance of JsonApiUserDataFilterPatchAttributes from a dict
json_api_user_data_filter_patch_attributes_from_dict = JsonApiUserDataFilterPatchAttributes.from_dict(json_api_user_data_filter_patch_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


