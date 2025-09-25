# JsonApiFilterContextOutRelationships


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiAttributeHierarchyOutRelationshipsAttributes**](JsonApiAttributeHierarchyOutRelationshipsAttributes.md) |  | [optional] 
**datasets** | [**JsonApiAnalyticalDashboardOutRelationshipsDatasets**](JsonApiAnalyticalDashboardOutRelationshipsDatasets.md) |  | [optional] 
**labels** | [**JsonApiAnalyticalDashboardOutRelationshipsLabels**](JsonApiAnalyticalDashboardOutRelationshipsLabels.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_filter_context_out_relationships import JsonApiFilterContextOutRelationships

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiFilterContextOutRelationships from a JSON string
json_api_filter_context_out_relationships_instance = JsonApiFilterContextOutRelationships.from_json(json)
# print the JSON string representation of the object
print(JsonApiFilterContextOutRelationships.to_json())

# convert the object into a dict
json_api_filter_context_out_relationships_dict = json_api_filter_context_out_relationships_instance.to_dict()
# create an instance of JsonApiFilterContextOutRelationships from a dict
json_api_filter_context_out_relationships_from_dict = JsonApiFilterContextOutRelationships.from_dict(json_api_filter_context_out_relationships_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


