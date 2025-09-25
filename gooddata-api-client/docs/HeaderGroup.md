# HeaderGroup

Contains the information specific for a group of headers. These groups correlate to attributes and metric groups.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**headers** | [**List[ExecutionResultHeader]**](ExecutionResultHeader.md) | An array containing headers. | 

## Example

```python
from gooddata_api_client.models.header_group import HeaderGroup

# TODO update the JSON string below
json = "{}"
# create an instance of HeaderGroup from a JSON string
header_group_instance = HeaderGroup.from_json(json)
# print the JSON string representation of the object
print(HeaderGroup.to_json())

# convert the object into a dict
header_group_dict = header_group_instance.to_dict()
# create an instance of HeaderGroup from a dict
header_group_from_dict = HeaderGroup.from_dict(header_group_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


