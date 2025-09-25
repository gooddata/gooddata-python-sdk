# JsonApiLabelOutAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**are_relations_valid** | **bool** |  | [optional] 
**description** | **str** |  | [optional] 
**is_hidden** | **bool** |  | [optional] 
**primary** | **bool** |  | [optional] 
**source_column** | **str** |  | [optional] 
**source_column_data_type** | **str** |  | [optional] 
**tags** | **List[str]** |  | [optional] 
**title** | **str** |  | [optional] 
**value_type** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_label_out_attributes import JsonApiLabelOutAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiLabelOutAttributes from a JSON string
json_api_label_out_attributes_instance = JsonApiLabelOutAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiLabelOutAttributes.to_json())

# convert the object into a dict
json_api_label_out_attributes_dict = json_api_label_out_attributes_instance.to_dict()
# create an instance of JsonApiLabelOutAttributes from a dict
json_api_label_out_attributes_from_dict = JsonApiLabelOutAttributes.from_dict(json_api_label_out_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


