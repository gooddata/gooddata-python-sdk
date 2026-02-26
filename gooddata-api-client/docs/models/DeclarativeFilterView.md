# gooddata_api_client.model.declarative_filter_view.DeclarativeFilterView

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**id** | str,  | str,  | FilterView object ID. | 
**title** | str,  | str,  |  | 
**analyticalDashboard** | [**DeclarativeAnalyticalDashboardIdentifier**](DeclarativeAnalyticalDashboardIdentifier.md) | [**DeclarativeAnalyticalDashboardIdentifier**](DeclarativeAnalyticalDashboardIdentifier.md) |  | [optional] 
**content** | [**JsonNode**](JsonNode.md) | [**JsonNode**](JsonNode.md) |  | [optional] 
**description** | str,  | str,  |  | [optional] 
**isDefault** | bool,  | BoolClass,  | Indicator whether the filter view should by applied by default. | [optional] 
**[tags](#tags)** | list, tuple,  | tuple,  |  | [optional] 
**user** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# tags

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  | A list of tags. | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

