# JsonApiLabelOut

JSON:API representation of label entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiLabelOutAttributes**](JsonApiLabelOutAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiAggregatedFactOutMeta**](JsonApiAggregatedFactOutMeta.md) |  | [optional] 
**relationships** | [**JsonApiLabelOutRelationships**](JsonApiLabelOutRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_label_out import JsonApiLabelOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiLabelOut from a JSON string
json_api_label_out_instance = JsonApiLabelOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiLabelOut.to_json())

# convert the object into a dict
json_api_label_out_dict = json_api_label_out_instance.to_dict()
# create an instance of JsonApiLabelOut from a dict
json_api_label_out_from_dict = JsonApiLabelOut.from_dict(json_api_label_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


