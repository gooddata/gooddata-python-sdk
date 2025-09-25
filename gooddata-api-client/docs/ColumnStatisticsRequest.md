# ColumnStatisticsRequest

A request to retrieve statistics for a column.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**column_name** | **str** |  | 
**frequency** | [**FrequencyProperties**](FrequencyProperties.md) |  | [optional] 
**var_from** | [**ColumnStatisticsRequestFrom**](ColumnStatisticsRequestFrom.md) |  | 
**histogram** | [**HistogramProperties**](HistogramProperties.md) |  | [optional] 
**statistics** | **List[str]** |  | [optional] 

## Example

```python
from gooddata_api_client.models.column_statistics_request import ColumnStatisticsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ColumnStatisticsRequest from a JSON string
column_statistics_request_instance = ColumnStatisticsRequest.from_json(json)
# print the JSON string representation of the object
print(ColumnStatisticsRequest.to_json())

# convert the object into a dict
column_statistics_request_dict = column_statistics_request_instance.to_dict()
# create an instance of ColumnStatisticsRequest from a dict
column_statistics_request_from_dict = ColumnStatisticsRequest.from_dict(column_statistics_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


