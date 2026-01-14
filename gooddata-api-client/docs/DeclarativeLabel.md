# DeclarativeLabel

A attribute label.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Label ID. | 
**source_column** | **str** | A name of the source column in the table. | 
**title** | **str** | Label title. | 
**description** | **str** | Label description. | [optional] 
**geo_area_config** | [**GeoAreaConfig**](GeoAreaConfig.md) |  | [optional] 
**is_hidden** | **bool** | Determines if the label is hidden from AI features. | [optional] 
**is_nullable** | **bool** | Flag indicating whether the associated source column allows null values. | [optional] 
**locale** | **str** | Default label locale. | [optional] 
**null_value** | **str** | Value used in coalesce during joins instead of null. | [optional] 
**source_column_data_type** | **str** | A type of the source column | [optional] 
**tags** | **[str]** | A list of tags. | [optional] 
**translations** | [**[DeclarativeLabelTranslation]**](DeclarativeLabelTranslation.md) | Other translations. | [optional] 
**value_type** | **str** | Specific type of label | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


