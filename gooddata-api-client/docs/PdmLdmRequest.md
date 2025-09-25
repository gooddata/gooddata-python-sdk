# PdmLdmRequest

PDM additions wrapper.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sqls** | [**List[PdmSql]**](PdmSql.md) | List of SQL datasets. | [optional] 
**table_overrides** | [**List[TableOverride]**](TableOverride.md) | (BETA) List of table overrides. | [optional] 
**tables** | [**List[DeclarativeTable]**](DeclarativeTable.md) | List of physical database tables. | [optional] 

## Example

```python
from gooddata_api_client.models.pdm_ldm_request import PdmLdmRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PdmLdmRequest from a JSON string
pdm_ldm_request_instance = PdmLdmRequest.from_json(json)
# print the JSON string representation of the object
print(PdmLdmRequest.to_json())

# convert the object into a dict
pdm_ldm_request_dict = pdm_ldm_request_instance.to_dict()
# create an instance of PdmLdmRequest from a dict
pdm_ldm_request_from_dict = PdmLdmRequest.from_dict(pdm_ldm_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


