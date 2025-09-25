# ColumnStatisticsRequestFrom


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sql** | **str** |  | 
**table_name** | **str** |  | 

## Example

```python
from gooddata_api_client.models.column_statistics_request_from import ColumnStatisticsRequestFrom

# TODO update the JSON string below
json = "{}"
# create an instance of ColumnStatisticsRequestFrom from a JSON string
column_statistics_request_from_instance = ColumnStatisticsRequestFrom.from_json(json)
# print the JSON string representation of the object
print(ColumnStatisticsRequestFrom.to_json())

# convert the object into a dict
column_statistics_request_from_dict = column_statistics_request_from_instance.to_dict()
# create an instance of ColumnStatisticsRequestFrom from a dict
column_statistics_request_from_from_dict = ColumnStatisticsRequestFrom.from_dict(column_statistics_request_from_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


