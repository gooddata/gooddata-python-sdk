# AttributeHeaderAttributeHeader


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attribute** | [**RestApiIdentifier**](RestApiIdentifier.md) |  | 
**attribute_name** | **str** | Attribute name. | 
**label** | [**RestApiIdentifier**](RestApiIdentifier.md) |  | 
**label_name** | **str** | Label name. | 
**local_identifier** | **str** | Local identifier of the attribute this header relates to. | 
**primary_label** | [**RestApiIdentifier**](RestApiIdentifier.md) |  | 
**data_type** | **str** | Data type of the attribute values, only filled for computed attributes. | [optional] 
**format** | [**AttributeFormat**](AttributeFormat.md) |  | [optional] 
**geo_area_config** | [**GeoAreaConfig**](GeoAreaConfig.md) |  | [optional] 
**granularity** | **str** | Date granularity of the attribute, only filled for date attributes. | [optional] 
**number_format** | **str** | Format to be used to format the attribute values, the same kind of format string as the measure format. Only filled for computed attributes with a format. | [optional] 
**value_type** | **str** | Attribute value type. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


