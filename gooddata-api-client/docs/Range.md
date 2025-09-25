# Range


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_from** | [**Value**](Value.md) |  | 
**measure** | [**LocalIdentifier**](LocalIdentifier.md) |  | 
**operator** | **str** |  | 
**to** | [**Value**](Value.md) |  | 

## Example

```python
from gooddata_api_client.models.range import Range

# TODO update the JSON string below
json = "{}"
# create an instance of Range from a JSON string
range_instance = Range.from_json(json)
# print the JSON string representation of the object
print(Range.to_json())

# convert the object into a dict
range_dict = range_instance.to_dict()
# create an instance of Range from a dict
range_from_dict = Range.from_dict(range_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


