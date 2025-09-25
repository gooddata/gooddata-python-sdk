# JsonApiUserDataFilterIn

JSON:API representation of userDataFilter entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiUserDataFilterInAttributes**](JsonApiUserDataFilterInAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**relationships** | [**JsonApiUserDataFilterInRelationships**](JsonApiUserDataFilterInRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_user_data_filter_in import JsonApiUserDataFilterIn

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiUserDataFilterIn from a JSON string
json_api_user_data_filter_in_instance = JsonApiUserDataFilterIn.from_json(json)
# print the JSON string representation of the object
print(JsonApiUserDataFilterIn.to_json())

# convert the object into a dict
json_api_user_data_filter_in_dict = json_api_user_data_filter_in_instance.to_dict()
# create an instance of JsonApiUserDataFilterIn from a dict
json_api_user_data_filter_in_from_dict = JsonApiUserDataFilterIn.from_dict(json_api_user_data_filter_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


