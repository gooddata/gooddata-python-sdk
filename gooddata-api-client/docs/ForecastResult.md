# ForecastResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attribute** | **List[str]** |  | 
**lower_bound** | **List[Optional[float]]** |  | 
**origin** | **List[Optional[float]]** |  | 
**prediction** | **List[Optional[float]]** |  | 
**upper_bound** | **List[Optional[float]]** |  | 

## Example

```python
from gooddata_api_client.models.forecast_result import ForecastResult

# TODO update the JSON string below
json = "{}"
# create an instance of ForecastResult from a JSON string
forecast_result_instance = ForecastResult.from_json(json)
# print the JSON string representation of the object
print(ForecastResult.to_json())

# convert the object into a dict
forecast_result_dict = forecast_result_instance.to_dict()
# create an instance of ForecastResult from a dict
forecast_result_from_dict = ForecastResult.from_dict(forecast_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


