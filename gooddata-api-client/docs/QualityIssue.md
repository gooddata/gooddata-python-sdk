# QualityIssue


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** |  | 
**detail** | **Dict[str, object]** |  | 
**objects** | [**List[QualityIssueObject]**](QualityIssueObject.md) |  | 
**severity** | **str** |  | 

## Example

```python
from gooddata_api_client.models.quality_issue import QualityIssue

# TODO update the JSON string below
json = "{}"
# create an instance of QualityIssue from a JSON string
quality_issue_instance = QualityIssue.from_json(json)
# print the JSON string representation of the object
print(QualityIssue.to_json())

# convert the object into a dict
quality_issue_dict = quality_issue_instance.to_dict()
# create an instance of QualityIssue from a dict
quality_issue_from_dict = QualityIssue.from_dict(quality_issue_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


