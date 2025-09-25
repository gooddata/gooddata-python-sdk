# ScanRequest

A request containing all information critical to model scanning.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**scan_tables** | **bool** | A flag indicating whether the tables should be scanned. | 
**scan_views** | **bool** | A flag indicating whether the views should be scanned. | 
**schemata** | **List[str]** | What schemata will be scanned. | [optional] 
**separator** | **str** | A separator between prefixes and the names. | 
**table_prefix** | **str** | Tables starting with this prefix will be scanned. The prefix is then followed by the value of &#x60;separator&#x60; parameter. Given the table prefix is &#x60;out_table&#x60; and separator is &#x60;__&#x60;, the table with name like &#x60;out_table__customers&#x60; will be scanned. | [optional] 
**view_prefix** | **str** | Views starting with this prefix will be scanned. The prefix is then followed by the value of &#x60;separator&#x60; parameter. Given the view prefix is &#x60;out_view&#x60; and separator is &#x60;__&#x60;, the table with name like &#x60;out_view__us_customers&#x60; will be scanned. | [optional] 

## Example

```python
from gooddata_api_client.models.scan_request import ScanRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ScanRequest from a JSON string
scan_request_instance = ScanRequest.from_json(json)
# print the JSON string representation of the object
print(ScanRequest.to_json())

# convert the object into a dict
scan_request_dict = scan_request_instance.to_dict()
# create an instance of ScanRequest from a dict
scan_request_from_dict = ScanRequest.from_dict(scan_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


