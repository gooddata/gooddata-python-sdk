# ResolvedLlmEndpoint


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Endpoint Id | 
**title** | **str** | Endpoint Title | 

## Example

```python
from gooddata_api_client.models.resolved_llm_endpoint import ResolvedLlmEndpoint

# TODO update the JSON string below
json = "{}"
# create an instance of ResolvedLlmEndpoint from a JSON string
resolved_llm_endpoint_instance = ResolvedLlmEndpoint.from_json(json)
# print the JSON string representation of the object
print(ResolvedLlmEndpoint.to_json())

# convert the object into a dict
resolved_llm_endpoint_dict = resolved_llm_endpoint_instance.to_dict()
# create an instance of ResolvedLlmEndpoint from a dict
resolved_llm_endpoint_from_dict = ResolvedLlmEndpoint.from_dict(resolved_llm_endpoint_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


