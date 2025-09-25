# GetImageExport202ResponseInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**char** | **str** |  | [optional] 
**direct** | **bool** |  | [optional] 
**double** | **float** |  | [optional] 
**var_float** | **float** |  | [optional] 
**int** | **int** |  | [optional] 
**long** | **int** |  | [optional] 
**read_only** | **bool** |  | [optional] 
**short** | **int** |  | [optional] 

## Example

```python
from gooddata_api_client.models.get_image_export202_response_inner import GetImageExport202ResponseInner

# TODO update the JSON string below
json = "{}"
# create an instance of GetImageExport202ResponseInner from a JSON string
get_image_export202_response_inner_instance = GetImageExport202ResponseInner.from_json(json)
# print the JSON string representation of the object
print(GetImageExport202ResponseInner.to_json())

# convert the object into a dict
get_image_export202_response_inner_dict = get_image_export202_response_inner_instance.to_dict()
# create an instance of GetImageExport202ResponseInner from a dict
get_image_export202_response_inner_from_dict = GetImageExport202ResponseInner.from_dict(get_image_export202_response_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


