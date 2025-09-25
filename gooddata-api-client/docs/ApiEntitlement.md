# ApiEntitlement


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**expiry** | **date** |  | [optional] 
**name** | **str** |  | 
**value** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.api_entitlement import ApiEntitlement

# TODO update the JSON string below
json = "{}"
# create an instance of ApiEntitlement from a JSON string
api_entitlement_instance = ApiEntitlement.from_json(json)
# print the JSON string representation of the object
print(ApiEntitlement.to_json())

# convert the object into a dict
api_entitlement_dict = api_entitlement_instance.to_dict()
# create an instance of ApiEntitlement from a dict
api_entitlement_from_dict = ApiEntitlement.from_dict(api_entitlement_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


