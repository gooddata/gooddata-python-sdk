# JsonApiAnalyticalDashboardOutRelationshipsFilterContexts


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[JsonApiFilterContextLinkage]**](JsonApiFilterContextLinkage.md) | References to other resource objects in a to-many (\\\&quot;relationship\\\&quot;). Relationships can be specified by including a member in a resource&#39;s links object. | 

## Example

```python
from gooddata_api_client.models.json_api_analytical_dashboard_out_relationships_filter_contexts import JsonApiAnalyticalDashboardOutRelationshipsFilterContexts

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAnalyticalDashboardOutRelationshipsFilterContexts from a JSON string
json_api_analytical_dashboard_out_relationships_filter_contexts_instance = JsonApiAnalyticalDashboardOutRelationshipsFilterContexts.from_json(json)
# print the JSON string representation of the object
print(JsonApiAnalyticalDashboardOutRelationshipsFilterContexts.to_json())

# convert the object into a dict
json_api_analytical_dashboard_out_relationships_filter_contexts_dict = json_api_analytical_dashboard_out_relationships_filter_contexts_instance.to_dict()
# create an instance of JsonApiAnalyticalDashboardOutRelationshipsFilterContexts from a dict
json_api_analytical_dashboard_out_relationships_filter_contexts_from_dict = JsonApiAnalyticalDashboardOutRelationshipsFilterContexts.from_dict(json_api_analytical_dashboard_out_relationships_filter_contexts_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


