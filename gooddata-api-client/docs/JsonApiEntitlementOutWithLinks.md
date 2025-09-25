# JsonApiEntitlementOutWithLinks


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiEntitlementOutAttributes**](JsonApiEntitlementOutAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_entitlement_out_with_links import JsonApiEntitlementOutWithLinks

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiEntitlementOutWithLinks from a JSON string
json_api_entitlement_out_with_links_instance = JsonApiEntitlementOutWithLinks.from_json(json)
# print the JSON string representation of the object
print(JsonApiEntitlementOutWithLinks.to_json())

# convert the object into a dict
json_api_entitlement_out_with_links_dict = json_api_entitlement_out_with_links_instance.to_dict()
# create an instance of JsonApiEntitlementOutWithLinks from a dict
json_api_entitlement_out_with_links_from_dict = JsonApiEntitlementOutWithLinks.from_dict(json_api_entitlement_out_with_links_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


