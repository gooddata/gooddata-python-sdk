# RawCustomOverride

Custom cell value overrides (IDs will be replaced with specified values).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**labels** | [**Dict[str, RawCustomLabel]**](RawCustomLabel.md) | Map of CustomLabels with keys used as placeholders in export result. | [optional] 
**metrics** | [**Dict[str, RawCustomMetric]**](RawCustomMetric.md) | Map of CustomMetrics with keys used as placeholders in export result. | [optional] 

## Example

```python
from gooddata_api_client.models.raw_custom_override import RawCustomOverride

# TODO update the JSON string below
json = "{}"
# create an instance of RawCustomOverride from a JSON string
raw_custom_override_instance = RawCustomOverride.from_json(json)
# print the JSON string representation of the object
print(RawCustomOverride.to_json())

# convert the object into a dict
raw_custom_override_dict = raw_custom_override_instance.to_dict()
# create an instance of RawCustomOverride from a dict
raw_custom_override_from_dict = RawCustomOverride.from_dict(raw_custom_override_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


