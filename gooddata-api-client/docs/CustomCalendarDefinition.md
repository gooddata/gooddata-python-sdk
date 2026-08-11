# CustomCalendarDefinition

Calendar backed by custom fiscal calendar tables defined per data source.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_source_tables** | [**{str: (CalendarTableReference,)}**](CalendarTableReference.md) | Custom fiscal calendar table per data source ID. | 
**type** | **str** |  | defaults to "custom"
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


