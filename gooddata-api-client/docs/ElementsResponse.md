# ElementsResponse

Entity holding list of sorted & filtered label elements, related primary label of attribute owning requested label and paging.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**elements** | [**[Element]**](Element.md) | List of returned elements. | 
**paging** | [**Paging**](Paging.md) |  | 
**primary_label** | [**RestApiIdentifier**](RestApiIdentifier.md) |  | 
**cache_id** | **str** | The client can use this in subsequent requests (like paging or search) to get results from the same point in time as the previous request. This is useful when the underlying data source has caches disabled and the client wants to avoid seeing inconsistent results and to also avoid excessive queries to the database itself. | [optional] 
**data_type** | **str** | Data type of the element values, only filled for computed attributes. | [optional] 
**format** | [**AttributeFormat**](AttributeFormat.md) |  | [optional] 
**granularity** | **str** | Granularity of requested label in case of date attribute | [optional] 
**number_format** | **str** | Format to be used to format the element values, the same kind of format string as the measure format. Only filled for computed attributes with a format. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


