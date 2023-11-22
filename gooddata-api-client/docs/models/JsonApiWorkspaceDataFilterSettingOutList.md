# gooddata_api_client.model.json_api_workspace_data_filter_setting_out_list.JsonApiWorkspaceDataFilterSettingOutList

A JSON:API document with a list of resources

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A JSON:API document with a list of resources | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[data](#data)** | list, tuple,  | tuple,  |  | 
**[included](#included)** | list, tuple,  | tuple,  | Included resources | [optional] 
**links** | [**ListLinks**](ListLinks.md) | [**ListLinks**](ListLinks.md) |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# data

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**JsonApiWorkspaceDataFilterSettingOutWithLinks**](JsonApiWorkspaceDataFilterSettingOutWithLinks.md) | [**JsonApiWorkspaceDataFilterSettingOutWithLinks**](JsonApiWorkspaceDataFilterSettingOutWithLinks.md) | [**JsonApiWorkspaceDataFilterSettingOutWithLinks**](JsonApiWorkspaceDataFilterSettingOutWithLinks.md) |  | 

# included

Included resources

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Included resources | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**JsonApiWorkspaceDataFilterOutWithLinks**](JsonApiWorkspaceDataFilterOutWithLinks.md) | [**JsonApiWorkspaceDataFilterOutWithLinks**](JsonApiWorkspaceDataFilterOutWithLinks.md) | [**JsonApiWorkspaceDataFilterOutWithLinks**](JsonApiWorkspaceDataFilterOutWithLinks.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

