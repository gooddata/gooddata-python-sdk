# JsonApiAggregatedFactOutAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**are_relations_valid** | **bool** |  | [optional] 
**description** | **str** |  | [optional] 
**operation** | **str** |  | 
**source_column** | **str** |  | [optional] 
**source_column_data_type** | **str** |  | [optional] 
**tags** | **List[str]** |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_aggregated_fact_out_attributes import JsonApiAggregatedFactOutAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAggregatedFactOutAttributes from a JSON string
json_api_aggregated_fact_out_attributes_instance = JsonApiAggregatedFactOutAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiAggregatedFactOutAttributes.to_json())

# convert the object into a dict
json_api_aggregated_fact_out_attributes_dict = json_api_aggregated_fact_out_attributes_instance.to_dict()
# create an instance of JsonApiAggregatedFactOutAttributes from a dict
json_api_aggregated_fact_out_attributes_from_dict = JsonApiAggregatedFactOutAttributes.from_dict(json_api_aggregated_fact_out_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


