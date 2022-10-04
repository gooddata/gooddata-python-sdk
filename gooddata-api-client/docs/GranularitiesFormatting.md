# GranularitiesFormatting

A date dataset granularities title formatting rules.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title_base** | **str** | Title base is used as a token in title pattern. If left empty, it is replaced by date dataset title. | 
**title_pattern** | **str** | This pattern is used to generate the title of attributes and labels that result from the granularities. There are two tokens available:  * &#x60;%titleBase&#x60; - represents shared part by all titles, or title of Date Dataset if left empty * &#x60;%granularityTitle&#x60; - represents &#x60;DateGranularity&#x60; built-in title | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


