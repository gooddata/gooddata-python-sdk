# ColumnStatistic


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**value** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.column_statistic import ColumnStatistic

# TODO update the JSON string below
json = "{}"
# create an instance of ColumnStatistic from a JSON string
column_statistic_instance = ColumnStatistic.from_json(json)
# print the JSON string representation of the object
print(ColumnStatistic.to_json())

# convert the object into a dict
column_statistic_dict = column_statistic_instance.to_dict()
# create an instance of ColumnStatistic from a dict
column_statistic_from_dict = ColumnStatistic.from_dict(column_statistic_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


