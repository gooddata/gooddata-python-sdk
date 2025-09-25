# RelativeDateFilter

A date filter specifying a time interval that is relative to the current date. For example, last week, next month, and so on. Field dataset is representing qualifier of date dimension. The 'from' and 'to' properties mark the boundaries of the interval. If 'from' is omitted, all values earlier than 'to' are included. If 'to' is omitted, all values later than 'from' are included. It is not allowed to omit both.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**relative_date_filter** | [**RelativeDateFilterRelativeDateFilter**](RelativeDateFilterRelativeDateFilter.md) |  | 

## Example

```python
from gooddata_api_client.models.relative_date_filter import RelativeDateFilter

# TODO update the JSON string below
json = "{}"
# create an instance of RelativeDateFilter from a JSON string
relative_date_filter_instance = RelativeDateFilter.from_json(json)
# print the JSON string representation of the object
print(RelativeDateFilter.to_json())

# convert the object into a dict
relative_date_filter_dict = relative_date_filter_instance.to_dict()
# create an instance of RelativeDateFilter from a dict
relative_date_filter_from_dict = RelativeDateFilter.from_dict(relative_date_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


