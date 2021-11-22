# ScanRequest

A request containing all information critical to model scanning.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**separator** | **str** | A separator between prefixes and the names. | 
**scan_tables** | **bool** | A flag indicating whether the tables should be scanned. | 
**scan_views** | **bool** | A flag indicating whether the views should be scanned. | 
**schemata** | **[str]** | What schemata will be scanned. | [optional] 
**table_prefix** | **str** | Tables starting with this prefix will be scanned. The prefix is then followed by the value of &#x60;separator&#x60; parameter. Given the table prefix is &#x60;out_table&#x60; and separator is &#x60;__&#x60;, the table with name like &#x60;out_table__customers&#x60; will be scanned. | [optional] 
**view_prefix** | **str** | Views starting with this prefix will be scanned. The prefix is then followed by the value of &#x60;separator&#x60; parameter. Given the view prefix is &#x60;out_view&#x60; and separator is &#x60;__&#x60;, the table with name like &#x60;out_view__us_customers&#x60; will be scanned. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


