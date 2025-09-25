# UserContext

User context, which can affect the behavior of the underlying AI features.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**active_object** | [**ActiveObjectIdentification**](ActiveObjectIdentification.md) |  | 

## Example

```python
from gooddata_api_client.models.user_context import UserContext

# TODO update the JSON string below
json = "{}"
# create an instance of UserContext from a JSON string
user_context_instance = UserContext.from_json(json)
# print the JSON string representation of the object
print(UserContext.to_json())

# convert the object into a dict
user_context_dict = user_context_instance.to_dict()
# create an instance of UserContext from a dict
user_context_from_dict = UserContext.from_dict(user_context_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


