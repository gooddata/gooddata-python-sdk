# FilterBy

Specifies what is used for filtering.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label_type** | **str** | Specifies which label is used for filtering - primary or requested. | [optional] [default to 'REQUESTED']

## Example

```python
from gooddata_api_client.models.filter_by import FilterBy

# TODO update the JSON string below
json = "{}"
# create an instance of FilterBy from a JSON string
filter_by_instance = FilterBy.from_json(json)
# print the JSON string representation of the object
print(FilterBy.to_json())

# convert the object into a dict
filter_by_dict = filter_by_instance.to_dict()
# create an instance of FilterBy from a dict
filter_by_from_dict = FilterBy.from_dict(filter_by_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


