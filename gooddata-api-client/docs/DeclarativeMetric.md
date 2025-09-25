# DeclarativeMetric


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **object** | Free-form JSON object | 
**created_at** | **str** | Time of the entity creation. | [optional] 
**created_by** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**description** | **str** | Metric description. | [optional] 
**id** | **str** | Metric ID. | 
**modified_at** | **str** | Time of the last entity modification. | [optional] 
**modified_by** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**tags** | **List[str]** | A list of tags. | [optional] 
**title** | **str** | Metric title. | 

## Example

```python
from gooddata_api_client.models.declarative_metric import DeclarativeMetric

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeMetric from a JSON string
declarative_metric_instance = DeclarativeMetric.from_json(json)
# print the JSON string representation of the object
print(DeclarativeMetric.to_json())

# convert the object into a dict
declarative_metric_dict = declarative_metric_instance.to_dict()
# create an instance of DeclarativeMetric from a dict
declarative_metric_from_dict = DeclarativeMetric.from_dict(declarative_metric_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


