---
title: "get_insights"
linkTitle: "get_insights"
weight: 15
superheading: "insights."
---

``get_insights(workspace_id: str)``

Gets a list of visualization objects.

{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}
{{< parameter p_type="list[Insight]" >}}
All available insights, each insight will contain side loaded metadata about the entities it references
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Get all visualizations
insights = sdk.insights.get_insights(workspace_id="123")
```
