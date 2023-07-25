# gooddata_api_client.model.generate_ldm_request.GenerateLdmRequest

A request containing all information needed for generation of logical model.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A request containing all information needed for generation of logical model. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**dateGranularities** | str,  | str,  | Option to control date granularities for date datasets. Empty value enables common date granularities (DAY, WEEK, MONTH, QUARTER, YEAR). Default value is &#x60;all&#x60; which enables all available date granularities, including time granularities (like hours, minutes). | [optional] 
**denormPrefix** | str,  | str,  | Columns starting with this prefix will be considered as denormalization references. The prefix is then followed by the value of &#x60;separator&#x60; parameter. Given the denormalization reference prefix is &#x60;dr&#x60; and separator is &#x60;__&#x60;, the columns with name like &#x60;dr__customer_name&#x60; will be considered as denormalization references. | [optional] 
**factPrefix** | str,  | str,  | Columns starting with this prefix will be considered as facts. The prefix is then followed by the value of &#x60;separator&#x60; parameter. Given the fact prefix is &#x60;f&#x60; and separator is &#x60;__&#x60;, the columns with name like &#x60;f__sold&#x60; will be considered as facts. | [optional] 
**generateLongIds** | bool,  | BoolClass,  | A flag dictating how the attribute, fact and label ids are generated. By default their ids are derived only from the column name, unless there would be a conflict (e.g. category coming from two different tables). In that case a long id format of &#x60;&lt;table&gt;.&lt;column&gt;&#x60; is used. If the flag is set to true, then all ids will be generated in the long form. | [optional] 
**grainPrefix** | str,  | str,  | Columns starting with this prefix will be considered as grains. The prefix is then followed by the value of &#x60;separator&#x60; parameter. Given the grain prefix is &#x60;g&#x60; and separator is &#x60;__&#x60;, the columns with name like &#x60;g__name&#x60; will be considered as grains. | [optional] 
**grainReferencePrefix** | str,  | str,  | Columns starting with this prefix will be considered as grain references. The prefix is then followed by the value of &#x60;separator&#x60; parameter. Given the reference prefix is &#x60;gr&#x60; and separator is &#x60;__&#x60;, the columns with name like &#x60;gr__customer_name&#x60; will be considered as grain references. | [optional] 
**pdm** | [**PdmLdmRequest**](PdmLdmRequest.md) | [**PdmLdmRequest**](PdmLdmRequest.md) |  | [optional] 
**primaryLabelPrefix** | str,  | str,  | Columns starting with this prefix will be considered as primary labels. The prefix is then followed by the value of &#x60;separator&#x60; parameter. Given the primary label prefix is &#x60;pl&#x60; and separator is &#x60;__&#x60;, the columns with name like &#x60;pl__country_id&#x60; will be considered as primary labels. | [optional] 
**referencePrefix** | str,  | str,  | Columns starting with this prefix will be considered as references. The prefix is then followed by the value of &#x60;separator&#x60; parameter. Given the reference prefix is &#x60;r&#x60; and separator is &#x60;__&#x60;, the columns with name like &#x60;r__customer_name&#x60; will be considered as references. | [optional] 
**secondaryLabelPrefix** | str,  | str,  | Columns starting with this prefix will be considered as secondary labels. The prefix is then followed by the value of &#x60;separator&#x60; parameter. Given the secondary label prefix is &#x60;sl&#x60; and separator is &#x60;__&#x60;, the columns with name like &#x60;sl__country_id_country_name&#x60; will be considered as secondary labels. | [optional] 
**separator** | str,  | str,  | A separator between prefixes and the names. Default is \&quot;__\&quot;. | [optional] if omitted the server will use the default value of "__"
**tablePrefix** | str,  | str,  | Tables starting with this prefix will be included. The prefix is then followed by the value of &#x60;separator&#x60; parameter. Given the table prefix is &#x60;out_table&#x60; and separator is &#x60;__&#x60;, the table with name like &#x60;out_table__customers&#x60; will be scanned. | [optional] 
**viewPrefix** | str,  | str,  | Views starting with this prefix will be included. The prefix is then followed by the value of &#x60;separator&#x60; parameter. Given the view prefix is &#x60;out_view&#x60; and separator is &#x60;__&#x60;, the table with name like &#x60;out_view__us_customers&#x60; will be scanned. | [optional] 
**wdfPrefix** | str,  | str,  | Column serving as workspace data filter. No labels are auto generated for such columns. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

