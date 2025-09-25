# JsonApiFilterViewPatchAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**are_relations_valid** | **bool** |  | [optional] 
**content** | **object** | The respective filter context. | [optional] 
**description** | **str** |  | [optional] 
**is_default** | **bool** | Indicator whether the filter view should by applied by default. | [optional] 
**tags** | **List[str]** |  | [optional] 
**title** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_filter_view_patch_attributes import JsonApiFilterViewPatchAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiFilterViewPatchAttributes from a JSON string
json_api_filter_view_patch_attributes_instance = JsonApiFilterViewPatchAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiFilterViewPatchAttributes.to_json())

# convert the object into a dict
json_api_filter_view_patch_attributes_dict = json_api_filter_view_patch_attributes_instance.to_dict()
# create an instance of JsonApiFilterViewPatchAttributes from a dict
json_api_filter_view_patch_attributes_from_dict = JsonApiFilterViewPatchAttributes.from_dict(json_api_filter_view_patch_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


