# QualityIssueObject


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**type** | **str** |  | 

## Example

```python
from gooddata_api_client.models.quality_issue_object import QualityIssueObject

# TODO update the JSON string below
json = "{}"
# create an instance of QualityIssueObject from a JSON string
quality_issue_object_instance = QualityIssueObject.from_json(json)
# print the JSON string representation of the object
print(QualityIssueObject.to_json())

# convert the object into a dict
quality_issue_object_dict = quality_issue_object_instance.to_dict()
# create an instance of QualityIssueObject from a dict
quality_issue_object_from_dict = QualityIssueObject.from_dict(quality_issue_object_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


