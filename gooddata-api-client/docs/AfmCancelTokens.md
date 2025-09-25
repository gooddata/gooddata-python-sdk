# AfmCancelTokens

Any information related to cancellation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**result_id_to_cancel_token_pairs** | **Dict[str, str]** | resultId to cancel token pairs | 

## Example

```python
from gooddata_api_client.models.afm_cancel_tokens import AfmCancelTokens

# TODO update the JSON string below
json = "{}"
# create an instance of AfmCancelTokens from a JSON string
afm_cancel_tokens_instance = AfmCancelTokens.from_json(json)
# print the JSON string representation of the object
print(AfmCancelTokens.to_json())

# convert the object into a dict
afm_cancel_tokens_dict = afm_cancel_tokens_instance.to_dict()
# create an instance of AfmCancelTokens from a dict
afm_cancel_tokens_from_dict = AfmCancelTokens.from_dict(afm_cancel_tokens_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


