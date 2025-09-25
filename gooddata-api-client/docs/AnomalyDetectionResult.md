# AnomalyDetectionResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**anomaly_flag** | **List[Optional[bool]]** |  | 
**attribute** | **List[str]** |  | 
**values** | **List[Optional[float]]** |  | 

## Example

```python
from gooddata_api_client.models.anomaly_detection_result import AnomalyDetectionResult

# TODO update the JSON string below
json = "{}"
# create an instance of AnomalyDetectionResult from a JSON string
anomaly_detection_result_instance = AnomalyDetectionResult.from_json(json)
# print the JSON string representation of the object
print(AnomalyDetectionResult.to_json())

# convert the object into a dict
anomaly_detection_result_dict = anomaly_detection_result_instance.to_dict()
# create an instance of AnomalyDetectionResult from a dict
anomaly_detection_result_from_dict = AnomalyDetectionResult.from_dict(anomaly_detection_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


