# Dimension

Single dimension description.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**item_identifiers** | **List[str]** | List of items in current dimension. Can reference &#39;localIdentifier&#39; from &#39;AttributeItem&#39;, or special pseudo attribute \&quot;measureGroup\&quot; representing list of metrics. | 
**local_identifier** | **str** | Dimension identification within requests. Other entities can reference this dimension by this value. | [optional] 
**sorting** | [**List[SortKey]**](SortKey.md) | List of sorting rules. From most relevant to least relevant (less relevant rule is applied, when more relevant rule compares items as equal). | [optional] 

## Example

```python
from gooddata_api_client.models.dimension import Dimension

# TODO update the JSON string below
json = "{}"
# create an instance of Dimension from a JSON string
dimension_instance = Dimension.from_json(json)
# print the JSON string representation of the object
print(Dimension.to_json())

# convert the object into a dict
dimension_dict = dimension_instance.to_dict()
# create an instance of Dimension from a dict
dimension_from_dict = Dimension.from_dict(dimension_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


