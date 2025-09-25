# JsonApiFilterViewInRelationships


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**analytical_dashboard** | [**JsonApiAutomationInRelationshipsAnalyticalDashboard**](JsonApiAutomationInRelationshipsAnalyticalDashboard.md) |  | [optional] 
**user** | [**JsonApiFilterViewInRelationshipsUser**](JsonApiFilterViewInRelationshipsUser.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_filter_view_in_relationships import JsonApiFilterViewInRelationships

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiFilterViewInRelationships from a JSON string
json_api_filter_view_in_relationships_instance = JsonApiFilterViewInRelationships.from_json(json)
# print the JSON string representation of the object
print(JsonApiFilterViewInRelationships.to_json())

# convert the object into a dict
json_api_filter_view_in_relationships_dict = json_api_filter_view_in_relationships_instance.to_dict()
# create an instance of JsonApiFilterViewInRelationships from a dict
json_api_filter_view_in_relationships_from_dict = JsonApiFilterViewInRelationships.from_dict(json_api_filter_view_in_relationships_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


