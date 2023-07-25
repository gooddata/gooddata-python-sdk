# gooddata_api_client.model.sort_key_attribute.SortKeyAttribute

Sorting rule for sorting by attribute value in current dimension.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Sorting rule for sorting by attribute value in current dimension. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[attribute](#attribute)** | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# attribute

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**attributeIdentifier** | str,  | str,  | Item reference (to &#x27;itemIdentifiers&#x27;) referencing, which item should be used for sorting. Only references to attributes are allowed. | 
**direction** | str,  | str,  | Sorting elements - ascending/descending order. | [optional] must be one of ["ASC", "DESC", ] 
**sortType** | str,  | str,  | Mechanism by which this attribute should be sorted. Available options are: - DEFAULT: sorting based on default rules (using sort column if defined, otherwise this label)  - LABEL: sorting by this label values  - ATTRIBUTE: sorting by values of this label&#x27;s attribute (or rather the primary label)  - AREA: sorting by area (total or subtotal) corresponding to each attribute value. The area is computed by summing up all metric values in all other dimensions. | [optional] must be one of ["DEFAULT", "LABEL", "ATTRIBUTE", "AREA", ] if omitted the server will use the default value of "DEFAULT"
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

