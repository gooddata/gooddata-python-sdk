# GetQualityIssuesResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**issues** | [**List[QualityIssue]**](QualityIssue.md) |  | 

## Example

```python
from gooddata_api_client.models.get_quality_issues_response import GetQualityIssuesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetQualityIssuesResponse from a JSON string
get_quality_issues_response_instance = GetQualityIssuesResponse.from_json(json)
# print the JSON string representation of the object
print(GetQualityIssuesResponse.to_json())

# convert the object into a dict
get_quality_issues_response_dict = get_quality_issues_response_instance.to_dict()
# create an instance of GetQualityIssuesResponse from a dict
get_quality_issues_response_from_dict = GetQualityIssuesResponse.from_dict(get_quality_issues_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


