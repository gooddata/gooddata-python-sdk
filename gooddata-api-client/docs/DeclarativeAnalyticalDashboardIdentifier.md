# DeclarativeAnalyticalDashboardIdentifier

An analytical dashboard identifier.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Identifier of the analytical dashboard. | 
**type** | **str** | A type. | 

## Example

```python
from gooddata_api_client.models.declarative_analytical_dashboard_identifier import DeclarativeAnalyticalDashboardIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeAnalyticalDashboardIdentifier from a JSON string
declarative_analytical_dashboard_identifier_instance = DeclarativeAnalyticalDashboardIdentifier.from_json(json)
# print the JSON string representation of the object
print(DeclarativeAnalyticalDashboardIdentifier.to_json())

# convert the object into a dict
declarative_analytical_dashboard_identifier_dict = declarative_analytical_dashboard_identifier_instance.to_dict()
# create an instance of DeclarativeAnalyticalDashboardIdentifier from a dict
declarative_analytical_dashboard_identifier_from_dict = DeclarativeAnalyticalDashboardIdentifier.from_dict(declarative_analytical_dashboard_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


