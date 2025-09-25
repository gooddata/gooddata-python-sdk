# DeclarativeAttribute

A dataset attribute.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Attribute ID. | 
**labels** | [**[DeclarativeLabel]**](DeclarativeLabel.md) | An array of attribute labels. | 
**source_column** | **str** | A name of the source column that is the primary label | 
**title** | **str** | Attribute title. | 
**default_view** | [**LabelIdentifier**](LabelIdentifier.md) |  | [optional] 
**description** | **str** | Attribute description. | [optional] 
**is_hidden** | **bool** | If true, this attribute is hidden from AI search results. | [optional] 
**sort_column** | **str** | Attribute sort column. | [optional] 
**sort_direction** | **str** | Attribute sort direction. | [optional] 
**source_column_data_type** | **str** | A type of the source column | [optional] 
**tags** | **[str]** | A list of tags. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


