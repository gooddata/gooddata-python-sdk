# gooddata_api_client.model.total_dimension.TotalDimension

A list of dimensions across which the total will be computed. Total headers for only these dimensions will be returned in the result.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A list of dimensions across which the total will be computed. Total headers for only these dimensions will be returned in the result. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[totalDimensionItems](#totalDimensionItems)** | list, tuple,  | tuple,  | List of dimension items which will be used for total computation. The total is a grand total in this dimension if the list is empty or it includes the first dimension item from the dimension definition, and its data and header will be returned in a separate &#x60;ExecutionResultGrandTotal&#x60; structure. Otherwise, it is a subtotal and the data will be integrated into the main result. | 
**dimensionIdentifier** | str,  | str,  | An identifier of a dimension for which the total will be computed. | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# totalDimensionItems

List of dimension items which will be used for total computation. The total is a grand total in this dimension if the list is empty or it includes the first dimension item from the dimension definition, and its data and header will be returned in a separate `ExecutionResultGrandTotal` structure. Otherwise, it is a subtotal and the data will be integrated into the main result.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | List of dimension items which will be used for total computation. The total is a grand total in this dimension if the list is empty or it includes the first dimension item from the dimension definition, and its data and header will be returned in a separate &#x60;ExecutionResultGrandTotal&#x60; structure. Otherwise, it is a subtotal and the data will be integrated into the main result. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

