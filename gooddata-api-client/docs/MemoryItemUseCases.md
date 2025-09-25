# MemoryItemUseCases

Defines the prompts where the given instruction should be applied.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**general** | **bool** | Apply this memory item to the general answer prompt. | 
**howto** | **bool** | Apply this memory item to the how-to prompt. | 
**keywords** | **bool** | Apply this memory item to the search keyword extraction prompt. | 
**metric** | **bool** | Apply this memory item to the metric selection prompt. | 
**normalize** | **bool** | Apply this memory item to the normalize prompt. | 
**router** | **bool** | Appy this memory item to the router prompt. | 
**search** | **bool** | Apply this memory item to the search prompt. | 
**visualization** | **bool** | Apply this memory item to the visualization prompt. | 

## Example

```python
from gooddata_api_client.models.memory_item_use_cases import MemoryItemUseCases

# TODO update the JSON string below
json = "{}"
# create an instance of MemoryItemUseCases from a JSON string
memory_item_use_cases_instance = MemoryItemUseCases.from_json(json)
# print the JSON string representation of the object
print(MemoryItemUseCases.to_json())

# convert the object into a dict
memory_item_use_cases_dict = memory_item_use_cases_instance.to_dict()
# create an instance of MemoryItemUseCases from a dict
memory_item_use_cases_from_dict = MemoryItemUseCases.from_dict(memory_item_use_cases_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


