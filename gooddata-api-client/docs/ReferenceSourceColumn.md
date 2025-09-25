# ReferenceSourceColumn


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**column** | **str** |  | 
**data_type** | **str** |  | [optional] 
**target** | [**DatasetGrain**](DatasetGrain.md) |  | 

## Example

```python
from gooddata_api_client.models.reference_source_column import ReferenceSourceColumn

# TODO update the JSON string below
json = "{}"
# create an instance of ReferenceSourceColumn from a JSON string
reference_source_column_instance = ReferenceSourceColumn.from_json(json)
# print the JSON string representation of the object
print(ReferenceSourceColumn.to_json())

# convert the object into a dict
reference_source_column_dict = reference_source_column_instance.to_dict()
# create an instance of ReferenceSourceColumn from a dict
reference_source_column_from_dict = ReferenceSourceColumn.from_dict(reference_source_column_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


