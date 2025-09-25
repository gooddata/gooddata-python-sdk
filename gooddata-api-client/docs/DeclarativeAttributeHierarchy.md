# DeclarativeAttributeHierarchy


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **object** | Free-form JSON object | 
**created_at** | **str** | Time of the entity creation. | [optional] 
**created_by** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**description** | **str** | Attribute hierarchy object description. | [optional] 
**id** | **str** | Attribute hierarchy object ID. | 
**modified_at** | **str** | Time of the last entity modification. | [optional] 
**modified_by** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**tags** | **List[str]** | A list of tags. | [optional] 
**title** | **str** | Attribute hierarchy object title. | 

## Example

```python
from gooddata_api_client.models.declarative_attribute_hierarchy import DeclarativeAttributeHierarchy

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeAttributeHierarchy from a JSON string
declarative_attribute_hierarchy_instance = DeclarativeAttributeHierarchy.from_json(json)
# print the JSON string representation of the object
print(DeclarativeAttributeHierarchy.to_json())

# convert the object into a dict
declarative_attribute_hierarchy_dict = declarative_attribute_hierarchy_instance.to_dict()
# create an instance of DeclarativeAttributeHierarchy from a dict
declarative_attribute_hierarchy_from_dict = DeclarativeAttributeHierarchy.from_dict(declarative_attribute_hierarchy_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


