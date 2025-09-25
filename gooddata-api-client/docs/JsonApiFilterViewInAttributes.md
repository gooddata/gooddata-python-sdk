# JsonApiFilterViewInAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**are_relations_valid** | **bool** |  | [optional] 
**content** | **object** | The respective filter context. | 
**description** | **str** |  | [optional] 
**is_default** | **bool** | Indicator whether the filter view should by applied by default. | [optional] 
**tags** | **List[str]** |  | [optional] 
**title** | **str** |  | 

## Example

```python
from gooddata_api_client.models.json_api_filter_view_in_attributes import JsonApiFilterViewInAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiFilterViewInAttributes from a JSON string
json_api_filter_view_in_attributes_instance = JsonApiFilterViewInAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiFilterViewInAttributes.to_json())

# convert the object into a dict
json_api_filter_view_in_attributes_dict = json_api_filter_view_in_attributes_instance.to_dict()
# create an instance of JsonApiFilterViewInAttributes from a dict
json_api_filter_view_in_attributes_from_dict = JsonApiFilterViewInAttributes.from_dict(json_api_filter_view_in_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


