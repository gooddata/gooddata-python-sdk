---
title: "for_insight"
linkTitle: "for_insight"
weight: 10
superheading: "table."
---

<!-- TODO -->

``for_insight(workspace_id: str, insight: Insight)``

Returns *ExecutionTable*.

Retrieve data as an ExecutionTable from the given visualization.

## Example

```Python
# Get visualization
campaign_spend_insight = sdk.insights.get_insight(workspace_id="123", insight_id="campaign_spend")
# Get the visualization as Execution Table
sdk.tables.for_insight(workspace_id="123", insight=campaign_spend_insight)

#ExecutionTable(
#   response=Execution(
#       workspace_id=demo,
#       result_id=c3899bb07edee259331707f817d710c80218b1ef
#   ),
#   columns=[
#           '291c085e7df8420db84117ca49f59c49',
#           'd9dd143d647d4d148405a60ec2cf59bc',
#           'd319bcb2d8c04442a684e3b3cd063381'
#   ],
#   rows=143
#)
```
