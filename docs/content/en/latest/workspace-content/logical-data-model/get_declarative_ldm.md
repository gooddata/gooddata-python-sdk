---
title: "get_declarative_ldm"
linkTitle: "get_declarative_ldm"
weight: 80
superheading: "catalog_workspace_content."
---

{{< api-ref "sdk.CatalogWorkspaceContentService.get_declarative_ldm" >}}

## Example

```python
# Get declarative Logical Data Model
declarative_ldm = sdk.catalog_workspace_content.get_declarative_ldm(workspace_id="123")

# CatalogDeclarativeModel(
#    ldm=CatalogDeclarativeLdm(
#        datasets=[
#            CatalogDeclarativeDataset(
#                id='campaign_channels',
#                title='Campaign channels',
#                grain=[
#                    CatalogGrainIdentifier(
#                        id='campaign_channel_id',
#                        type='attribute'
#                    )
#                ],
#                references=[
#                    CatalogDeclarativeReference(
#                        identifier=CatalogReferenceIdentifier(
#                            id='campaigns'
#                        ),
#                        multivalue=False,
#                         source_columns=['campaign_id']
#                    )
#                ],
#                description='Campaign channels',
#                attributes=[
#                    CatalogDeclarativeAttribute(
#                        id='campaign_channel_id',
#                        title='Campaign channel id',
#                        source_column='campaign_channel_id',
#                        labels=[],
# ...
```
