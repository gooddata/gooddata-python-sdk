# JsonApiMetricPostOptionalId

JSON:API representation of metric entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiMetricInAttributes**](JsonApiMetricInAttributes.md) |  | 
**id** | **str** | API identifier of an object | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_metric_post_optional_id import JsonApiMetricPostOptionalId

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiMetricPostOptionalId from a JSON string
json_api_metric_post_optional_id_instance = JsonApiMetricPostOptionalId.from_json(json)
# print the JSON string representation of the object
print(JsonApiMetricPostOptionalId.to_json())

# convert the object into a dict
json_api_metric_post_optional_id_dict = json_api_metric_post_optional_id_instance.to_dict()
# create an instance of JsonApiMetricPostOptionalId from a dict
json_api_metric_post_optional_id_from_dict = JsonApiMetricPostOptionalId.from_dict(json_api_metric_post_optional_id_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


