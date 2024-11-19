---
title: "put_declarative_notification_channels"
linkTitle: "put_declarative_notification_channels..."
weight: 190
no_list: true
superheading: "catalog_organization."
---

{{< api-ref "sdk.CatalogOrganizationService.put_declarative_notification_channels" >}}

## Example

```python
from gooddata_sdk import CatalogDeclarativeNotificationChannel, CatalogWebhook

notification_channels = [CatalogDeclarativeNotificationChannel(
    id="webhook", name="Webhook", destination=CatalogWebhook(url="https://webhook.site", token="123")
)]
sdk.catalog_organization.put_declarative_notification_channels()
```
