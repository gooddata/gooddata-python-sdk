# JsonApiAggregatedFactOutMetaOrigin


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**origin_id** | **str** | defines id of the workspace where the entity comes from | 
**origin_type** | **str** | defines type of the origin of the entity | 

## Example

```python
from gooddata_api_client.models.json_api_aggregated_fact_out_meta_origin import JsonApiAggregatedFactOutMetaOrigin

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAggregatedFactOutMetaOrigin from a JSON string
json_api_aggregated_fact_out_meta_origin_instance = JsonApiAggregatedFactOutMetaOrigin.from_json(json)
# print the JSON string representation of the object
print(JsonApiAggregatedFactOutMetaOrigin.to_json())

# convert the object into a dict
json_api_aggregated_fact_out_meta_origin_dict = json_api_aggregated_fact_out_meta_origin_instance.to_dict()
# create an instance of JsonApiAggregatedFactOutMetaOrigin from a dict
json_api_aggregated_fact_out_meta_origin_from_dict = JsonApiAggregatedFactOutMetaOrigin.from_dict(json_api_aggregated_fact_out_meta_origin_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


