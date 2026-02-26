# gooddata_api_client.model.aac_tab.AacTab

Dashboard tabs (for tabbed dashboards).

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Dashboard tabs (for tabbed dashboards). | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**id** | str,  | str,  | Unique identifier of the tab. | 
**title** | str,  | str,  | Display title for the tab. | 
**[filters](#filters)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | Tab-specific filters. | [optional] 
**[sections](#sections)** | list, tuple,  | tuple,  | Sections within the tab. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# filters

Tab-specific filters.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Tab-specific filters. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**any_string_name** | [**AacDashboardFilter**](AacDashboardFilter.md) | [**AacDashboardFilter**](AacDashboardFilter.md) | any string name can be used but the value must be the correct type | [optional] 

# sections

Sections within the tab.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Sections within the tab. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AacSection**](AacSection.md) | [**AacSection**](AacSection.md) | [**AacSection**](AacSection.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

