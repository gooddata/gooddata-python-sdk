# JsonApiMetricOutIncludes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiDatasetOutAttributes**](JsonApiDatasetOutAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 
**meta** | [**JsonApiAggregatedFactOutMeta**](JsonApiAggregatedFactOutMeta.md) |  | [optional] 
**relationships** | [**JsonApiDatasetOutRelationships**](JsonApiDatasetOutRelationships.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_metric_out_includes import JsonApiMetricOutIncludes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiMetricOutIncludes from a JSON string
json_api_metric_out_includes_instance = JsonApiMetricOutIncludes.from_json(json)
# print the JSON string representation of the object
print(JsonApiMetricOutIncludes.to_json())

# convert the object into a dict
json_api_metric_out_includes_dict = json_api_metric_out_includes_instance.to_dict()
# create an instance of JsonApiMetricOutIncludes from a dict
json_api_metric_out_includes_from_dict = JsonApiMetricOutIncludes.from_dict(json_api_metric_out_includes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


