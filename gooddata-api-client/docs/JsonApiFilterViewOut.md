# JsonApiFilterViewOut

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
from gooddata_api_client.models.json_api_filter_view_out import JsonApiFilterViewOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiFilterViewOut from a JSON string
json_api_filter_view_out_instance = JsonApiFilterViewOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiFilterViewOut.to_json())

# convert the object into a dict
json_api_filter_view_out_dict = json_api_filter_view_out_instance.to_dict()
# create an instance of JsonApiFilterViewOut from a dict
json_api_filter_view_out_from_dict = JsonApiFilterViewOut.from_dict(json_api_filter_view_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


