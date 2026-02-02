# AllowedRelationshipType

Allowed relationship type combination.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**source_type** | **str** | Source object type (e.g., &#39;dashboard&#39;, &#39;visualization&#39;, &#39;metric&#39;). | 
**target_type** | **str** | Target object type (e.g., &#39;visualization&#39;, &#39;metric&#39;, &#39;attribute&#39;). | 
**allow_orphans** | **bool** | If true, allows target objects that are not part of any relationship (orphans) to be included in results. If false, orphan target objects will be excluded even if they directly match the search query. Default is true (orphans are allowed). | [optional]  if omitted the server will use the default value of True
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


