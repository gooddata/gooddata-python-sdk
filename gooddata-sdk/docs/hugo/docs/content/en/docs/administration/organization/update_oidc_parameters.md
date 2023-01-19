---
title: "update_oidc_parameters"
linkTitle: "update_oidc_parameters"
weight: 20
no_list: true
superheading: "catalog_organization."
---



``update_oidc_parameters(oauth_issuer_location: Optional[str] = None, oauth_client_id: Optional[str] = None, oauth_client_secret: Optional[str] = None)``

Updates the OIDC parameters for a given users.

{{% parameters-block  title="Parameters"%}}

{{< parameter p_name="oauth_issuer_location" p_type="Optional[string]" >}}
Issuer location. Defaults to None.
{{< /parameter >}}
{{< parameter p_name="oauth_client_id" p_type="Optional[string]" >}}
Public client identifier. Defaults to None.
{{< /parameter >}}
{{< parameter p_name="oauth_client_secret" p_type="Optional[string]" >}}
Client secret. Defaults to None.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes"%}}
{{% /parameters-block %}}

{{% parameters-block title="Raises"%}}
{{< parameter p_name="ValueError" >}}
Parameters were not strictly all none or all string.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Update OIDC provider
sdk.catalog_organization.update_oidc_parameters(oauth_client_id="oauth_client_id",
                                                oauth_issuer_location="oauth_issuer_location",
                                                oauth_client_secret="oauth_client_secret")
```
