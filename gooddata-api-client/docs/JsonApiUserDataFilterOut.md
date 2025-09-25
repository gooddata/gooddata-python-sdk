# JsonApiUserDataFilterOut

JSON:API representation of userDataFilter entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiUserDataFilterInAttributes**](JsonApiUserDataFilterInAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiAggregatedFactOutMeta**](JsonApiAggregatedFactOutMeta.md) |  | [optional] 
**relationships** | [**JsonApiUserDataFilterOutRelationships**](JsonApiUserDataFilterOutRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_user_data_filter_out import JsonApiUserDataFilterOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiUserDataFilterOut from a JSON string
json_api_user_data_filter_out_instance = JsonApiUserDataFilterOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiUserDataFilterOut.to_json())

# convert the object into a dict
json_api_user_data_filter_out_dict = json_api_user_data_filter_out_instance.to_dict()
# create an instance of JsonApiUserDataFilterOut from a dict
json_api_user_data_filter_out_from_dict = JsonApiUserDataFilterOut.from_dict(json_api_user_data_filter_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


