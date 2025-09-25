# JsonApiFilterViewIn

JSON:API representation of filterView entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiFilterViewInAttributes**](JsonApiFilterViewInAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**relationships** | [**JsonApiFilterViewInRelationships**](JsonApiFilterViewInRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_filter_view_in import JsonApiFilterViewIn

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiFilterViewIn from a JSON string
json_api_filter_view_in_instance = JsonApiFilterViewIn.from_json(json)
# print the JSON string representation of the object
print(JsonApiFilterViewIn.to_json())

# convert the object into a dict
json_api_filter_view_in_dict = json_api_filter_view_in_instance.to_dict()
# create an instance of JsonApiFilterViewIn from a dict
json_api_filter_view_in_from_dict = JsonApiFilterViewIn.from_dict(json_api_filter_view_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


