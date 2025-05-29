---
title: "GoodData AI (beta)"
linkTitle: "GoodData AI (beta)"
weight: 24
no_list: true
---

GoodData AI is a feature that allows you to ask questions about your data in natural language.

For more information on how to use and setup GoodData AI, see the [GoodData AI documentation](https://www.gooddata.com/docs/cloud/ai/).

## Methods

* [ai_chat](./ai_chat/)
* [ai_chat_stream](./ai_chat_stream/)
* [get_ai_chat_history](./get_ai_chat_history/)
* [reset_ai_chat_history](./reset_ai_chat_history/)
* [set_ai_chat_history_feedback](./set_ai_chat_history_feedback/)
* [search_ai](./search_ai/)
* [sync_metadata](./sync_metadata/)


## Example

This example shows how to use the GoodData AI to get execution definition. You can also use it to get a pandas dataframe, but for that you need to use the [GoodPandas](../../pandas/).

```python
from gooddata_sdk import GoodDataSdk # For AI chat and execution definition.
from gooddata_pandas import GoodDataPandas # For pandas dataframe.


host = "https://www.example.com"
token = "<your_personal_access_token>"
sdk = GoodDataSdk.create(host, token)

# Get execution definition from AI chat (not needed for pandas dataframe)
response = sdk.compute.ai_chat(test_workspace_id, "Display the revenue by product")
execution_definition = sdk.compute.buid_exec_def_from_chat_result(response)

# Create a pandas dataframe from the AI response.
gp = GoodDataPandas(host, token)
gdf = gp.data_frames(workspace_id)
df, df_metadata = gdf.for_created_visualization(response)

# Print the results
print(execution_definition) # Execution Definition.
print(df_metadata) # Dataframe metadata.
print(df) # Pandas dataframe.
```
