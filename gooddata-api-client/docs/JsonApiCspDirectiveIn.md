# JsonApiCspDirectiveIn

JSON:API representation of cspDirective entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiCspDirectiveInAttributes**](JsonApiCspDirectiveInAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_csp_directive_in import JsonApiCspDirectiveIn

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiCspDirectiveIn from a JSON string
json_api_csp_directive_in_instance = JsonApiCspDirectiveIn.from_json(json)
# print the JSON string representation of the object
print(JsonApiCspDirectiveIn.to_json())

# convert the object into a dict
json_api_csp_directive_in_dict = json_api_csp_directive_in_instance.to_dict()
# create an instance of JsonApiCspDirectiveIn from a dict
json_api_csp_directive_in_from_dict = JsonApiCspDirectiveIn.from_dict(json_api_csp_directive_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


