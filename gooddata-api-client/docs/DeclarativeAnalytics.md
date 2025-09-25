# DeclarativeAnalytics

Entities describing users' view on data.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**analytics** | [**DeclarativeAnalyticsLayer**](DeclarativeAnalyticsLayer.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.declarative_analytics import DeclarativeAnalytics

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeAnalytics from a JSON string
declarative_analytics_instance = DeclarativeAnalytics.from_json(json)
# print the JSON string representation of the object
print(DeclarativeAnalytics.to_json())

# convert the object into a dict
declarative_analytics_dict = declarative_analytics_instance.to_dict()
# create an instance of DeclarativeAnalytics from a dict
declarative_analytics_from_dict = DeclarativeAnalytics.from_dict(declarative_analytics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


