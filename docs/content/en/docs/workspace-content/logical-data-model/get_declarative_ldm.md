---
title: "get_declarative_ldm"
linkTitle: "get_declarative_ldm"
weight: 80
superheading: "catalog_workspace_content."
---



``get_declarative_ldm(workspace_id: str)``

Gets a logical model layout.

On CatalogDeclarativeModel user can call ``modify_mapped_data_source(data_source_mapping: dict)`` method, which substitutes data source id in datasets.

{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogDeclarativeModel" >}}
Object Containing declarative Logical Data Model
{{< /parameter >}}
{{% /parameters-block %}}

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
