# ResolveSettingsRequest

A request containing setting IDs to resolve.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**settings** | **List[str]** | An array of setting IDs to resolve. | 

## Example

```python
from gooddata_api_client.models.resolve_settings_request import ResolveSettingsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ResolveSettingsRequest from a JSON string
resolve_settings_request_instance = ResolveSettingsRequest.from_json(json)
# print the JSON string representation of the object
print(ResolveSettingsRequest.to_json())

# convert the object into a dict
resolve_settings_request_dict = resolve_settings_request_instance.to_dict()
# create an instance of ResolveSettingsRequest from a dict
resolve_settings_request_from_dict = ResolveSettingsRequest.from_dict(resolve_settings_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


