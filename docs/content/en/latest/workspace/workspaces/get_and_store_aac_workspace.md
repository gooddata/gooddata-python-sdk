---
title: "get_and_store_aac_workspace"
linkTitle: "get_and_store_aac_workspace"
weight: 136
superheading: "catalog_workspace."
api_ref: "CatalogWorkspaceService.get_and_store_aac_workspace"
---

<!-- AUTO-GENERATED FROM DOCSTRING — do not edit above this line -->

<div class="python-ref">
<p><code>get_and_store_aac_workspace(workspace_id: str, source_dir: Path)</code></p>
<div class="python-ref-description">
<p>Get declarative workspace from server, convert to AAC YAML files, and write to disk.</p>
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
Path to the directory where AAC YAML files will be written.
</tr>
</tbody>
</table>
<h4>Returns</h4>
<i>None</i>
</div>

## Example

Clone a workspace layout as AAC YAML files:

```python
from pathlib import Path
from gooddata_sdk import GoodDataSdk

host = "https://www.example.com"
token = "some_user_token"
sdk = GoodDataSdk.create(host, token)

# Clone workspace to AAC YAML files
sdk.catalog_workspace.get_and_store_aac_workspace(
    workspace_id="demo",
    source_dir=Path("analytics")
)
```

This creates typed subdirectories under the target path:

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
