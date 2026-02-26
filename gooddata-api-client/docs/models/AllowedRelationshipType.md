# gooddata_api_client.model.allowed_relationship_type.AllowedRelationshipType

Allowed relationship type combination.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Allowed relationship type combination. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**sourceType** | str,  | str,  | Source object type (e.g., &#x27;dashboard&#x27;, &#x27;visualization&#x27;, &#x27;metric&#x27;). | must be one of ["attribute", "metric", "fact", "label", "date", "dataset", "visualization", "dashboard", ] 
**targetType** | str,  | str,  | Target object type (e.g., &#x27;visualization&#x27;, &#x27;metric&#x27;, &#x27;attribute&#x27;). | must be one of ["attribute", "metric", "fact", "label", "date", "dataset", "visualization", "dashboard", ] 
**allowOrphans** | bool,  | BoolClass,  | If true, allows target objects that are not part of any relationship (orphans) to be included in results. If false, orphan target objects will be excluded even if they directly match the search query. Default is true (orphans are allowed). | [optional] if omitted the server will use the default value of True
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

