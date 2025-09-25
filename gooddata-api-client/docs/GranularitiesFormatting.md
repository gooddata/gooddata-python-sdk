# GranularitiesFormatting

A date dataset granularities title formatting rules.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title_base** | **str** | Title base is used as a token in title pattern. If left empty, it is replaced by date dataset title. | 
**title_pattern** | **str** | This pattern is used to generate the title of attributes and labels that result from the granularities. There are two tokens available:  * &#x60;%titleBase&#x60; - represents shared part by all titles, or title of Date Dataset if left empty * &#x60;%granularityTitle&#x60; - represents &#x60;DateGranularity&#x60; built-in title | 

## Example

```python
from gooddata_api_client.models.granularities_formatting import GranularitiesFormatting

# TODO update the JSON string below
json = "{}"
# create an instance of GranularitiesFormatting from a JSON string
granularities_formatting_instance = GranularitiesFormatting.from_json(json)
# print the JSON string representation of the object
print(GranularitiesFormatting.to_json())

# convert the object into a dict
granularities_formatting_dict = granularities_formatting_instance.to_dict()
# create an instance of GranularitiesFormatting from a dict
granularities_formatting_from_dict = GranularitiesFormatting.from_dict(granularities_formatting_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


