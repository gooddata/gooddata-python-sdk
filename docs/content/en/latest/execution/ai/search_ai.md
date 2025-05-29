---
title: "search_ai"
linkTitle: "search_ai"
weight: 98
superheading: "compute."
---

``search_ai(
        workspace_id: str,
        question: str,
        deep_search: Optional[bool] = None,
        limit: Optional[int] = None,
        object_types: Optional[list[str]] = None,
        relevant_score_threshold: Optional[float] = None,
        title_to_descriptor_ratio: Optional[float] = None,
    ) -> SearchResult:``

Search for metadata objects using similarity search.

Default values for optional parameters are documented in the AI Search endpoint of the GoodData API.


{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="str" >}}
The ID of the GoodData Workspace.
{{< /parameter >}}
{{< parameter p_name="question" p_type="str" >}}
The question to ask the AI.
{{< /parameter >}}
{{< parameter p_name="deep_search" p_type="Optional[bool]" >}}
turn on deep search - if true, content of complex objects will be searched as well
{{< /parameter >}}
{{< parameter p_name="limit" p_type="Optional[int]" >}}
maximum number of results to return. Defaults to None.
{{< /parameter >}}
{{< parameter p_name="object_types" p_type="Optional[list[str]]" >}}
list of object types to search for. Enum items: "attribute", "metric", "fact", "label", "date", "dataset", "visualization" and "dashboard". Defaults to None.
{{< /parameter >}}
{{< parameter p_name="relevant_score_threshold" p_type="Optional[float]" >}}
minimum relevance score threshold for results. Defaults to None.
{{< /parameter >}}
{{< parameter p_name="title_to_descriptor_ratio" p_type="Optional[float]" >}}
ratio of title score to descriptor score. Defaults to None.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}
{{< parameter p_name="search_result" p_type="SearchResult" >}}
SearchResult: Search results{{< /parameter >}}
{{% /parameters-block %}}


## Example

```python

host = "https://www.example.com"
token = "<your_personal_access_token>"
sdk = GoodDataSdk.create(host, token)

chat_result = sdk.compute.ai_chat(workspace_id, "Display the revenue by product")

print(chat_result)
```
