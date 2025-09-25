# DeclarativeDataset

A dataset defined by its properties.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**aggregated_facts** | [**List[DeclarativeAggregatedFact]**](DeclarativeAggregatedFact.md) | An array of aggregated facts. | [optional] 
**attributes** | [**List[DeclarativeAttribute]**](DeclarativeAttribute.md) | An array of attributes. | [optional] 
**data_source_table_id** | [**DataSourceTableIdentifier**](DataSourceTableIdentifier.md) |  | [optional] 
**description** | **str** | A dataset description. | [optional] 
**facts** | [**List[DeclarativeFact]**](DeclarativeFact.md) | An array of facts. | [optional] 
**grain** | [**List[GrainIdentifier]**](GrainIdentifier.md) | An array of grain identifiers. | 
**id** | **str** | The Dataset ID. This ID is further used to refer to this instance of dataset. | 
**precedence** | **int** | Precedence used in aggregate awareness. | [optional] 
**references** | [**List[DeclarativeReference]**](DeclarativeReference.md) | An array of references. | 
**sql** | [**DeclarativeDatasetSql**](DeclarativeDatasetSql.md) |  | [optional] 
**tags** | **List[str]** | A list of tags. | [optional] 
**title** | **str** | A dataset title. | 
**workspace_data_filter_columns** | [**List[DeclarativeWorkspaceDataFilterColumn]**](DeclarativeWorkspaceDataFilterColumn.md) | An array of columns which are available for match to implicit workspace data filters. | [optional] 
**workspace_data_filter_references** | [**List[DeclarativeWorkspaceDataFilterReferences]**](DeclarativeWorkspaceDataFilterReferences.md) | An array of explicit workspace data filters. | [optional] 

## Example

```python
from gooddata_api_client.models.declarative_dataset import DeclarativeDataset

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeDataset from a JSON string
declarative_dataset_instance = DeclarativeDataset.from_json(json)
# print the JSON string representation of the object
print(DeclarativeDataset.to_json())

# convert the object into a dict
declarative_dataset_dict = declarative_dataset_instance.to_dict()
# create an instance of DeclarativeDataset from a dict
declarative_dataset_from_dict = DeclarativeDataset.from_dict(declarative_dataset_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


