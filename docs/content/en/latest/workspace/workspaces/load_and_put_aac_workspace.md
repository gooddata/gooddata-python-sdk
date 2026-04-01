---
title: "load_and_put_aac_workspace"
linkTitle: "load_and_put_aac_workspace"
weight: 135
superheading: "catalog_workspace."
api_ref: "CatalogWorkspaceService.load_and_put_aac_workspace"
---

<!-- AUTO-GENERATED FROM DOCSTRING — do not edit above this line -->

<div class="python-ref">
<p><code>load_and_put_aac_workspace(workspace_id: str, source_dir: Path)</code></p>
<div class="python-ref-description">
<p>Load AAC YAML files from source_dir, convert to declarative, and deploy to workspace.</p>
</div>
<h4>Parameters</h4>
<table class="gd-docs-parameters-block">
<thead>
<tr>
<th>name</th>
<th>type</th>
<th>description</th>
</tr>
</thead>
<tbody>
<tr>
<th padding="0px">workspace_id
<th padding="0px">str
<th>
Workspace identification string e.g. "demo"
</tr>
<tr>
<th padding="0px">source_dir
<th padding="0px">Path
<th>
Path to the directory containing AAC YAML files.
</tr>
</tbody>
</table>
<h4>Returns</h4>
<i>None</i>
</div>

## Example

Deploy AAC YAML files from a local directory to a workspace:

```python
from pathlib import Path
from gooddata_sdk import GoodDataSdk

host = "https://www.example.com"
token = "some_user_token"
sdk = GoodDataSdk.create(host, token)

# Deploy AAC YAML files to workspace
sdk.catalog_workspace.load_and_put_aac_workspace(
    workspace_id="demo",
    source_dir=Path("analytics")
)
```

The AAC YAML directory can contain typed subdirectories:

```
analytics/
    datasets/
        campaigns.yaml
        orders.yaml
    metrics/
        revenue.yaml
    visualisations/
        revenue_chart.yaml
    dashboards/
        overview.yaml
```

Each YAML file has a `type` field that determines its kind:

```yaml
type: metric
id: revenue
title: Revenue
maql: SELECT SUM({fact/amount})
format: "#,##0"
```
