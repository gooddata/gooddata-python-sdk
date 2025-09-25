# LocalIdentifier


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**format** | **str** | Metric format. | [optional] [default to '#,##0.00']
**local_identifier** | **str** | Local identifier of the metric to be compared. | 
**title** | **str** | Metric title. | [optional] 

## Example

```python
from gooddata_api_client.models.local_identifier import LocalIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of LocalIdentifier from a JSON string
local_identifier_instance = LocalIdentifier.from_json(json)
# print the JSON string representation of the object
print(LocalIdentifier.to_json())

# convert the object into a dict
local_identifier_dict = local_identifier_instance.to_dict()
# create an instance of LocalIdentifier from a dict
local_identifier_from_dict = LocalIdentifier.from_dict(local_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


