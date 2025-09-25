# DependentEntitiesResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**graph** | [**DependentEntitiesGraph**](DependentEntitiesGraph.md) |  | 

## Example

```python
from gooddata_api_client.models.dependent_entities_response import DependentEntitiesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DependentEntitiesResponse from a JSON string
dependent_entities_response_instance = DependentEntitiesResponse.from_json(json)
# print the JSON string representation of the object
print(DependentEntitiesResponse.to_json())

# convert the object into a dict
dependent_entities_response_dict = dependent_entities_response_instance.to_dict()
# create an instance of DependentEntitiesResponse from a dict
dependent_entities_response_from_dict = DependentEntitiesResponse.from_dict(dependent_entities_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


