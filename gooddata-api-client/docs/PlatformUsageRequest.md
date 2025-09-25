# PlatformUsageRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**usage_item_names** | **List[str]** |  | 

## Example

```python
from gooddata_api_client.models.platform_usage_request import PlatformUsageRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PlatformUsageRequest from a JSON string
platform_usage_request_instance = PlatformUsageRequest.from_json(json)
# print the JSON string representation of the object
print(PlatformUsageRequest.to_json())

# convert the object into a dict
platform_usage_request_dict = platform_usage_request_instance.to_dict()
# create an instance of PlatformUsageRequest from a dict
platform_usage_request_from_dict = PlatformUsageRequest.from_dict(platform_usage_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


