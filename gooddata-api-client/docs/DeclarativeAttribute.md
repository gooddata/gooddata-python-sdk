# DeclarativeAttribute

A dataset attribute.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**default_view** | [**LabelIdentifier**](LabelIdentifier.md) |  | [optional] 
**description** | **str** | Attribute description. | [optional] 
**id** | **str** | Attribute ID. | 
**is_hidden** | **bool** | If true, this attribute is hidden from AI search results. | [optional] 
**labels** | [**List[DeclarativeLabel]**](DeclarativeLabel.md) | An array of attribute labels. | 
**sort_column** | **str** | Attribute sort column. | [optional] 
**sort_direction** | **str** | Attribute sort direction. | [optional] 
**source_column** | **str** | A name of the source column that is the primary label | 
**source_column_data_type** | **str** | A type of the source column | [optional] 
**tags** | **List[str]** | A list of tags. | [optional] 
**title** | **str** | Attribute title. | 

## Example

```python
from gooddata_api_client.models.declarative_attribute import DeclarativeAttribute

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeAttribute from a JSON string
declarative_attribute_instance = DeclarativeAttribute.from_json(json)
# print the JSON string representation of the object
print(DeclarativeAttribute.to_json())

# convert the object into a dict
declarative_attribute_dict = declarative_attribute_instance.to_dict()
# create an instance of DeclarativeAttribute from a dict
declarative_attribute_from_dict = DeclarativeAttribute.from_dict(declarative_attribute_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


