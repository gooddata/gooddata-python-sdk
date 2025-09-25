# MemoryItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Memory item ID | 
**instruction** | **str** | Instruction that will be injected into the prompt. | 
**keywords** | **List[str]** | List of keywords used to match the memory item. | 
**strategy** | **str** | Defines the application strategy. | [optional] 
**use_cases** | [**MemoryItemUseCases**](MemoryItemUseCases.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.memory_item import MemoryItem

# TODO update the JSON string below
json = "{}"
# create an instance of MemoryItem from a JSON string
memory_item_instance = MemoryItem.from_json(json)
# print the JSON string representation of the object
print(MemoryItem.to_json())

# convert the object into a dict
memory_item_dict = memory_item_instance.to_dict()
# create an instance of MemoryItem from a dict
memory_item_from_dict = MemoryItem.from_dict(memory_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


