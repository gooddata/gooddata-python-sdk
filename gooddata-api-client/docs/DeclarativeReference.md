# DeclarativeReference

A dataset reference.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**identifier** | [**ReferenceIdentifier**](ReferenceIdentifier.md) |  | 
**multivalue** | **bool** | The multi-value flag enables many-to-many cardinality for references. | 
**source_column_data_types** | **[str]** | An array of source column data types for a given reference. Deprecated, use &#39;sources&#39; instead. | [optional] 
**source_columns** | **[str]** | An array of source column names for a given reference. Deprecated, use &#39;sources&#39; instead. | [optional] 
**sources** | [**[DeclarativeReferenceSource]**](DeclarativeReferenceSource.md) | An array of source columns for a given reference. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


