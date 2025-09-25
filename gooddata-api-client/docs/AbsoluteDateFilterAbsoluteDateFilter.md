# AbsoluteDateFilterAbsoluteDateFilter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**apply_on_result** | **bool** |  | [optional] 
**dataset** | [**AfmObjectIdentifierDataset**](AfmObjectIdentifierDataset.md) |  | 
**var_from** | **str** |  | 
**local_identifier** | **str** |  | [optional] 
**to** | **str** |  | 

## Example

```python
from gooddata_api_client.models.absolute_date_filter_absolute_date_filter import AbsoluteDateFilterAbsoluteDateFilter

# TODO update the JSON string below
json = "{}"
# create an instance of AbsoluteDateFilterAbsoluteDateFilter from a JSON string
absolute_date_filter_absolute_date_filter_instance = AbsoluteDateFilterAbsoluteDateFilter.from_json(json)
# print the JSON string representation of the object
print(AbsoluteDateFilterAbsoluteDateFilter.to_json())

# convert the object into a dict
absolute_date_filter_absolute_date_filter_dict = absolute_date_filter_absolute_date_filter_instance.to_dict()
# create an instance of AbsoluteDateFilterAbsoluteDateFilter from a dict
absolute_date_filter_absolute_date_filter_from_dict = AbsoluteDateFilterAbsoluteDateFilter.from_dict(absolute_date_filter_absolute_date_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


