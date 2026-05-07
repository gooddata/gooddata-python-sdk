# DeclarativeDataset

A dataset defined by its properties.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**grain** | [**[GrainIdentifier]**](GrainIdentifier.md) | An array of grain identifiers. | 
**id** | **str** | The Dataset ID. This ID is further used to refer to this instance of dataset. | 
**references** | [**[DeclarativeReference]**](DeclarativeReference.md) | An array of references. The semantics of &#x60;sources&#x60; depends on the dataset shape: for NORMAL→NORMAL references, &#x60;sources&#x60; is a compound foreign key to the target dataset&#39;s grain (one source per grain component, dataType-matched). For pre-aggregation datasets (NORMAL with &#x60;aggregatedFacts&#x60;), &#x60;sources&#x60; is reinterpreted as independent column→attribute mappings — one entry per source — and targets are NOT required to be grain components. | 
**title** | **str** | A dataset title. | 
**aggregated_facts** | [**[DeclarativeAggregatedFact]**](DeclarativeAggregatedFact.md) | An array of aggregated facts. Presence makes the dataset a pre-aggregation dataset, which requires &#x60;precedence &gt; 0&#x60; and must NOT be set on AUXILIARY datasets. | [optional] 
**attributes** | [**[DeclarativeAttribute]**](DeclarativeAttribute.md) | An array of attributes. | [optional] 
**data_source_table_id** | [**DataSourceTableIdentifier**](DataSourceTableIdentifier.md) |  | [optional] 
**description** | **str** | A dataset description. | [optional] 
**facts** | [**[DeclarativeFact]**](DeclarativeFact.md) | An array of facts. | [optional] 
**precedence** | **int** | Precedence used in aggregate awareness. Pre-aggregation datasets (NORMAL with &#x60;aggregatedFacts&#x60;) MUST set &#x60;precedence &gt; 0&#x60;; non-pre-aggregation datasets MUST leave it null. Must NOT be set on AUXILIARY datasets. | [optional] 
**sql** | [**DeclarativeDatasetSql**](DeclarativeDatasetSql.md) |  | [optional] 
**tags** | **[str]** | A list of tags. | [optional] 
**type** | **str** | Dataset type. NORMAL is the standard fact/dim dataset. AUXILIARY denotes a synthetic dataset used as a reference target by pre-aggregation datasets (keystone of the aggregate-awareness design); AUX datasets must not carry &#x60;aggregatedFacts&#x60;, &#x60;sql&#x60;, &#x60;dataSourceTableId&#x60;, &#x60;workspaceDataFilterReferences&#x60; or &#x60;precedence&#x60;. Date datasets use a separate schema and are not represented by this enum. | [optional] 
**workspace_data_filter_columns** | [**[DeclarativeWorkspaceDataFilterColumn]**](DeclarativeWorkspaceDataFilterColumn.md) | An array of columns which are available for match to implicit workspace data filters. | [optional] 
**workspace_data_filter_references** | [**[DeclarativeWorkspaceDataFilterReferences]**](DeclarativeWorkspaceDataFilterReferences.md) | An array of explicit workspace data filters. Must NOT be set on AUXILIARY datasets. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


