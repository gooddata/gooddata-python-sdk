# JsonApiEntitlementOutAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**expiry** | **date** |  | [optional] 
**value** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_entitlement_out_attributes import JsonApiEntitlementOutAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiEntitlementOutAttributes from a JSON string
json_api_entitlement_out_attributes_instance = JsonApiEntitlementOutAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiEntitlementOutAttributes.to_json())

# convert the object into a dict
json_api_entitlement_out_attributes_dict = json_api_entitlement_out_attributes_instance.to_dict()
# create an instance of JsonApiEntitlementOutAttributes from a dict
json_api_entitlement_out_attributes_from_dict = JsonApiEntitlementOutAttributes.from_dict(json_api_entitlement_out_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


