# CustomOverride

Custom cell value overrides (IDs will be replaced with specified values).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**labels** | [**Dict[str, CustomLabel]**](CustomLabel.md) | Map of CustomLabels with keys used as placeholders in document. | [optional] 
**metrics** | [**Dict[str, CustomMetric]**](CustomMetric.md) | Map of CustomMetrics with keys used as placeholders in document. | [optional] 

## Example

```python
from gooddata_api_client.models.custom_override import CustomOverride

# TODO update the JSON string below
json = "{}"
# create an instance of CustomOverride from a JSON string
custom_override_instance = CustomOverride.from_json(json)
# print the JSON string representation of the object
print(CustomOverride.to_json())

# convert the object into a dict
custom_override_dict = custom_override_instance.to_dict()
# create an instance of CustomOverride from a dict
custom_override_from_dict = CustomOverride.from_dict(custom_override_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


