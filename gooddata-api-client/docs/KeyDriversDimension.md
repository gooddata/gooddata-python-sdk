# KeyDriversDimension


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attribute** | [**RestApiIdentifier**](RestApiIdentifier.md) |  | 
**attribute_name** | **str** |  | 
**format** | [**AttributeFormat**](AttributeFormat.md) |  | [optional] 
**granularity** | **str** |  | [optional] 
**label** | [**RestApiIdentifier**](RestApiIdentifier.md) |  | 
**label_name** | **str** |  | 
**value_type** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.key_drivers_dimension import KeyDriversDimension

# TODO update the JSON string below
json = "{}"
# create an instance of KeyDriversDimension from a JSON string
key_drivers_dimension_instance = KeyDriversDimension.from_json(json)
# print the JSON string representation of the object
print(KeyDriversDimension.to_json())

# convert the object into a dict
key_drivers_dimension_dict = key_drivers_dimension_instance.to_dict()
# create an instance of KeyDriversDimension from a dict
key_drivers_dimension_from_dict = KeyDriversDimension.from_dict(key_drivers_dimension_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


