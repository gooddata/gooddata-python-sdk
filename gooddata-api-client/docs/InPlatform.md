# InPlatform

In-platform destination for notifications.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | The destination type. | 

## Example

```python
from gooddata_api_client.models.in_platform import InPlatform

# TODO update the JSON string below
json = "{}"
# create an instance of InPlatform from a JSON string
in_platform_instance = InPlatform.from_json(json)
# print the JSON string representation of the object
print(InPlatform.to_json())

# convert the object into a dict
in_platform_dict = in_platform_instance.to_dict()
# create an instance of InPlatform from a dict
in_platform_from_dict = InPlatform.from_dict(in_platform_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


