# DeclarativeComputedAttribute


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | [**DeclarativeComputedAttributeContent**](DeclarativeComputedAttributeContent.md) |  | 
**id** | **str** | Computed attribute ID. | 
**title** | **str** | Computed attribute title. | 
**certification** | **str** | Certification status of the entity. | [optional]  if omitted the server will use the default value of "CERTIFIED"
**certification_message** | **str, none_type** | Optional message associated with the certification. | [optional] 
**certified_at** | **str, none_type** | Time when the certification was set. | [optional] 
**certified_by** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**created_at** | **str, none_type** | Time of the entity creation. | [optional] 
**created_by** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**data_type** | **str** | Computed attribute data type | [optional] 
**description** | **str** | Computed attribute description. | [optional] 
**is_hidden** | **bool** | If true, this computed attribute is hidden from AI search results. | [optional] 
**is_nullable** | **bool** | Flag indicating whether the associated source column allows null values. | [optional] 
**locale** | **str** | Default locale for primary computed label. | [optional] 
**modified_at** | **str, none_type** | Time of the last entity modification. | [optional] 
**modified_by** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**null_value** | **str** | Value used in coalesce during joins instead of null. | [optional] 
**tags** | **[str]** | A list of tags. | [optional] 
**value_type** | **str** | Specific type of the computed attribute value | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


