# ElementsResponse

Entity holding list of sorted & filtered label elements, related primary label of attribute owning requested label and paging.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**elements** | [**[Element]**](Element.md) | List of returned elements. | 
**paging** | [**Paging**](Paging.md) |  | 
**primary_label** | [**RestApiIdentifier**](RestApiIdentifier.md) |  | 
**format** | [**AttributeFormat**](AttributeFormat.md) |  | [optional] 
**granularity** | **str** | Granularity of requested label in case of date attribute | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


