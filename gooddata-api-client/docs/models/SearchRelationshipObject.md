# gooddata_api_client.model.search_relationship_object.SearchRelationshipObject

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**targetObjectTitle** | str,  | str,  | Target object title. | 
**sourceObjectType** | str,  | str,  | Source object type, e.g. dashboard. | 
**targetObjectId** | str,  | str,  | Target object ID. | 
**sourceWorkspaceId** | str,  | str,  | Source workspace ID. If relationship is dashboard-&gt;visualization, this is the workspace where the dashboard is located. | 
**targetWorkspaceId** | str,  | str,  | Target workspace ID. If relationship is dashboard-&gt;visualization, this is the workspace where the visualization is located. | 
**sourceObjectId** | str,  | str,  | Source object ID. | 
**sourceObjectTitle** | str,  | str,  | Source object title. | 
**targetObjectType** | str,  | str,  | Target object type, e.g. visualization. | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

