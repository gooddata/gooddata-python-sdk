# ChatHistoryInteraction

List of chat history interactions.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**interaction_finished** | **bool** | Has the interaction already finished? Can be used for polling when interaction is in progress. | 
**interaction_id** | **int** | Chat History interaction ID. Unique ID for each interaction. | 
**question** | **str** | User question | 
**routing** | [**RouteResult**](RouteResult.md) |  | 
**thread_id** | **str** | Chat History thread ID. Backend persists chat history and returns ID for further requests. | 
**created_visualizations** | [**CreatedVisualizations**](CreatedVisualizations.md) |  | [optional] 
**found_objects** | [**FoundObjects**](FoundObjects.md) |  | [optional] 
**text_response** | **str** | Text response for general questions. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


