# JsonApiDatasetOutAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**are_relations_valid** | **bool** |  | [optional] 
**data_source_table_id** | **str** |  | [optional] 
**data_source_table_path** | **List[str]** | Path to database table. | [optional] 
**description** | **str** |  | [optional] 
**grain** | [**List[JsonApiDatasetOutAttributesGrainInner]**](JsonApiDatasetOutAttributesGrainInner.md) |  | [optional] 
**precedence** | **int** |  | [optional] 
**reference_properties** | [**List[JsonApiDatasetOutAttributesReferencePropertiesInner]**](JsonApiDatasetOutAttributesReferencePropertiesInner.md) |  | [optional] 
**sql** | [**JsonApiDatasetOutAttributesSql**](JsonApiDatasetOutAttributesSql.md) |  | [optional] 
**tags** | **List[str]** |  | [optional] 
**title** | **str** |  | [optional] 
**type** | **str** |  | 
**workspace_data_filter_columns** | [**List[JsonApiDatasetOutAttributesWorkspaceDataFilterColumnsInner]**](JsonApiDatasetOutAttributesWorkspaceDataFilterColumnsInner.md) |  | [optional] 
**workspace_data_filter_references** | [**List[JsonApiDatasetOutAttributesWorkspaceDataFilterReferencesInner]**](JsonApiDatasetOutAttributesWorkspaceDataFilterReferencesInner.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_dataset_out_attributes import JsonApiDatasetOutAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiDatasetOutAttributes from a JSON string
json_api_dataset_out_attributes_instance = JsonApiDatasetOutAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiDatasetOutAttributes.to_json())

# convert the object into a dict
json_api_dataset_out_attributes_dict = json_api_dataset_out_attributes_instance.to_dict()
# create an instance of JsonApiDatasetOutAttributes from a dict
json_api_dataset_out_attributes_from_dict = JsonApiDatasetOutAttributes.from_dict(json_api_dataset_out_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


