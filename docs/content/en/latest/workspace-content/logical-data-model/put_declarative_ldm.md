---
title: "put_declarative_ldm"
linkTitle: "put_declarative_ldm"
weight: 90
superheading: "catalog_workspace_content."
---

{{< api-ref "sdk.CatalogWorkspaceContentService.put_declarative_ldm" >}}

## Example

```python
# Generate logical data model
logical_model = sdk.catalog_data_source.generate_logical_model(data_source_id="demo-test-ds")

# Do some changes
# ...

# Put logical data model
sdk.catalog_workspace_content.put_declarative_ldm(workspace_id="demo", ldm=logical_model)
```
