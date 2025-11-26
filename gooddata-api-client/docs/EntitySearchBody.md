# EntitySearchBody

Request body for entity search operations

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**filter** | **str, none_type** | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
**includes** | **[str], none_type** | List of related entities to include in the response | [optional] 
**meta_include** | **[str], none_type** | Set of metadata fields to include in the response | [optional] 
**page** | [**EntitySearchPage**](EntitySearchPage.md) |  | [optional] 
**sort** | [**[EntitySearchSort], none_type**](EntitySearchSort.md) | Sorting criteria (can specify multiple sort orders) | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


