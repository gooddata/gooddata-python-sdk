# KeyDriversRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**aux_metrics** | [**List[MeasureItem]**](MeasureItem.md) | Additional metrics to be included in the computation, but excluded from the analysis. | [optional] 
**metric** | [**MeasureItem**](MeasureItem.md) |  | 
**sort_direction** | **str** | Sorting elements - ascending/descending order. | [optional] [default to 'DESC']

## Example

```python
from gooddata_api_client.models.key_drivers_request import KeyDriversRequest

# TODO update the JSON string below
json = "{}"
# create an instance of KeyDriversRequest from a JSON string
key_drivers_request_instance = KeyDriversRequest.from_json(json)
# print the JSON string representation of the object
print(KeyDriversRequest.to_json())

# convert the object into a dict
key_drivers_request_dict = key_drivers_request_instance.to_dict()
# create an instance of KeyDriversRequest from a dict
key_drivers_request_from_dict = KeyDriversRequest.from_dict(key_drivers_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


