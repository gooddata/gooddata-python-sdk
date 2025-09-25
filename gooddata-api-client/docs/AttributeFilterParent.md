# AttributeFilterParent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**filter_local_identifier** | **str** |  | 
**over** | [**Over**](Over.md) |  | 

## Example

```python
from gooddata_api_client.models.attribute_filter_parent import AttributeFilterParent

# TODO update the JSON string below
json = "{}"
# create an instance of AttributeFilterParent from a JSON string
attribute_filter_parent_instance = AttributeFilterParent.from_json(json)
# print the JSON string representation of the object
print(AttributeFilterParent.to_json())

# convert the object into a dict
attribute_filter_parent_dict = attribute_filter_parent_instance.to_dict()
# create an instance of AttributeFilterParent from a dict
attribute_filter_parent_from_dict = AttributeFilterParent.from_dict(attribute_filter_parent_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


