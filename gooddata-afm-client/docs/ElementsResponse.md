# ElementsResponse

Entity holding list of sorted & filtered label elements, related primary label of attribute owning requested label and paging.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**primary_label** | [**ObjectIdentifier**](ObjectIdentifier.md) |  | 
**elements** | [**[Element]**](Element.md) | List of returned elements. | 
**paging** | [**Paging**](Paging.md) |  | 
**total_count_without_filters** | **int** | Total count of items ignoring all filters (using on &#x60;&#x60;&#x60;project&#x60;&#x60;&#x60; and  &#x60;&#x60;&#x60;label&#x60;&#x60;&#x60; from request). | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


