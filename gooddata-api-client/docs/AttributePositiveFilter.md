# AttributePositiveFilter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**include** | **List[str]** |  | 
**using** | **str** |  | 

## Example

```python
from gooddata_api_client.models.attribute_positive_filter import AttributePositiveFilter

# TODO update the JSON string below
json = "{}"
# create an instance of AttributePositiveFilter from a JSON string
attribute_positive_filter_instance = AttributePositiveFilter.from_json(json)
# print the JSON string representation of the object
print(AttributePositiveFilter.to_json())

# convert the object into a dict
attribute_positive_filter_dict = attribute_positive_filter_instance.to_dict()
# create an instance of AttributePositiveFilter from a dict
attribute_positive_filter_from_dict = AttributePositiveFilter.from_dict(attribute_positive_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


