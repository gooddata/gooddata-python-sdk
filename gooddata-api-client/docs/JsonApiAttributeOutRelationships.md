# JsonApiAttributeOutRelationships


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attribute_hierarchies** | [**JsonApiAttributeOutRelationshipsAttributeHierarchies**](JsonApiAttributeOutRelationshipsAttributeHierarchies.md) |  | [optional] 
**dataset** | [**JsonApiAggregatedFactOutRelationshipsDataset**](JsonApiAggregatedFactOutRelationshipsDataset.md) |  | [optional] 
**default_view** | [**JsonApiAttributeOutRelationshipsDefaultView**](JsonApiAttributeOutRelationshipsDefaultView.md) |  | [optional] 
**labels** | [**JsonApiAnalyticalDashboardOutRelationshipsLabels**](JsonApiAnalyticalDashboardOutRelationshipsLabels.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_attribute_out_relationships import JsonApiAttributeOutRelationships

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAttributeOutRelationships from a JSON string
json_api_attribute_out_relationships_instance = JsonApiAttributeOutRelationships.from_json(json)
# print the JSON string representation of the object
print(JsonApiAttributeOutRelationships.to_json())

# convert the object into a dict
json_api_attribute_out_relationships_dict = json_api_attribute_out_relationships_instance.to_dict()
# create an instance of JsonApiAttributeOutRelationships from a dict
json_api_attribute_out_relationships_from_dict = JsonApiAttributeOutRelationships.from_dict(json_api_attribute_out_relationships_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


