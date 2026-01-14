# AacTab

Dashboard tabs (for tabbed dashboards).

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier of the tab. | 
**title** | **str** | Display title for the tab. | 
**filters** | [**{str: (AacDashboardFilter,)}**](AacDashboardFilter.md) | Tab-specific filters. | [optional] 
**sections** | [**[AacSection]**](AacSection.md) | Sections within the tab. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


