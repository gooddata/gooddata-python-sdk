# AttributeNegativeFilter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**exclude** | **List[str]** |  | 
**using** | **str** |  | 

## Example

```python
from gooddata_api_client.models.attribute_negative_filter import AttributeNegativeFilter

# TODO update the JSON string below
json = "{}"
# create an instance of AttributeNegativeFilter from a JSON string
attribute_negative_filter_instance = AttributeNegativeFilter.from_json(json)
# print the JSON string representation of the object
print(AttributeNegativeFilter.to_json())

# convert the object into a dict
attribute_negative_filter_dict = attribute_negative_filter_instance.to_dict()
# create an instance of AttributeNegativeFilter from a dict
attribute_negative_filter_from_dict = AttributeNegativeFilter.from_dict(attribute_negative_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


