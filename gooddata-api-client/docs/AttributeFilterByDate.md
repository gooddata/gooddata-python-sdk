# AttributeFilterByDate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**filter_local_identifier** | **str** |  | 
**is_common_date** | **bool** |  | 

## Example

```python
from gooddata_api_client.models.attribute_filter_by_date import AttributeFilterByDate

# TODO update the JSON string below
json = "{}"
# create an instance of AttributeFilterByDate from a JSON string
attribute_filter_by_date_instance = AttributeFilterByDate.from_json(json)
# print the JSON string representation of the object
print(AttributeFilterByDate.to_json())

# convert the object into a dict
attribute_filter_by_date_dict = attribute_filter_by_date_instance.to_dict()
# create an instance of AttributeFilterByDate from a dict
attribute_filter_by_date_from_dict = AttributeFilterByDate.from_dict(attribute_filter_by_date_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


