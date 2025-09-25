# ColumnStatisticsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**frequency** | [**Frequency**](Frequency.md) |  | [optional] 
**histogram** | [**Histogram**](Histogram.md) |  | [optional] 
**statistics** | [**List[ColumnStatistic]**](ColumnStatistic.md) |  | [optional] 
**warnings** | [**List[ColumnStatisticWarning]**](ColumnStatisticWarning.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.column_statistics_response import ColumnStatisticsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ColumnStatisticsResponse from a JSON string
column_statistics_response_instance = ColumnStatisticsResponse.from_json(json)
# print the JSON string representation of the object
print(ColumnStatisticsResponse.to_json())

# convert the object into a dict
column_statistics_response_dict = column_statistics_response_instance.to_dict()
# create an instance of ColumnStatisticsResponse from a dict
column_statistics_response_from_dict = ColumnStatisticsResponse.from_dict(column_statistics_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


