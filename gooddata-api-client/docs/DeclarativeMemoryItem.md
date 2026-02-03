# DeclarativeMemoryItem


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Memory item ID. | 
**instruction** | **str** | The text that will be injected into the system prompt. | 
**strategy** | **str** | Strategy defining when the memory item should be applied | 
**title** | **str** | Memory item title. | 
**created_at** | **str, none_type** | Time of the entity creation. | [optional] 
**created_by** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**description** | **str** | Memory item description. | [optional] 
**is_disabled** | **bool** | Whether memory item is disabled. | [optional] 
**keywords** | **[str]** | Set of unique strings used for semantic similarity filtering. | [optional] 
**modified_at** | **str, none_type** | Time of the last entity modification. | [optional] 
**modified_by** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**tags** | **[str]** | A list of tags. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


