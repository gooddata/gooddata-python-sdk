# JsonApiLlmEndpointOutWithLinks


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiLlmEndpointOutAttributes**](JsonApiLlmEndpointOutAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_llm_endpoint_out_with_links import JsonApiLlmEndpointOutWithLinks

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiLlmEndpointOutWithLinks from a JSON string
json_api_llm_endpoint_out_with_links_instance = JsonApiLlmEndpointOutWithLinks.from_json(json)
# print the JSON string representation of the object
print(JsonApiLlmEndpointOutWithLinks.to_json())

# convert the object into a dict
json_api_llm_endpoint_out_with_links_dict = json_api_llm_endpoint_out_with_links_instance.to_dict()
# create an instance of JsonApiLlmEndpointOutWithLinks from a dict
json_api_llm_endpoint_out_with_links_from_dict = JsonApiLlmEndpointOutWithLinks.from_dict(json_api_llm_endpoint_out_with_links_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


