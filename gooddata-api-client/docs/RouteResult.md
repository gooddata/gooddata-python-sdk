# RouteResult

Question -> Use Case routing. May contain final answer is a special use case is not required.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reasoning** | **str** | Explanation why LLM picked this use case. | 
**use_case** | **str** | Use case where LLM routed based on question. | 

## Example

```python
from gooddata_api_client.models.route_result import RouteResult

# TODO update the JSON string below
json = "{}"
# create an instance of RouteResult from a JSON string
route_result_instance = RouteResult.from_json(json)
# print the JSON string representation of the object
print(RouteResult.to_json())

# convert the object into a dict
route_result_dict = route_result_instance.to_dict()
# create an instance of RouteResult from a dict
route_result_from_dict = RouteResult.from_dict(route_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


