# ValidateByItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Specifies entity used for valid elements computation. | 
**type** | **str** | Specifies entity type which could be label, attribute, fact, or metric. | 

## Example

```python
from gooddata_api_client.models.validate_by_item import ValidateByItem

# TODO update the JSON string below
json = "{}"
# create an instance of ValidateByItem from a JSON string
validate_by_item_instance = ValidateByItem.from_json(json)
# print the JSON string representation of the object
print(ValidateByItem.to_json())

# convert the object into a dict
validate_by_item_dict = validate_by_item_instance.to_dict()
# create an instance of ValidateByItem from a dict
validate_by_item_from_dict = ValidateByItem.from_dict(validate_by_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


