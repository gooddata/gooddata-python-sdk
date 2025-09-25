# RunningSection

Footer section of the slide

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**left** | **str** | Either {{logo}} variable or custom text with combination of other variables. | [optional] 
**right** | **str** | Either {{logo}} variable or custom text with combination of other variables. | [optional] 

## Example

```python
from gooddata_api_client.models.running_section import RunningSection

# TODO update the JSON string below
json = "{}"
# create an instance of RunningSection from a JSON string
running_section_instance = RunningSection.from_json(json)
# print the JSON string representation of the object
print(RunningSection.to_json())

# convert the object into a dict
running_section_dict = running_section_instance.to_dict()
# create an instance of RunningSection from a dict
running_section_from_dict = RunningSection.from_dict(running_section_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


