# gooddata_api_client.model.granularities_formatting.GranularitiesFormatting

A date dataset granularities title formatting rules.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A date dataset granularities title formatting rules. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**titlePattern** | str,  | str,  | This pattern is used to generate the title of attributes and labels that result from the granularities. There are two tokens available:  * &#x60;%titleBase&#x60; - represents shared part by all titles, or title of Date Dataset if left empty * &#x60;%granularityTitle&#x60; - represents &#x60;DateGranularity&#x60; built-in title | 
**titleBase** | str,  | str,  | Title base is used as a token in title pattern. If left empty, it is replaced by date dataset title. | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

