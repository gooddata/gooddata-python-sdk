# ColumnStatisticWarning


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | **str** |  | 
**message** | **str** |  | 

## Example

```python
from gooddata_api_client.models.column_statistic_warning import ColumnStatisticWarning

# TODO update the JSON string below
json = "{}"
# create an instance of ColumnStatisticWarning from a JSON string
column_statistic_warning_instance = ColumnStatisticWarning.from_json(json)
# print the JSON string representation of the object
print(ColumnStatisticWarning.to_json())

# convert the object into a dict
column_statistic_warning_dict = column_statistic_warning_instance.to_dict()
# create an instance of ColumnStatisticWarning from a dict
column_statistic_warning_from_dict = ColumnStatisticWarning.from_dict(column_statistic_warning_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


