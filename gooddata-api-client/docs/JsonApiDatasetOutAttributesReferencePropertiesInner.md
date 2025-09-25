# JsonApiDatasetOutAttributesReferencePropertiesInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**identifier** | [**DatasetReferenceIdentifier**](DatasetReferenceIdentifier.md) |  | 
**multivalue** | **bool** |  | 
**source_column_data_types** | **List[str]** |  | [optional] 
**source_columns** | **List[str]** |  | [optional] 
**sources** | [**List[ReferenceSourceColumn]**](ReferenceSourceColumn.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_dataset_out_attributes_reference_properties_inner import JsonApiDatasetOutAttributesReferencePropertiesInner

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiDatasetOutAttributesReferencePropertiesInner from a JSON string
json_api_dataset_out_attributes_reference_properties_inner_instance = JsonApiDatasetOutAttributesReferencePropertiesInner.from_json(json)
# print the JSON string representation of the object
print(JsonApiDatasetOutAttributesReferencePropertiesInner.to_json())

# convert the object into a dict
json_api_dataset_out_attributes_reference_properties_inner_dict = json_api_dataset_out_attributes_reference_properties_inner_instance.to_dict()
# create an instance of JsonApiDatasetOutAttributesReferencePropertiesInner from a dict
json_api_dataset_out_attributes_reference_properties_inner_from_dict = JsonApiDatasetOutAttributesReferencePropertiesInner.from_dict(json_api_dataset_out_attributes_reference_properties_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


