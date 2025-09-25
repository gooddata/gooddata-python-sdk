# DimAttribute

List of attributes representing the dimensionality of the new visualization

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | ID of the object | 
**title** | **str** | Title of attribute. | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.dim_attribute import DimAttribute

# TODO update the JSON string below
json = "{}"
# create an instance of DimAttribute from a JSON string
dim_attribute_instance = DimAttribute.from_json(json)
# print the JSON string representation of the object
print(DimAttribute.to_json())

# convert the object into a dict
dim_attribute_dict = dim_attribute_instance.to_dict()
# create an instance of DimAttribute from a dict
dim_attribute_from_dict = DimAttribute.from_dict(dim_attribute_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


