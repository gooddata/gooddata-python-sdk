# AacDataset

AAC dataset definition.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier of the dataset. | 
**type** | **str** | Dataset type discriminator. | 
**data_source** | **str** | Data source ID. | [optional] 
**description** | **str** | Dataset description. | [optional] 
**fields** | [**{str: (AacField,)}**](AacField.md) | Dataset fields (attributes, facts, aggregated facts). | [optional] 
**precedence** | **int** | Precedence value for aggregate awareness. | [optional] 
**primary_key** | [**AacDatasetPrimaryKey**](AacDatasetPrimaryKey.md) |  | [optional] 
**references** | [**[AacReference]**](AacReference.md) | References to other datasets. | [optional] 
**sql** | **str** | SQL statement defining this dataset. | [optional] 
**table_path** | **str** | Table path in the data source. | [optional] 
**tags** | **[str]** | Metadata tags. | [optional] 
**title** | **str** | Human readable title. | [optional] 
**workspace_data_filters** | [**[AacWorkspaceDataFilter]**](AacWorkspaceDataFilter.md) | Workspace data filters. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


