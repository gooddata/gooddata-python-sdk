# JsonApiLlmEndpointOut

JSON:API representation of llmEndpoint entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiLlmEndpointOutAttributes**](JsonApiLlmEndpointOutAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_llm_endpoint_out import JsonApiLlmEndpointOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiLlmEndpointOut from a JSON string
json_api_llm_endpoint_out_instance = JsonApiLlmEndpointOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiLlmEndpointOut.to_json())

# convert the object into a dict
json_api_llm_endpoint_out_dict = json_api_llm_endpoint_out_instance.to_dict()
# create an instance of JsonApiLlmEndpointOut from a dict
json_api_llm_endpoint_out_from_dict = JsonApiLlmEndpointOut.from_dict(json_api_llm_endpoint_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


