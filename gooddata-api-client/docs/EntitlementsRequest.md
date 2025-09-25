# EntitlementsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**entitlements_name** | **List[str]** |  | 

## Example

```python
from gooddata_api_client.models.entitlements_request import EntitlementsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of EntitlementsRequest from a JSON string
entitlements_request_instance = EntitlementsRequest.from_json(json)
# print the JSON string representation of the object
print(EntitlementsRequest.to_json())

# convert the object into a dict
entitlements_request_dict = entitlements_request_instance.to_dict()
# create an instance of EntitlementsRequest from a dict
entitlements_request_from_dict = EntitlementsRequest.from_dict(entitlements_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


