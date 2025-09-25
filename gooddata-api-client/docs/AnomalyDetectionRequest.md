# AnomalyDetectionRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sensitivity** | **float** | Anomaly detection sensitivity. | 

## Example

```python
from gooddata_api_client.models.anomaly_detection_request import AnomalyDetectionRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AnomalyDetectionRequest from a JSON string
anomaly_detection_request_instance = AnomalyDetectionRequest.from_json(json)
# print the JSON string representation of the object
print(AnomalyDetectionRequest.to_json())

# convert the object into a dict
anomaly_detection_request_dict = anomaly_detection_request_instance.to_dict()
# create an instance of AnomalyDetectionRequest from a dict
anomaly_detection_request_from_dict = AnomalyDetectionRequest.from_dict(anomaly_detection_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


