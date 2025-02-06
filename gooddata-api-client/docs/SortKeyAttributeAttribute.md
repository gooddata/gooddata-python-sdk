# SortKeyAttributeAttribute


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attribute_identifier** | **str** | Item reference (to &#39;itemIdentifiers&#39;) referencing, which item should be used for sorting. Only references to attributes are allowed. | 
**direction** | **str** | Sorting elements - ascending/descending order. | [optional] 
**sort_type** | **str** | Mechanism by which this attribute should be sorted. Available options are: - DEFAULT: sorting based on default rules (using sort column if defined, otherwise this label)  - LABEL: sorting by this label values  - ATTRIBUTE: sorting by values of this label&#39;s attribute (or rather the primary label)  - ATTRIBUTE: sorting by values of this label&#39;s attribute (or rather the primary label)- AREA: sorting by area (total or subtotal) corresponding to each attribute value. The area is computed by summing up all metric values in all other dimensions. | [optional]  if omitted the server will use the default value of "DEFAULT"
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


