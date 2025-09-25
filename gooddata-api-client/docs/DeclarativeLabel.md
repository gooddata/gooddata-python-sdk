# DeclarativeLabel

A attribute label.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** | Label description. | [optional] 
**id** | **str** | Label ID. | 
**is_hidden** | **bool** | Determines if the label is hidden from AI features. | [optional] 
**source_column** | **str** | A name of the source column in the table. | 
**source_column_data_type** | **str** | A type of the source column | [optional] 
**tags** | **List[str]** | A list of tags. | [optional] 
**title** | **str** | Label title. | 
**value_type** | **str** | Specific type of label | [optional] 

## Example

```python
from gooddata_api_client.models.declarative_label import DeclarativeLabel

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeLabel from a JSON string
declarative_label_instance = DeclarativeLabel.from_json(json)
# print the JSON string representation of the object
print(DeclarativeLabel.to_json())

# convert the object into a dict
declarative_label_dict = declarative_label_instance.to_dict()
# create an instance of DeclarativeLabel from a dict
declarative_label_from_dict = DeclarativeLabel.from_dict(declarative_label_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


