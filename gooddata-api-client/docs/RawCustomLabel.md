# RawCustomLabel

Custom label object override.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | Override value. | 

## Example

```python
from gooddata_api_client.models.raw_custom_label import RawCustomLabel

# TODO update the JSON string below
json = "{}"
# create an instance of RawCustomLabel from a JSON string
raw_custom_label_instance = RawCustomLabel.from_json(json)
# print the JSON string representation of the object
print(RawCustomLabel.to_json())

# convert the object into a dict
raw_custom_label_dict = raw_custom_label_instance.to_dict()
# create an instance of RawCustomLabel from a dict
raw_custom_label_from_dict = RawCustomLabel.from_dict(raw_custom_label_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


