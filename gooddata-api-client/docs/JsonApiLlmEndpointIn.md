# JsonApiLlmEndpointIn

JSON:API representation of llmEndpoint entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiLlmEndpointInAttributes**](JsonApiLlmEndpointInAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_llm_endpoint_in import JsonApiLlmEndpointIn

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiLlmEndpointIn from a JSON string
json_api_llm_endpoint_in_instance = JsonApiLlmEndpointIn.from_json(json)
# print the JSON string representation of the object
print(JsonApiLlmEndpointIn.to_json())

# convert the object into a dict
json_api_llm_endpoint_in_dict = json_api_llm_endpoint_in_instance.to_dict()
# create an instance of JsonApiLlmEndpointIn from a dict
json_api_llm_endpoint_in_from_dict = JsonApiLlmEndpointIn.from_dict(json_api_llm_endpoint_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


