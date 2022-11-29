---
title: "get_facts_catalog"
linkTitle: "get_facts_catalog"
weight: 40
superheading: "catalog_workspace_content."
---

<!-- TODO -->

``get_facts_catalog(workspace_id: str)``

Returns *list[CatalogFact]*

Retrieve all facts for a workspace.

## Example

```Python
# Get all the facts
facts = sdk.catalog_workspace_content.get_facts_catalog(workspace_id="123")
```
