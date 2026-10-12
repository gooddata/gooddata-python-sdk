# FlowTableResult

A page of a table result.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | [**[FlowColumn]**](FlowColumn.md) | Columns of the page, in order. | 
**data** | **[[{str: (bool, date, datetime, dict, float, int, list, str, none_type)}]]** | Rows of the page. A row has one value for each column, in the order of the columns. | 
**paging** | [**FlowTablePaging**](FlowTablePaging.md) |  | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


