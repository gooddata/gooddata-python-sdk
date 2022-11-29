---
title: "get_insights"
linkTitle: "get_insights"
weight: 15
superheading: "insights."
---

<!-- TODO -->

``get_insights(workspace_id: str)``

Returns *list[Insight]*.

Retrieve a list of visualization objects.

## Example

```Python
# Get all visualizations
insights = sdk.insights.get_insights(workspace_id="123")
```
