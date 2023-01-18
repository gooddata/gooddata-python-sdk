---
title: "get_insight"
linkTitle: "get_insight"
weight: 15
superheading: "insights."
---

<!-- TODO -->

``get_insight(workspace_id: str, insight_id: str)``

Gets a single insight from a workspace.


{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="insight_id" p_type="string" >}}
Insight identifier string e.g. "bikes"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}
{{< parameter p_type="Insight" >}}
A single Insight object contains side loaded metadata about the entities it references
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```Python
# Get all visualizations
insights = sdk.insights.get_insights(workspace_id="123")
```
