# AbsoluteDateFilter

A datetime filter specifying exact from and to values.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**absolute_date_filter** | [**AbsoluteDateFilterAbsoluteDateFilter**](AbsoluteDateFilterAbsoluteDateFilter.md) |  | 

## Example

```python
from gooddata_api_client.models.absolute_date_filter import AbsoluteDateFilter

# TODO update the JSON string below
json = "{}"
# create an instance of AbsoluteDateFilter from a JSON string
absolute_date_filter_instance = AbsoluteDateFilter.from_json(json)
# print the JSON string representation of the object
print(AbsoluteDateFilter.to_json())

# convert the object into a dict
absolute_date_filter_dict = absolute_date_filter_instance.to_dict()
# create an instance of AbsoluteDateFilter from a dict
absolute_date_filter_from_dict = AbsoluteDateFilter.from_dict(absolute_date_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


