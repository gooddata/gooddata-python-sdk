# CustomLabel

Custom label object override.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | Override value. | 

## Example

```python
from gooddata_api_client.models.custom_label import CustomLabel

# TODO update the JSON string below
json = "{}"
# create an instance of CustomLabel from a JSON string
custom_label_instance = CustomLabel.from_json(json)
# print the JSON string representation of the object
print(CustomLabel.to_json())

# convert the object into a dict
custom_label_dict = custom_label_instance.to_dict()
# create an instance of CustomLabel from a dict
custom_label_from_dict = CustomLabel.from_dict(custom_label_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


