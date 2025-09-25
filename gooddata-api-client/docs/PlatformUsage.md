# PlatformUsage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** |  | [optional] 
**name** | **str** |  | 

## Example

```python
from gooddata_api_client.models.platform_usage import PlatformUsage

# TODO update the JSON string below
json = "{}"
# create an instance of PlatformUsage from a JSON string
platform_usage_instance = PlatformUsage.from_json(json)
# print the JSON string representation of the object
print(PlatformUsage.to_json())

# convert the object into a dict
platform_usage_dict = platform_usage_instance.to_dict()
# create an instance of PlatformUsage from a dict
platform_usage_from_dict = PlatformUsage.from_dict(platform_usage_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


