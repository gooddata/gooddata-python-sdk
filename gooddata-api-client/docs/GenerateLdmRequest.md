# GenerateLdmRequest

A request containing all information needed for generation of logical model.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**date_granularities** | **str** | Option to control date granularities for date datasets. Empty value enables common date granularities (DAY, WEEK, MONTH, QUARTER, YEAR). Default value is &#x60;all&#x60; which enables all available date granularities, including time granularities (like hours, minutes). | [optional] 
**denorm_prefix** | **str** | Columns starting with this prefix will be considered as denormalization references. The prefix is then followed by the value of &#x60;separator&#x60; parameter. Given the denormalization reference prefix is &#x60;dr&#x60; and separator is &#x60;__&#x60;, the columns with name like &#x60;dr__customer_name&#x60; will be considered as denormalization references. | [optional] 
**fact_prefix** | **str** | Columns starting with this prefix will be considered as facts. The prefix is then followed by the value of &#x60;separator&#x60; parameter. Given the fact prefix is &#x60;f&#x60; and separator is &#x60;__&#x60;, the columns with name like &#x60;f__sold&#x60; will be considered as facts. | [optional] 
**generate_long_ids** | **bool** | A flag dictating how the attribute, fact and label ids are generated. By default their ids are derived only from the column name, unless there would be a conflict (e.g. category coming from two different tables). In that case a long id format of &#x60;&lt;table&gt;.&lt;column&gt;&#x60; is used. If the flag is set to true, then all ids will be generated in the long form. | [optional] 
**grain_prefix** | **str** | Columns starting with this prefix will be considered as grains. The prefix is then followed by the value of &#x60;separator&#x60; parameter. Given the grain prefix is &#x60;g&#x60; and separator is &#x60;__&#x60;, the columns with name like &#x60;g__name&#x60; will be considered as grains. | [optional] 
**grain_reference_prefix** | **str** | Columns starting with this prefix will be considered as grain references. The prefix is then followed by the value of &#x60;separator&#x60; parameter. Given the reference prefix is &#x60;gr&#x60; and separator is &#x60;__&#x60;, the columns with name like &#x60;gr__customer_name&#x60; will be considered as grain references. | [optional] 
**pdm** | [**PdmLdmRequest**](PdmLdmRequest.md) |  | [optional] 
**primary_label_prefix** | **str** | Columns starting with this prefix will be considered as primary labels. The prefix is then followed by the value of &#x60;separator&#x60; parameter. Given the primary label prefix is &#x60;pl&#x60; and separator is &#x60;__&#x60;, the columns with name like &#x60;pl__country_id&#x60; will be considered as primary labels. | [optional] 
**reference_prefix** | **str** | Columns starting with this prefix will be considered as references. The prefix is then followed by the value of &#x60;separator&#x60; parameter. Given the reference prefix is &#x60;r&#x60; and separator is &#x60;__&#x60;, the columns with name like &#x60;r__customer_name&#x60; will be considered as references. | [optional] 
**secondary_label_prefix** | **str** | Columns starting with this prefix will be considered as secondary labels. The prefix is then followed by the value of &#x60;separator&#x60; parameter. Given the secondary label prefix is &#x60;sl&#x60; and separator is &#x60;__&#x60;, the columns with name like &#x60;sl__country_id_country_name&#x60; will be considered as secondary labels. | [optional] 
**separator** | **str** | A separator between prefixes and the names. Default is \&quot;__\&quot;. | [optional]  if omitted the server will use the default value of "__"
**table_prefix** | **str** | Tables starting with this prefix will be included. The prefix is then followed by the value of &#x60;separator&#x60; parameter. Given the table prefix is &#x60;out_table&#x60; and separator is &#x60;__&#x60;, the table with name like &#x60;out_table__customers&#x60; will be scanned. | [optional] 
**view_prefix** | **str** | Views starting with this prefix will be included. The prefix is then followed by the value of &#x60;separator&#x60; parameter. Given the view prefix is &#x60;out_view&#x60; and separator is &#x60;__&#x60;, the table with name like &#x60;out_view__us_customers&#x60; will be scanned. | [optional] 
**wdf_prefix** | **str** | Column serving as workspace data filter. No labels are auto generated for such columns. | [optional] 
**workspace_id** | **str** | Optional workspace id. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


