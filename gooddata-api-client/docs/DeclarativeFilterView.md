# DeclarativeFilterView


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**analytical_dashboard** | [**DeclarativeAnalyticalDashboardIdentifier**](DeclarativeAnalyticalDashboardIdentifier.md) |  | [optional] 
**content** | **object** | Free-form JSON object | [optional] 
**description** | **str** |  | [optional] 
**id** | **str** | FilterView object ID. | 
**is_default** | **bool** | Indicator whether the filter view should by applied by default. | [optional] 
**tags** | **List[str]** |  | [optional] 
**title** | **str** |  | 
**user** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.declarative_filter_view import DeclarativeFilterView

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeFilterView from a JSON string
declarative_filter_view_instance = DeclarativeFilterView.from_json(json)
# print the JSON string representation of the object
print(DeclarativeFilterView.to_json())

# convert the object into a dict
declarative_filter_view_dict = declarative_filter_view_instance.to_dict()
# create an instance of DeclarativeFilterView from a dict
declarative_filter_view_from_dict = DeclarativeFilterView.from_dict(declarative_filter_view_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


