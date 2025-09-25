# JsonApiEntitlementOut

JSON:API representation of entitlement entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiEntitlementOutAttributes**](JsonApiEntitlementOutAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_entitlement_out import JsonApiEntitlementOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiEntitlementOut from a JSON string
json_api_entitlement_out_instance = JsonApiEntitlementOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiEntitlementOut.to_json())

# convert the object into a dict
json_api_entitlement_out_dict = json_api_entitlement_out_instance.to_dict()
# create an instance of JsonApiEntitlementOut from a dict
json_api_entitlement_out_from_dict = JsonApiEntitlementOut.from_dict(json_api_entitlement_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


