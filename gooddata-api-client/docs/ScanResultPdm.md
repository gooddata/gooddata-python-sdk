# ScanResultPdm

Result of scan of data source physical model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pdm** | [**DeclarativeTables**](DeclarativeTables.md) |  | 
**warnings** | [**List[TableWarning]**](TableWarning.md) |  | 

## Example

```python
from gooddata_api_client.models.scan_result_pdm import ScanResultPdm

# TODO update the JSON string below
json = "{}"
# create an instance of ScanResultPdm from a JSON string
scan_result_pdm_instance = ScanResultPdm.from_json(json)
# print the JSON string representation of the object
print(ScanResultPdm.to_json())

# convert the object into a dict
scan_result_pdm_dict = scan_result_pdm_instance.to_dict()
# create an instance of ScanResultPdm from a dict
scan_result_pdm_from_dict = ScanResultPdm.from_dict(scan_result_pdm_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


