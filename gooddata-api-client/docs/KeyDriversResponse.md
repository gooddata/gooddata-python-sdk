# KeyDriversResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dimensions** | [**List[KeyDriversDimension]**](KeyDriversDimension.md) |  | 
**links** | [**ExecutionLinks**](ExecutionLinks.md) |  | 

## Example

```python
from gooddata_api_client.models.key_drivers_response import KeyDriversResponse

# TODO update the JSON string below
json = "{}"
# create an instance of KeyDriversResponse from a JSON string
key_drivers_response_instance = KeyDriversResponse.from_json(json)
# print the JSON string representation of the object
print(KeyDriversResponse.to_json())

# convert the object into a dict
key_drivers_response_dict = key_drivers_response_instance.to_dict()
# create an instance of KeyDriversResponse from a dict
key_drivers_response_from_dict = KeyDriversResponse.from_dict(key_drivers_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


