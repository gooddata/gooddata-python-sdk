# JsonApiUserDataFilterOutRelationships


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiAttributeHierarchyOutRelationshipsAttributes**](JsonApiAttributeHierarchyOutRelationshipsAttributes.md) |  | [optional] 
**datasets** | [**JsonApiAnalyticalDashboardOutRelationshipsDatasets**](JsonApiAnalyticalDashboardOutRelationshipsDatasets.md) |  | [optional] 
**facts** | [**JsonApiDatasetOutRelationshipsFacts**](JsonApiDatasetOutRelationshipsFacts.md) |  | [optional] 
**labels** | [**JsonApiAnalyticalDashboardOutRelationshipsLabels**](JsonApiAnalyticalDashboardOutRelationshipsLabels.md) |  | [optional] 
**metrics** | [**JsonApiAnalyticalDashboardOutRelationshipsMetrics**](JsonApiAnalyticalDashboardOutRelationshipsMetrics.md) |  | [optional] 
**user** | [**JsonApiFilterViewInRelationshipsUser**](JsonApiFilterViewInRelationshipsUser.md) |  | [optional] 
**user_group** | [**JsonApiOrganizationOutRelationshipsBootstrapUserGroup**](JsonApiOrganizationOutRelationshipsBootstrapUserGroup.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_user_data_filter_out_relationships import JsonApiUserDataFilterOutRelationships

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiUserDataFilterOutRelationships from a JSON string
json_api_user_data_filter_out_relationships_instance = JsonApiUserDataFilterOutRelationships.from_json(json)
# print the JSON string representation of the object
print(JsonApiUserDataFilterOutRelationships.to_json())

# convert the object into a dict
json_api_user_data_filter_out_relationships_dict = json_api_user_data_filter_out_relationships_instance.to_dict()
# create an instance of JsonApiUserDataFilterOutRelationships from a dict
json_api_user_data_filter_out_relationships_from_dict = JsonApiUserDataFilterOutRelationships.from_dict(json_api_user_data_filter_out_relationships_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


