# Dimension

Single dimension description.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**item_identifiers** | **[str]** | List of items in current dimension. Can reference &#39;localIdentifier&#39; from &#39;AttributeItem&#39;, or special pseudo attribute \&quot;measureGroup\&quot; representing list of metrics. | 
**local_identifier** | **str** | Dimension identification within requests. Other entities can reference this dimension by this value. | [optional] 
**sorting** | [**[SortKey]**](SortKey.md) | List of sorting rules. From most relevant to least relevant (less relevant rule is applied, when more relevant rule compares items as equal). | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


